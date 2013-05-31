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
        modified = False
        for command, args, kwargs in self.chain:
            if command == 'is_replaced_by':
                if key in data:
                    data[args[0]] = data.pop(key)
                    modified = True
            elif command == 'is_required':
                if key not in data:
                    errors.append("'%s' is required" % key)
                    if fail_fast is True:
                        break
            elif command == 'is_type':
                if key not in data:
                    continue
                value = data[key]
                if not isinstance(value, args[0]):
                    errors.append("'%s' is not a(n) %s" % (key,
                                  args[0].__name__))
                    if fail_fast is True:
                        break
            elif command == 'Defn':
                # TODO: Make DRY
                if key not in data:
                    if self.required is True:
                        errors.append("'%s' is required" % key)
                        if fail_fast is True:
                            break

                if key not in data:
                    continue
                value = data[key]
                if not isinstance(value, args[0]):
                    errors.append("'%s' is not a(n) %s" % (key,
                                  args[0].__name__))
                    if fail_fast is True:
                        break
            elif command == 'translate':
                if key in data:
                    if self.args[0] and data[key] in self.args[0]:
                        data[key] = self.args[0][data[key]]
                        modified = True
            elif command == 'as_of':
                pass
            elif command == 'delete':
                if key in data:
                    del data[key]
                    modified = True
            elif command == 'write':
                """Writes a value into a dict building any intermediate keys"""
                parts = self.args[0].split('/')
                current = data
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = current = {}
                    else:
                        current = current[part]
                current[parts[-1]] = value
                modified = True
            elif command == 'read':
                """Reads a value from a dict supporting a path as a key"""
                parts = self.args[0].strip('/').split('/')
                current = data
                found = False
                if len(parts) == 1:
                    if key in current:
                        found = True
                else:
                    found = True
                    for part in parts[:-1]:
                        if part not in current:
                            break
                        current = current[part]
                        if not isinstance(current, dict):
                            break
                if found is True:
                    data[key] = current.get(parts[-1])
                    modified = True
            else:
                raise SyntaxError("'%s' is not a recognized validation rule" %
                                  command)
        return modified, errors


class Defn(SchemaOp):
    ''' DOCS '''
    pass


# pylint: disable=C0103
class as_of(SchemaOp):
    ''' DOCS '''
    pass


class delete(SchemaOp):
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


class read(SchemaOp):
    ''' DOCS '''
    pass


class translate(SchemaOp):
    ''' DOCS '''
    pass
