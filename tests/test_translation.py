# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict, Schema
from morpheus.operations import read, delete, translate, is_replaced_by, write


class Foo(MorpheusDict):
    __schema__ = Schema(
        id=int,
        status=translate({'PREVIOUS': 'NEW'}),
        answer=read('object/subobject/deep-value'),
        object=delete(),
        not_there=is_replaced_by('also-not-there')
    )


class Bar(MorpheusDict):
    __schema__ = Schema(
        object=write('object/subobject/deep-value', 1),
    )


class Woo(MorpheusDict):
    __schema__ = Schema(
        object=object,
        test=read('object'),
    )


class Oor(MorpheusDict):
    __schema__ = Schema(
        object=int,
        test=read('object/not/there'),
    )


class TestTranslation(unittest.TestCase):
    def test_mapping(self):
        data = {
            'id': 1000,
            'status': 'PREVIOUS',
            'object': {
                'subobject': {
                    'deep-value': 42
                }
            }
        }
        expected = {
            'id': 1000,
            'status': 'NEW',
            'answer': 42
        }
        translated = Foo(data)
        self.assertDictEqual(translated, expected)

    def test_write(self):
        expected = {
            'object': {
                'subobject': {
                    'deep-value': 1,
                },
            },
        }
        self.assertDictEqual(Bar(), expected)

    def test_read_root(self):
        '''Test reading from a single root entry'''
        expected = {
            'object': 1,
            'test': 1,
        }
        self.assertDictEqual(Woo({'object': 1}), expected)

    def test_read_out_of_range(self):
        '''Test reading from a path that is not there'''
        expected = {
            'object': 1,
        }
        self.assertDictEqual(Oor({'object': 1}), expected)


if __name__ == '__main__':
    unittest.main()
