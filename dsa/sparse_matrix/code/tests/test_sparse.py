import unittest
import os
from ..src.sparse_matrix import SparseMatrix

class TestSparseMatrix(unittest.TestCase):
    def setUp(self):
        # Create test files
        with open("easy_sample1.txt", 'w') as f:
            f.write("rows=2\ncols=2\n(0, 0, 1)\n(1, 1, 1)\n")
        
        with open("easy_sample2.txt", 'w') as f:
            f.write("rows=2\ncols=2\n(0, 1, 2)\n(1, 0, 2)\n")
    
    def tearDown(self):
        # Clean up test files
        os.remove("easy_sample1.txt")
        os.remove("easy_sample2.txt")
    
    def test_loading(self):
        mat = SparseMatrix("sample_inputs/easy_sample1.txt")
        self.assertEqual(mat.get_element(0, 0), 1)
        self.assertEqual(mat.get_element(1, 1), 1)
        self.assertEqual(mat.get_element(0, 1), 0)
    
    def test_addition(self):
        mat1 = SparseMatrix("easy_sample1.txt")
        mat2 = SparseMatrix("easy_sample2.txt")
        result = mat1.add(mat2)
        self.assertEqual(result.get_element(0, 0), 1)
        self.assertEqual(result.get_element(0, 1), 2)
        self.assertEqual(result.get_element(1, 0), 2)
        self.assertEqual(result.get_element(1, 1), 1)
    
    def test_multiplication(self):
        mat1 = SparseMatrix("easy_sample1.txt")
        mat2 = SparseMatrix("easy_sample2.txt")
        result = mat1.multiply(mat2)
        self.assertEqual(result.get_element(0, 0), 0)
        self.assertEqual(result.get_element(0, 1), 2)
        self.assertEqual(result.get_element(1, 0), 2)
        self.assertEqual(result.get_element(1, 1), 0)

if __name__ == "__main__":
    unittest.main()
