class SparseMatrix:
    def __init__(self, filepath=None, num_rows=None, num_cols=None):
        self.rows = 0
        self.cols = 0
        self.data = []
        self.indices = []
        self.indptr = [0]  # CSR format components
        
        if filepath:
            self._load_from_file(filepath)
        elif num_rows is not None and num_cols is not None:
            self.rows = num_rows
            self.cols = num_cols
    
    def _load_from_file(self, filepath):
        """Load matrix from file with strict format validation"""
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            
            if len(lines) < 2 or not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                raise ValueError("Invalid file format: missing dimensions")
            
            try:
                self.rows = int(lines[0][5:])
                self.cols = int(lines[1][5:])
            except:
                raise ValueError("Invalid dimension format")
            
            for line in lines[2:]:
                if not (line.startswith('(') and line.endswith(')')):
                    raise ValueError(f"Invalid entry format: {line}")
                
                try:
                    parts = line[1:-1].split(',')
                    if len(parts) != 3:
                        raise ValueError
                    row = int(parts[0].strip())
                    col = int(parts[1].strip())
                    value = int(parts[2].strip())
                except:
                    raise ValueError(f"Malformed entry: {line}")
                
                self._insert_entry(row, col, value)
    
    def _insert_entry(self, row, col, value):
        """Insert entry in sorted CSR format"""
        if row >= self.rows or col >= self.cols:
            raise IndexError("Matrix index out of bounds")
        
        if value == 0:
            return  # Don't store zeros
        
        # Find insertion point for column-major order
        start = self.indptr[row]
        end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
        pos = start
        while pos < end and self.indices[pos] < col:
            pos += 1
        
        if pos < end and self.indices[pos] == col:
            self.data[pos] = value  # Update existing
        else:
            # Insert new entry
            self.data.insert(pos, value)
            self.indices.insert(pos, col)
            # Update indptr for subsequent rows
            for r in range(row+1, len(self.indptr)):
                self.indptr[r] += 1
            if len(self.indptr) < self.rows + 1:
                self.indptr += [self.indptr[-1]] * (self.rows + 1 - len(self.indptr))
    
    def get_element(self, row, col):
        """Get value at (row, col)"""
        if row >= self.rows or col >= self.cols:
            raise IndexError("Matrix index out of bounds")
        
        # Binary search would be better for large matrices
        start = self.indptr[row]
        end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
        for i in range(start, end):
            if self.indices[i] == col:
                return self.data[i]
        return 0
    
    def set_element(self, row, col, value):
        """Set value at (row, col)"""
        self._insert_entry(row, col, value)
    
    def add(self, other):
        """Add two sparse matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        for row in range(self.rows):
            # Collect entries from both matrices
            entries = {}
            
            # Add entries from self
            start = self.indptr[row]
            end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
            for i in range(start, end):
                col = self.indices[i]
                entries[col] = self.data[i]
            
            # Add entries from other
            start = other.indptr[row]
            end = other.indptr[row+1] if row+1 < len(other.indptr) else len(other.data)
            for i in range(start, end):
                col = other.indices[i]
                entries[col] = entries.get(col, 0) + other.data[i]
            
            # Insert non-zero results
            for col, value in entries.items():
                if value != 0:
                    result._insert_entry(row, col, value)
        
        return result
    
    def subtract(self, other):
        """Subtract two sparse matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        for row in range(self.rows):
            entries = {}
            
            # Add self's entries
            start = self.indptr[row]
            end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
            for i in range(start, end):
                col = self.indices[i]
                entries[col] = self.data[i]
            
            # Subtract other's entries
            start = other.indptr[row]
            end = other.indptr[row+1] if row+1 < len(other.indptr) else len(other.data)
            for i in range(start, end):
                col = other.indices[i]
                entries[col] = entries.get(col, 0) - other.data[i]
            
            # Store non-zero results
            for col, value in entries.items():
                if value != 0:
                    result._insert_entry(row, col, value)
        
        return result
    
    def multiply(self, other):
        """Multiply two sparse matrices"""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        
        for row in range(self.rows):
            # Get non-zero columns in current row of self
            self_start = self.indptr[row]
            self_end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
            
            for i in range(self_start, self_end):
                col = self.indices[i]
                value = self.data[i]
                
                # Multiply with corresponding row in other
                other_start = other.indptr[col]
                other_end = other.indptr[col+1] if col+1 < len(other.indptr) else len(other.data)
                
                for j in range(other_start, other_end):
                    other_col = other.indices[j]
                    product = value * other.data[j]
                    
                    # Accumulate product
                    current = result.get_element(row, other_col)
                    result.set_element(row, other_col, current + product)
        
        return result
    
    def save_to_file(self, filepath):
        """Save matrix to file in assignment format"""
        with open(filepath, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for row in range(self.rows):
                start = self.indptr[row]
                end = self.indptr[row+1] if row+1 < len(self.indptr) else len(self.data)
                for i in range(start, end):
                    f.write(f"({row}, {self.indices[i]}, {self.data[i]})\n")
