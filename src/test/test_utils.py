import os
import sys
import unittest
from loguru import logger
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_folder)
from UI.utils import extract_variables
class TestUtils(unittest.TestCase):
    @logger.catch
    def test_extract_variables(self):
            self.assertEqual(set(extract_variables("assertion x <= y")), set(['x', 'y']))
            self.assertEqual(set(extract_variables("assertion a > b")), set(['a', 'b']))
            self.assertEqual(set(extract_variables("assertion z / x + asdas <= y")), set(['z', 'x', 'asdas', 'y']))
            self.assertEqual(set(extract_variables("assertion p == q")), set(['p', 'q']))
            self.assertEqual(set(extract_variables("assertion x + x < y")), set(['x', 'y']))
            self.assertEqual(set(extract_variables("assertion var_name <= y")), set(['var_name', 'y']))
            self.assertEqual(set(extract_variables("assertion x < x")), set(['x']))
            self.assertEqual(set(extract_variables("assertion x / (y + z) <= a")), set(['x', 'y', 'z', 'a']))

if __name__ == '__main__':
    unittest.main()
