# pylint: disable=C0103,C0111,R0903,R0904,W0212,W0232
import unittest

import morpheus


class TestModule(unittest.TestCase):
    def test_MorpheusDict_exists(self):
        '''Check that MorpheusDict exists in the package namespace'''
        self.assertTrue(hasattr(morpheus, 'MorpheusDict'), msg="MorpheusDict "
                        "does not exist in the morpheus package")

    def test_MorpheusDict_class(self):
        '''MorpheusDict in the package namespace should be the right class'''
        self.assertEqual(getattr(morpheus, 'MorpheusDict').__name__,
                         'MorpheusDict',
                         msg="MorpheusDict in the morpheus package is not a "
                         "MorpheusDict")

    def test_MorpheusDict_is_a_dict(self):
        '''MorpheusDict should look like a dict'''
        self.assertTrue(issubclass(dict, morpheus.MorpheusDict))
        self.assertTrue(isinstance({}, morpheus.MorpheusDict),
                        msg="MorpheusDict is not being seen as a dict")
        # TODO: assertDictEqual checks if isinstance(, dict) and fails
        # self.assertTrue(isinstance(morpheus.MorpheusDict(), dict))
        self.assertEqual(morpheus.MorpheusDict(test=1)['test'], 1)

    def test_operations_exists(self):
        '''Check that operations exists in the package namespace'''
        self.assertTrue(hasattr(morpheus, 'operations'), msg="'operations' "
                        "does not exist in the morpheus package")

    def test_SchemaOp_exists(self):
        '''Check that SchemaOp exists in the package namespace'''
        self.assertTrue(hasattr(morpheus.operations, 'SchemaOp'),
                        msg="SchemaOp does not exist in the "
                        "morpheus.operations package")

    def test_Schema_exists(self):
        '''Check that Schema exists in the package namespace'''
        self.assertTrue(hasattr(morpheus, 'Schema'), msg="'Schema' does not "
                        "exist in the morpheus package")


if __name__ == "__main__":
    unittest.main()
