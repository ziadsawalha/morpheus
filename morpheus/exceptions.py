'''Morpheus Exceptions'''


class ValidationError(StandardError):
    '''Used to indicate that a one or more validation rules failed'''

    def __init__(self, message, errors=None):
        StandardError.__init__(self, message)
        self.errors = errors
