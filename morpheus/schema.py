'''

Schema class for representing schema as a child class

Example:

class Foo(dict):
    __schema__ = Schema(
        status=basestring,
        state=as_of(0.7).is_replaced_by('status')
    )

'''


class Schema(dict):
    ''' DOCS '''
    pass
