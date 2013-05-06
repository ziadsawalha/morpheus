'''

Chainable Operations morpheus supports in a schema definition

Example:

class Foo(dict):
    __schema__ = dict(
        status=basestring,
        state=as_of(0.7).is_replaced_by('status')
    )

'''


class SchemaOp():
    ''' DOCS '''

    def __init__(self, *args, **kwargs):
        ''' DOCS '''
        self.args = list(args) or []
        self.chain = [(self.__class__.__name__, args, kwargs)]

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


class as_of(SchemaOp):
    pass
