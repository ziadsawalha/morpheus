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

from morpheus.exceptions import ValidationError


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

    def execute(self, data, key):
        ''' DOCS '''
        for command, args, kwargs in self.chain:
            if command == 'is_replaced_by':
                data[args[0]] = data.pop(key)
            elif command == 'is_required':
                if key not in data:
                    raise ValidationError("'%s' is required" % key)


# pylint: disable=C0103
class as_of(SchemaOp):
    ''' DOCS '''
    pass


class is_required(SchemaOp):
    ''' DOCS '''
    pass


class Defn(SchemaOp):
    ''' DOCS '''
    pass
