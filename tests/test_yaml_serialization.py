# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

try:
    import yaml
    YAML_INSTALLED = True
except ImportError:
    YAML_INSTALLED = False

from morpheus import MorpheusDict


@unittest.skipUnless(YAML_INSTALLED,
                     reason="Skipping because JSON is not installed")
class TestMorpheusDictYAMLSerialization(unittest.TestCase):
    def test_yaml_serialization(self):
        data = {'key': {'a': 1}}
        md = MorpheusDict(data)
        serialized = yaml.safe_dump(md, default_flow_style=False)
        self.assertEqual(serialized, 'key:\n  a: 1\n')

        serialized = yaml.dump(md, default_flow_style=False)
        self.assertEqual(serialized, 'key:\n  a: 1\n')


if __name__ == '__main__':
    unittest.main()
