'''

Chainable Operations morpheus supports in a schema definition

Example:

class Foo(dict):
    __schema__ = dict(
        id=Defn(int, required=True),
        status=basestring,
        state=as_of(0.7).is_replaced_by('status')
    )

'''


class SchemaOp(object):
    ''' DOCS '''

    def __init__(self, *args, **kwargs):
        ''' DOCS '''
        self.args = list(args) or []
        op_name = self.__class__.__name__
        self.chain = [(op_name, args, kwargs)]
        self.required = (op_name == 'is_required' or
                         kwargs.get('required') is True)

    def __call__(self, *args, **kwargs):
        ''' DOCS '''
        self.chain[-1] = (self.chain[-1][0], args, kwargs)
        return self

    def __getattr__(self, name):
        ''' DOCS '''
        self.chain.append((name, (), {}))
        return self

    def execute(self, data, key, fail_fast=False):
        ''' DOCS '''
        errors = []
        for command, args, kwargs in self.chain:
            if command == 'is_replaced_by':
                data[args[0]] = data.pop(key)
            elif command == 'is_required':
                if key not in data:
                    errors.append("'%s' is required" % key)
                    if fail_fast is True:
                        return errors
            elif command == 'is_type':
                if key not in data:
                    continue
                value = data[key]
                if not isinstance(value, args[0]):
                    errors.append("'%s' is not a(n) %s" % (key,
                                  args[0].__name__))
                    if fail_fast is True:
                        return errors
            elif command == 'Defn':
                # TODO: Make DRY
                if key not in data:
                    if self.required is True:
                        errors.append("'%s' is required" % key)
                        if fail_fast is True:
                            return errors

                if key not in data:
                    continue
                value = data[key]
                if not isinstance(value, args[0]):
                    errors.append("'%s' is not a(n) %s" % (key,
                                  args[0].__name__))
                    if fail_fast is True:
                        return errors
            elif command == 'as_of':
                pass
            else:
                raise SyntaxError("'%s' is not a recognized validation rule" %
                                  command)
        return errors


# pylint: disable=C0103
class as_of(SchemaOp):
    ''' DOCS '''
    pass


class is_type(SchemaOp):
    ''' DOCS '''
    pass


class is_required(SchemaOp):
    ''' DOCS '''
    pass


class is_replaced_by(SchemaOp):
    ''' DOCS '''
    pass


class Defn(SchemaOp):
    ''' DOCS '''
    pass
