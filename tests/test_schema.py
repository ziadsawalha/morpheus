# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict as dict  # pylint: disable=W0622
from morpheus import Schema, exceptions
from morpheus.operations import is_required


class TestAllowed(unittest.TestCase):
    def test_allowed_combines(self):
        class Foo(dict):
            __schema__ = ['id']
            allowed = ['this-also']
        result = list(Foo.allowed)
        result.sort()
        self.assertListEqual(result, ['id', 'this-also'])

    def test_required_combines(self):
        class Foo(dict):
            __schema__ = Schema(
                id=is_required()
            )
            required = ['this-also']
        result = list(Foo.required)
        result.sort()
        self.assertListEqual(result, ['id', 'this-also'])


class TestSchema(unittest.TestCase):

    def test_none_schema(self):
        class Foo(dict):
            __schema__ = None
        result = Foo({'id': 1})
        self.assertDictEqual(result, {'id': 1})

    def test_empty_dict_schema(self):
        class Foo(dict):
            __schema__ = {}
        result = Foo({'id': 1})
        self.assertDictEqual(result, {'id': 1})

    def test_empty_list_schema(self):
        class Foo(dict):
            __schema__ = []
        result = Foo({'id': 1})
        self.assertDictEqual(result, {'id': 1})

    def test_bad_rule(self):
        class Foo(dict):
            __schema__ = dict(
                bad=is_required().made_up(),
            )
        self.assertRaises(SyntaxError, Foo)


if __name__ == '__main__':
    unittest.main()
