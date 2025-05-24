#Sparse Matrix Operations



#📝 Overview


This repository contains a complete implementation of sparse matrix operations in pure Python, adhering to strict academic guidelines. The solution supports loading sparse matrices from files, performing addition/subtraction/multiplication, and saving results - all while optimizing for memory and runtime efficiency.

#📂 Repository Structure


dsa/sparse_matrix/
│── /code/
│   │── /src/
│   │   │── sparse_matrix.py   # Core matrix implementation
│   │   │── main.py           # Command-line interface
│   │── /tests/
│   │   │── test_sparse.py    # Unit tests
│── /sample_inputs/           # Example matrices
│   │── easy_sample1.txt      # 3x3 sample matrix
│   │── easy_sample2.txt      # 3x3 sample matrix
│   │── large_sample.txt      # Real-world scale matrix
│── README.md                 # This file


#How It Works


##🔢 Input File Format
Matrix files must follow this exact format:

rows=[N]
cols=[M]
(row, col, value)
(row, col, value)

#✨ Features

Memory Efficient: Uses CSR (Compressed Sparse Row) format

Full Validation: Strict checking of input file formatting

Three Operations:

Matrix Addition

Matrix Subtraction

Matrix Multiplication

Running the Program
Navigate to the code directory:

bash
cd dsa/sparse_matrix/code/src
Execute the main program:

bash
python main.py
Follow the prompts:

Sparse Matrix Operations
1. Add
2. Subtract
3. Multiply
Enter operation (1/2/3): 1
Path to first matrix: ../../sample_inputs/easy_sample1.txt
Path to second matrix: ../../sample_inputs/easy_sample2.txt
Output file path: result.txt
Running Tests
bash
python -m unittest ../tests/test_sparse.py


#📜 Academic Compliance


✅ No external libraries used

✅ Complete from-scratch implementation

✅ Proper error handling

✅ Full documentation

✅ Unit tests included


#📝 Sample Walkthrough


Create input files in /sample_inputs/

Run operations via the menu interface

Verify results:

python
result = SparseMatrix("result.txt")
print(result.get_element(0, 0))  # Check specific values


#🤝 Contributing


While this is an academic assignment, suggestions for improvement are welcome through issues. Please note this implementation must remain library-free.

#📄 License

Academic Use Only - All rights reserved by the course instructors.
