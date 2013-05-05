# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict as dict  # pylint: disable=W0622
from morpheus import Schema


class Foo(dict):
    __schema__ = ['id', 'name', 'state']


class Bar(dict):
    __schema__ = dict(
        id=int,
        name=basestring,
        status=basestring
    )


class Woo(dict):
    __schema__ = Schema(
        id=int,
        name=basestring,
        status=basestring
    )


class TestSimpleValidation(unittest.TestCase):
    def test_fail_on_bad_field(self):
        self.assertRaisesRegexp(AttributeError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Foo'",
                                Foo,
                                sneaky='git blame someone for this!')

    def test_positive(self):
        obj = Foo(id=1, name="John", state="Gone fishing")
        expected = dict(id=1, name="John", state="Gone fishing")
        self.assertEqual(obj, expected)

    def test_schema_as_dict(self):
        self.assertRaisesRegexp(AttributeError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Bar'",
                                Bar,
                                sneaky='git blame someone for this!')

    def test_schema_as_class(self):
        self.assertRaisesRegexp(AttributeError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Woo'",
                                Woo,
                                sneaky='git blame someone for this!')


if __name__ == '__main__':
    unittest.main()
