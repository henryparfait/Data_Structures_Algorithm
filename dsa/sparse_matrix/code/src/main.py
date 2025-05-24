from sparse_matrix import SparseMatrix

def main():
    print("Sparse Matrix Operations")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    
    while True:
        try:
            choice = input("Enter operation (1/2/3): ").strip()
            if choice not in {'1', '2', '3'}:
                raise ValueError("Invalid choice")
            
            file1 = input("Data_Structure_Algorithm/dsa/sparse_matrix/sample_inputs/easy_sample1.txt").strip()
            file2 = input("Data_Structure_Algorithm/dsa/sparse_matrix/sample_inputs/easy_sample2.txt").strip()
            output_file = input("Data_Structure_Algorithm/dsa/sparse_matrix/sample_inputs/output.txt").strip()
            
            mat1 = SparseMatrix(Data_Structure_Algorithm/dsa/sparse_matrix/sample_inputs/easy_sample1.txt)
            mat2 = SparseMatrix(Data_Structure_Algorithm/dsa/sparse_matrix/sample_inputs/easy_sample2.txt)
            
            if choice == '1':
                result = mat1.add(mat2)
            elif choice == '2':
                result = mat1.subtract(mat2)
            elif choice == '3':
                result = mat1.multiply(mat2)
            
            result.save_to_file("output.txt")
            print(f"Operation completed. Result saved to {output_file}")
            break
            
        except Exception as e:
            print(f"Error: {str(e)}\nPlease try again.\n")

if __name__ == "__main__":
    main()
