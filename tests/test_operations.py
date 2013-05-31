# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict, exceptions
from morpheus import operations as ops


class Foo(MorpheusDict):
    __schema__ = dict(
        simple=int,

        status=basestring,
        state=ops.is_replaced_by('status'),

        boolean=ops.is_type(bool),
        chain=ops.as_of(0.7).is_type(int),
    )


class Bar(MorpheusDict):
    __schema__ = dict(
        must=ops.is_required()
    )


class TestOperations(unittest.TestCase):
    '''Test basic operations'''

    def test_is_replaced_by(self):
        obj = Foo(state="ACTIVE")
        self.assertIn('status', obj)
        self.assertNotIn('state', obj)

        expected = dict(status="ACTIVE")
        self.assertEqual(obj, expected)

    def test_is_type(self):
        obj = Foo(boolean=True)
        self.assertIn('boolean', obj)
        self.assertTrue(isinstance(obj['boolean'], bool))

        self.assertRaisesRegexp(exceptions.ValidationError, '', Foo, boolean=8)

    def test_is_required_instantiation(self):
        obj = Bar(must=8)
        self.assertIn('must', obj)
        self.assertEqual(obj['must'], 8)

    def test_is_required_delitem(self):
        obj = Bar(must=8)

        try:
            del obj['must']
            self.assertTrue(False)
        except exceptions.ValidationError:
            pass

    def test_is_required_validation(self):
        self.assertRaisesRegexp(exceptions.ValidationError, '', Bar)

    def test_chaining(self):
        obj = Foo(chain=12)
        self.assertIn('chain', obj)
        self.assertEqual(obj['chain'], 12)


if __name__ == '__main__':
    unittest.main()
