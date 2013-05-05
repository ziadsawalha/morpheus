# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

from morpheus import MorpheusDict


class TestMorpheusDict(unittest.TestCase):
    def test_init(self):
        """Check that init works like dict does"""
        data = {'key': 'value', 1: 2}
        md = MorpheusDict(data)
        self.assertDictEqual(md.__dict__(), data)

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
        self.assertDictEqual(md.__dict__(), dict(key='value'))

    def test_empty_kwargs(self):
        template = dict(key='value')
        md = MorpheusDict(template)
        self.assertDictEqual(md.__dict__(), template)

    def test_empty_args_and_kwargs(self):
        md = MorpheusDict()
        self.assertDictEqual(md.__dict__(), {})


if __name__ == '__main__':
    unittest.main()
