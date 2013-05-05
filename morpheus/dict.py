'''
The main morpheus dict substitute class lives here: MorpheusDict
'''
from abc import ABCMeta
import collections


class MorpheusDict(collections.MutableMapping):
    ''' DOCS '''
    __metaclass__ = ABCMeta

    #
    # dict emulation methods
    #
    def __init__(self, *args, **kwargs):
        obj = dict(*args, **kwargs)
        self.__data = obj

    def __len__(self):
        return len(self.__data)

    def __contains__(self, key):
        return key in self.__data

    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, key):
        return self.__data[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.__data[self.__keytransform__(key)] = value

    def __delitem__(self, k):
        del self.__data[k]

    @staticmethod
    def __keytransform__(key):
        return key

    def __repr__(self):
        return self.__data.__repr__()

    def __dict__(self):
        return self.__data

MorpheusDict.register(dict)  # pylint: disable=E1101
