#!/usr/bin/env python3
import os

class SparseMatrix:
    def __init__(self, filepath=None, num_rows=None, num_cols=None):
        self.rows = 0
        self.cols = 0
        self.data = []
        self.indices = []
        self.indptr = [0]
        if filepath:
            self._load_from_file(filepath)
        elif num_rows is not None and num_cols is not None:
            self.rows = num_rows
            self.cols = num_cols

    def _load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) < 2 or not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                raise ValueError("Invalid file format")
            self.rows = int(lines[0][5:])
            self.cols = int(lines[1][5:])
            for line in lines[2:]:
                if not (line.startswith('(') and line.endswith(')')):
                    raise ValueError("Malformed entry")
                parts = line[1:-1].split(',')
                row = int(parts[0].strip())
                col = int(parts[1].strip())
                value = int(parts[2].strip())
                self._insert_entry(row, col, value)

    def _insert_entry(self, row, col, value):
        if row >= self.rows or col >= self.cols:
            raise IndexError("Index out of bounds")
        if value == 0:
            return
        start = self.indptr[row]
        end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
        pos = start
        while pos < end and self.indices[pos] < col:
            pos += 1
        if pos < end and self.indices[pos] == col:
            self.data[pos] = value
        else:
            self.data.insert(pos, value)
            self.indices.insert(pos, col)
            for r in range(row+1, len(self.indptr)):
                self.indptr[r] += 1
            if len(self.indptr) < self.rows + 1:
                self.indptr += [self.indptr[-1]] * (self.rows + 1 - len(self.indptr))

    def get_element(self, row, col):
        if row >= self.rows or col >= self.cols:
            raise IndexError("Index out of bounds")
        start = self.indptr[row]
        end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
        for i in range(start, end):
            if self.indices[i] == col:
                return self.data[i]
        return 0

    def set_element(self, row, col, value):
        self._insert_entry(row, col, value)

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension mismatch")
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for row in range(self.rows):
            entries = {}
            start = self.indptr[row]
            end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
            for i in range(start, end):
                entries[self.indices[i]] = self.data[i]
            start = other.indptr[row]
            end = other.indptr[row+1] if row+1 < len(other.indptr) else len(other.data)
            for i in range(start, end):
                col = other.indices[i]
                entries[col] = entries.get(col, 0) + other.data[i]
            for col, value in entries.items():
                if value != 0:
                    result._insert_entry(row, col, value)
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Dimension mismatch")
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        for row in range(self.rows):
            self_start = self.indptr[row]
            self_end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
            for i in range(self_start, self_end):
                col = self.indices[i]
                val = self.data[i]
                other_start = other.indptr[col]
                other_end = other.indptr[col+1] if col+1 < len(other.indptr) else len(other.data)
                for j in range(other_start, other_end):
                    result.set_element(row, other.indices[j], result.get_element(row, other.indices[j]) + val * other.data[j])
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension mismatch")
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        for row in range(self.rows):
            entries = {}
            start = self.indptr[row]
            end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
            for i in range(start, end):
                entries[self.indices[i]] = self.data[i]
            start = other.indptr[row]
            end = other.indptr[row+1] if row+1 < len(other.indptr) else len(other.data)
            for i in range(start, end):
                col = other.indices[i]
                entries[col] = entries.get(col, 0) - other.data[i]
            for col, value in entries.items():
                if value != 0:
                    result._insert_entry(row, col, value)
        return result

    def save_to_file(self, filepath):
        with open(filepath, 'w') as f:
            f.write(f"rows={self.rows}\ncols={self.cols}\n")
            for row in range(self.rows):
                start = self.indptr[row]
                end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
                for i in range(start, end):
                    f.write(f"({row}, {self.indices[i]}, {self.data[i]})\n")

def get_valid_filepath(prompt):
    while True:
        filepath = input(prompt).strip()
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            continue
        return filepath

def print_matrix_preview(matrix, limit=5):
    print("\nMatrix Preview:")
    count = 0
    for i in range(matrix.rows):
        start = matrix.indptr[i]
        end = matrix.indptr[i+1] if i+1 < len(matrix.indptr) else len(matrix.data)
        for j in range(start, end):
            if count >= limit:
                print(f"... {len(matrix.data)-limit} more elements")
                return
            print(f"({i}, {matrix.indices[j]}, {matrix.data[j]})")
            count += 1

def main():
    print("=== Sparse Matrix Operations ===")
    print("1. Add\n2. Subtract\n3. Multiply\n4. Exit")
    while True:
        try:
            choice = input("\nEnter operation (1-4): ").strip()
            if choice == '4':
                break
            if choice not in ('1', '2', '3'):
                raise ValueError("Invalid choice")
            
            file1 = get_valid_filepath("Enter first matrix file: ")
            mat1 = SparseMatrix(file1)
            print(f"Loaded: {mat1.rows}x{mat1.cols}")
            print_matrix_preview(mat1)
            
            file2 = get_valid_filepath("Enter second matrix file: ")
            mat2 = SparseMatrix(file2)
            print(f"Loaded: {mat2.rows}x{mat2.cols}")
            print_matrix_preview(mat2)
            
            output_file = input("Enter output file: ").strip()
            
            if choice == '1':
                result = mat1.add(mat2)
            elif choice == '2':
                result = mat1.subtract(mat2)
            elif choice == '3':
                result = mat1.multiply(mat2)
                
            result.save_to_file(output_file)
            print(f"Saved to {output_file}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
