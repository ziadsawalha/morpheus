'''
The main morpheus dict substitute class lives here: MorpheusDict
'''
from abc import ABCMeta
import inspect
import types

from morpheus.operations import SchemaOp


class MorpheusDict(dict):
    ''' DOCS '''

    __metaclass__ = ABCMeta

    def __new__(cls, *args, **kwargs):
        obj = dict.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    #
    # dict emulation methods
    #
    def __init__(self, *args, **kwargs):
        # TODO: do this only once, not on class init
        self.definitions = self.get_schema_definitions()
        self.parse_schema_definitions(self.definitions)

        dict.__init__(self, *args, **kwargs)
        if hasattr(self.__class__, '__schema__'):
            self.validate(self)

    def __setitem__(self, key, value):
        if (hasattr(self, 'allowed') and self.allowed and
                key not in self.allowed):
            raise AttributeError("'%s' is not permitted on an object of type "
                                 "'%s'" % (key, self.__class__.__name__))
        dict.__setitem__(self, self.__keytransform__(key), value)

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
        schema = getattr(cls, '__schema__', None) or {}
        item_definitions = {}
        if isinstance(schema, type):
            for key in get_class_vars(schema):
                item_definitions[key] = getattr(schema, key)
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
                                "class or morpheus.Schema class")
        return item_definitions

    @classmethod
    def parse_schema_definitions(cls, definitions):
        '''

        Normalizes and preprocesses all schema definitions.

        Sets:
        cls.allowed: all allowed keys
        cls.required: all required keys

        '''
        cls.allowed = set(definitions.keys())
        cls.required = set([])

    def validate(self, data):
        '''

        Checks schema and validates data. Raises error if errors exist.

        Call inspect if you want to check the data without raising and error.

        '''

        existing = set(data.keys())
        extras = existing - self.allowed
        if extras:
            if len(extras) == 1:
                msg = "'%s' is not a permitted attribute for a '%s'"
            else:
                msg = "%s are not permitted attributes for a '%s'"
            raise AttributeError(msg % (', '.join(extras),
                                        self.__class__.__name__))

        for key in data.keys():
            definition = self.definitions[key]
            if issubclass(definition.__class__, SchemaOp):
                definition.execute(data, key)


def get_class_vars(cls):
    '''Get unhidden variables defined on a class'''
    return [name for name, obj in cls.__dict__.iteritems()
            if not name.startswith("__") and not inspect.isroutine(obj)]
