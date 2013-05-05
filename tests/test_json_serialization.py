# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232

from morpheus import MorpheusDict

try:
    import json
    JSON_INSTALLED = True
except ImportError:
    try:
        import simplejson as json
        JSON_INSTALLED = True
    except ImportError:
        JSON_INSTALLED = False
import unittest


@unittest.skipUnless(JSON_INSTALLED,
                     reason="Skipping because JSON is not installed")
class TestMorpheusDictJsonSerialization(unittest.TestCase):
    def test_json_serialization(self):
        data = {'key': 1}
        md = MorpheusDict(data)
        jsonized = json.dumps(md)
        self.assertEqual(jsonized, '{"key": 1}')


if __name__ == '__main__':
    unittest.main()
