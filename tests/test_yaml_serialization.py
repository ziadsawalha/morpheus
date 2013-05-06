# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

try:
    import yaml
    YAML_INSTALLED = True
except ImportError:
    YAML_INSTALLED = False

from morpheus import MorpheusDict
from morpheus.dict import register_yaml_representer


@unittest.skipUnless(YAML_INSTALLED,
                     reason="Skipping because JSON is not installed")
class TestMorpheusDictYAMLSerialization(unittest.TestCase):
    def test_yaml_serialization_safe(self):
        data = {'key': {'a': 1}}
        md = MorpheusDict(data)
        serialized = yaml.safe_dump(md, default_flow_style=False)
        self.assertEqual(serialized, 'key:\n  a: 1\n')

    def test_yaml_serialization(self):
        data = {'key': {'a': 1}}
        md = MorpheusDict(data)
        serialized = yaml.dump(md, default_flow_style=False)
        self.assertEqual(serialized, 'key:\n  a: 1\n')

    def test_yaml_representer(self):
        class SomeClass(dict):
            pass
        register_yaml_representer(SomeClass)
        data = SomeClass({'key': {'a': 1}})
        self.assertDictEqual(dict(data), {'key': {'a': 1}})

        result = yaml.safe_dump(SomeClass(data), default_flow_style=False)
        self.assertEqual(result, 'key:\n  a: 1\n')


if __name__ == '__main__':
    unittest.main()
