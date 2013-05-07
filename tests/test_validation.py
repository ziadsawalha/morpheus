# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict, Schema, Defn, exceptions


class Foo(MorpheusDict):
    __schema__ = Schema(
        id=Defn(int, required=True)
    )


class Bar(MorpheusDict):
    __schema__ = Schema(
        id=Defn(int, required=True),
        name=Defn(basestring, required=True)
    )


class TestRequired(unittest.TestCase):
    '''Test that fields marked as 'required' are required'''

    def test_required_parsing(self):
        obj = Foo(id=1)
        self.assertIn('id', obj)
        self.assertTrue(isinstance(obj['id'], int))

    def test_required_enforced_single(self):
        self.assertRaisesRegexp(exceptions.ValidationError,
                                "Missing required key 'id'", Foo)

    def test_required_enforced_multiple(self):
        regex = r"Missing required keys: (?:name.*id|id.*name)"
        self.assertRaisesRegexp(exceptions.ValidationError, regex, Bar)


if __name__ == '__main__':
    unittest.main()
