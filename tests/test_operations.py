# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus.operations import as_of
from morpheus import MorpheusDict, exceptions


class Foo(MorpheusDict):
    __schema__ = dict(
        status=basestring,

        # Things we learned we should change or just changed our minds about
        state=as_of(0.7).is_replaced_by('status')


class Bar(MorpheusDict):
    __schema__ = dict(
        must=is_required()
    )


class TestOperations(unittest.TestCase):
    def test_is_replaced_by(self):
        obj = Foo(state="ACTIVE")
        self.assertIn('status', obj)
        self.assertNotIn('state', obj)

        expected = dict(status="ACTIVE")
        self.assertEqual(obj, expected)


    def test_is_required_instantiation(self):
        obj = Bar(must=8)
        self.assertIn('must', obj)
        self.assertEqual(obj['must'], 8)

    def test_is_required_validation(self):
        self.assertRaisesRegexp(exceptions.ValidationError, '', Bar)

if __name__ == '__main__':
    unittest.main()
