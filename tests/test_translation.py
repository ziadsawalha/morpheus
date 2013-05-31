# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict, Schema
from morpheus.operations import read, delete, translate, is_replaced_by


class Foo(MorpheusDict):
    __schema__ = Schema(
        id=int,
        status=translate({'PREVIOUS': 'NEW'}),
        answer=read('object/subobject/deep-value'),
        object=delete(),
        not_there=is_replaced_by('also-not-there')
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


if __name__ == '__main__':
    unittest.main()
