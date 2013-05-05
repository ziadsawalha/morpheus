# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict
from morpheus.operations import as_of


class Foo(MorpheusDict):
    __schema__ = dict(
        status=basestring,

        # Things we learned we should change or just changed our minds about
        state=as_of(0.7).is_replaced_by('status')
    )


class TestOperations(unittest.TestCase):
    def test_is_replaced_by(self):
        obj = Foo(state="ACTIVE")
        self.assertIn('status', obj)
        self.assertNotIn('state', obj)

        expected = dict(status="ACTIVE")
        self.assertEqual(obj, expected)


if __name__ == '__main__':
    unittest.main()
