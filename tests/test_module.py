# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

import morpheus


class TestModule(unittest.TestCase):
    def test_MorpheusDict_exists(self):
        '''Check that MorpheusDict exists in the package namespace'''
        self.assertTrue(hasattr(morpheus, 'MorpheusDict'), msg="MorpheusDict "
                        "does not exist in the morpheus package")


if __name__ == "__main__":
    unittest.main()
