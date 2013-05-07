# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict as dict  # pylint: disable=W0622
from morpheus import Schema, exceptions


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


class Yee(dict):
    class __schema__:
        id = int
        name = basestring
        status = basestring


class TestInstantiation(unittest.TestCase):
    '''Test that we can define schema using the four methods above'''
    def test_schema_as_list(self):
        md = Foo(id=1)
        self.assertEqual(md['id'], 1)

    def test_schema_as_dict(self):
        md = Bar(id=1)
        self.assertEqual(md['id'], 1)

    def test_schema_as_Schema(self):
        md = Woo(id=1)
        self.assertEqual(md['id'], 1)

    def test_schema_as_class(self):
        md = Yee(id=1)
        self.assertEqual(md['id'], 1)

    def test_invalid_schema(self):
        try:
            class Womp(dict):
                ''' Fail '''
                __schema__ = 2
            self.assertTrue(False, "Bad schema did not raise a TypeError")
        except TypeError:
            pass


class TestSimpleValidation(unittest.TestCase):
    def test_fail_on_bad_field(self):
        self.assertRaisesRegexp(exceptions.ValidationError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Foo'",
                                Foo,
                                sneaky='git blame someone for this!')

    def test_positive(self):
        obj = Foo(id=1, name="John", state="Gone fishing")
        expected = dict(id=1, name="John", state="Gone fishing")
        self.assertEqual(obj, expected)

    def test_schema_as_dict(self):
        self.assertRaisesRegexp(exceptions.ValidationError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Bar'",
                                Bar,
                                sneaky='git blame someone for this!')

    def test_schema_as_class(self):
        self.assertRaisesRegexp(exceptions.ValidationError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Woo'",
                                Woo,
                                sneaky='git blame someone for this!')

    def test_schema_as_subclass(self):
        self.assertRaisesRegexp(exceptions.ValidationError,
                                "'sneaky' is not a permitted attribute for a "
                                "'Yee'",
                                Yee,
                                sneaky='git blame someone for this!')


class TestOtherValidation(unittest.TestCase):
    def test_fail_on_multiples(self):
        self.assertRaisesRegexp(exceptions.ValidationError,
                                "second, first are not permitted attributes "
                                "for a 'Foo'",
                                Foo,
                                first="error",
                                second="mistake")


if __name__ == '__main__':
    unittest.main()
