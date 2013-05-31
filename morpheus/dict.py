'''
The main morpheus dict substitute class lives here: MorpheusDict
'''
import inspect
import types

try:
    import yaml
    from yaml import SafeDumper, Dumper
    from yaml import representer
    YAML_DETECTED = True
except ImportError:  # pragma: nocover
    YAML_DETECTED = False


def register_yaml_representer(cls):
    ''' DOCS '''
    yaml.add_representer(cls, representer.Representer.represent_dict,
                         Dumper=Dumper)
    yaml.add_representer(cls, representer.SafeRepresenter.represent_dict,
                         Dumper=SafeDumper)

from morpheus.exceptions import ValidationError
from morpheus.schema import Schema
from morpheus.operations import SchemaOp, Defn


def get_class_vars(cls):
    '''Get unhidden variables defined on a class'''
    return [name for name, obj in cls.__dict__.iteritems()
            if not name.startswith("__") and not inspect.isroutine(obj)]


def normalize_definitions(definitions):
    '''Converts all definitions to Defn types'''
    if definitions:
        for key, definition in definitions.items():
            if isinstance(definition, SchemaOp):
                continue
            definitions[key] = Defn(definition)
    return definitions


class MorpheusDictSubclassDetector(type):
    '''Metaclass for MorpheusDict to detect when MorpheusDict is subclassed'''
    def __new__(mcs, *args, **kwargs):
        new_type = type.__new__(mcs, *args, **kwargs)
        new_type.definitions = new_type.get_schema_definitions()
        new_type.parse_schema_definitions(new_type.definitions)
        register_yaml_representer(new_type)
        if args[0] != "MorpheusDict":
            MorpheusDict.__initsubclass__(new_type)
        return new_type


class MorpheusDict(dict):
    ''' DOCS '''
    __metaclass__ = MorpheusDictSubclassDetector

    def __new__(cls, *args, **kwargs):
        obj = dict.__new__(cls)
        obj.__init__(*args, **kwargs)
        # TODO: don't register each one, but until I figure out how pyyaml
        # detects classes I need to:
        if YAML_DETECTED is True:
            register_yaml_representer(cls)
        return obj

    @classmethod
    def __initsubclass__(cls, subclass):
        '''Called when MorpheusDict has been subclassed'''
        # I wish we could do this here, but PyYAML dumping then fails
        # register_yaml_representer(cls)
        pass

    #
    # dict emulation methods
    #
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        if hasattr(self.__class__, '__schema__'):
            self.translate(self)
            self.validate(self, fail_fast=True)

    def __setitem__(self, key, value):
        if (hasattr(self, 'allowed') and self.allowed and
                key not in self.allowed):
            raise ValidationError("'%s' is not permitted on an object of type "
                                  "'%s'" % (key, self.__class__.__name__))
        dict.__setitem__(self, self.__keytransform__(key), value)

    def __delitem__(self, key):
        if key in self.required:
            raise ValidationError("Cannot remove required key '%s'" % key)
        dict.__delitem__(self, key)

    @staticmethod
    def __keytransform__(key):
        return key

    #
    # Schema methods
    #
    @classmethod
    def get_schema_definitions(cls):
        '''

        Finds the fields defined in the schema.

        The __schema__ attribute of a class can contain a list, a dict, or a
        class. A list we assume contains a list of allowed keys. A dict we
        assume has a valid schema dict. A class we assume has variables for
        definitions.

        :returns dict: keys are allowed item keys and values are the schema
                       definitions of those items

        '''
        schema = getattr(cls, '__schema__', None)
        item_definitions = {}
        if not schema:
            return item_definitions
        elif isinstance(schema, Schema):
            for key, value in schema.iteritems():
                item_definitions[key] = value
        elif isinstance(schema, list):
            for key in schema:
                item_definitions[key] = object
        elif isinstance(schema, (types.TypeType, types.ClassType)):
            for key in get_class_vars(schema):
                item_definitions[key] = getattr(schema, key)
        else:
            try:
                iter(schema)
                item_definitions = schema
            except TypeError:
                raise TypeError("__schema__ must be an iterable list, dict, "
                                "class or morpheus.Schema class, not %s" %
                                type(schema))

        return normalize_definitions(item_definitions)

    @classmethod
    def parse_schema_definitions(cls, definitions):
        '''

        Normalizes and preprocesses all schema definitions.

        Sets:
        cls.allowed: all allowed keys
        cls.required: all required keys

        '''
        try:
            if isinstance(cls.allowed, list):
                cls.allowed = set(cls.allowed)
        except AttributeError:
            cls.allowed = set()
        cls.allowed = cls.allowed.union(set(definitions.keys()))

        try:
            if isinstance(cls.required, list):
                cls.required = set(cls.required)
        except AttributeError:
            cls.required = set()
        cls.required = cls.required.union(
            set([k for k, v in definitions.items() if v.required is True]))

    # pylint: disable=E1101
    @classmethod
    def inspect(cls, data, fail_fast=False):
        '''

        Checks schema and validates data. Returns list of errors.

        Call inspect if you want to check the data without raising and error.

        :param fail_fast: if you want to return on the first error

        '''
        errors = []
        # Execute transforms and evals first
        for key in data.keys():
            if key in cls.definitions:
                definition = cls.definitions[key]
                if issubclass(definition.__class__, SchemaOp):
                    _, results = definition.execute(dict(data), key,
                                                    fail_fast=fail_fast)
                    if results:
                        errors += results
                        if fail_fast is True:
                            return errors
        # evaluate result
        existing = set(data.keys())
        extras = existing - cls.allowed
        if extras and len(cls.allowed) > 0:
            if len(extras) == 1:
                msg = "'%s' is not a permitted attribute for a '%s'"
            else:
                msg = "%s are not permitted attributes for a '%s'"
            errors.append(msg % (', '.join(extras), cls.__name__))
            if fail_fast is True:
                return errors

        if cls.required:
            missing = cls.required - set(data.keys())
            if missing:
                if len(missing) == 1:
                    msg = "Missing required key '%s'" % missing.pop()
                else:
                    msg = "Missing required keys: %s" % ', '.join(missing)
                errors.append(msg)
                if fail_fast is True:
                    return errors
        return errors

    @classmethod
    def validate(cls, data, fail_fast=False):
        '''

        Checks schema and validates data. Raises error if errors exist.

        Call inspect if you want to check the data without raising and error.

        '''

        errors = cls.inspect(data, fail_fast=fail_fast)
        if errors:
            raise ValidationError('. '.join(errors))

    @classmethod
    def translate(cls, data, target=None):
        '''

        Checks schema and executes all definitions.

        If not target is specified, it will execute all definitions on data
        itself.

        '''
        if target is None:
            target = data
        # Execute transforms and evals first
        for key, definition in cls.definitions.items():
            if issubclass(definition.__class__, SchemaOp):
                definition.execute(target, key)
