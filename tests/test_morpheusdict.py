# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus.dict import get_class_vars
from morpheus import MorpheusDict, Defn


class TestMorpheusDict(unittest.TestCase):
    def test_init(self):
        """Check that init works like dict does"""
        data = {'key': 'value', 1: 2}
        md = MorpheusDict(data)
        self.assertDictEqual(md, data)

    def test_basic_operations(self):
        """Test basic dictionary-type operations"""
        md = MorpheusDict(key='value')
        self.assertIn('key', md)
        self.assertEqual(md['key'], 'value')

        md['new'] = 2
        self.assertIn('new', md)
        self.assertEqual(md['new'], 2)
        self.assertEqual(len(md), 2)

        del md['new']
        self.assertNotIn('new', md)

    def test_empty_args(self):
        md = MorpheusDict(key='value')
        self.assertDictEqual(md, dict(key='value'))

    def test_empty_kwargs(self):
        template = dict(key='value')
        md = MorpheusDict(template)
        self.assertDictEqual(md, template)

    def test_empty_args_and_kwargs(self):
        md = MorpheusDict()
        self.assertDictEqual(md, {})

    def test_get_class_vars_empty(self):
        self.assertEqual(get_class_vars(dict), [])

    def test_get_class_vars(self):
        class MDTest():
            an_id = int
        self.assertEqual(get_class_vars(MDTest), ['an_id'])


class MDSubclass(MorpheusDict):
    '''Used for subclass trsting'''
    __schema__ = ['id']


class TestMorpheusDictSubclass(unittest.TestCase):
    def test_setitem(self):
        md = MDSubclass(id=1)
        expect = "'not_id' is not permitted on an object of type 'MDSubclass'"
        self.assertRaisesRegexp(AttributeError, expect, md.__setitem__,
                                "not_id", 1)


if __name__ == '__main__':
    unittest.main()
