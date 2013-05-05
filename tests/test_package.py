import unittest


class TestPackage(unittest.TestCase):
    def test_morpheus_exists(self):
        try:
            import morpheus  # pylint: disable=W0612, F0401
        except ImportError:
            self.assertTrue(False, msg="Package 'morpheus' does not exist")


if __name__ == "__main__":
    unittest.main()
