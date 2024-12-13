'''
Assignment No. 3 : Write a Python Program to compute following computation on matrices :
                   a)Addition of two matrices
                   b)Subtraction of two matrices
                   c)Multiplication of two matrices
                   d)Transpose of a matix
'''

#<------------------------------------------ START OF PROGRAM ----------------------------------------->

def print_matrix(matrix):
    """
    Prints a matrix in a readable format.
    """
    for row in matrix:
        print(" ".join(map(str, row)))  # Join elements of the row with space and print
    print()

#<------------------------------------------------------------------------------------------------->

def add_matrices(A, B):
    """
    Adds two matrices A and B.
    Assumes A and B have the same dimensions.
    """
    rows = len(A)       # Number of rows in matrix A
    cols = len(A[0])    # Number of columns in matrix A
    C = [[0] * cols for _ in range(rows)]  # Initialize result matrix C with zeros
    
    for i in range(rows):
        for j in range(cols):
            C[i][j] = A[i][j] + B[i][j]  # Element-wise addition
    
    return C

#<------------------------------------------------------------------------------------------------->

def subtract_matrices(A, B):
    """
    Subtracts matrix B from matrix A.
    Assumes A and B have the same dimensions.
    """
    rows = len(A)       # Number of rows in matrix A
    cols = len(A[0])    # Number of columns in matrix A
    C = [[0] * cols for _ in range(rows)]  # Initialize result matrix C with zeros
    
    for i in range(rows):
        for j in range(cols):
            C[i][j] = A[i][j] - B[i][j]  # Element-wise subtraction
    
    return C

#<------------------------------------------------------------------------------------------------->

def multiply_matrices(A, B):
    """
    Multiplies two matrices A and B.
    Assumes the number of columns in A equals the number of rows in B.
    """
    rows_A = len(A)         # Number of rows in matrix A
    cols_A = len(A[0])      # Number of columns in matrix A
    rows_B = len(B)         # Number of rows in matrix B
    cols_B = len(B[0])      # Number of columns in matrix B
    
    if cols_A != rows_B:
        raise ValueError("Incompatible matrices for multiplication")  # Check for compatibility
    
    # Initialize result matrix C with zeros
    C = [[0] * cols_B for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]  # Matrix multiplication logic
    
    return C

#<------------------------------------------------------------------------------------------------->

def transpose_matrix(A):
    """
    Computes the transpose of matrix A.
    """
    rows = len(A)         # Number of rows in matrix A
    cols = len(A[0])      # Number of columns in matrix A
    
    # Initialize result matrix B with zeros
    B = [[0] * rows for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            B[j][i] = A[i][j]  # Transpose operation
    
    return B

#<------------------------------------------------------------------------------------------------->

# Example matrices
A = [
    [1, 2, 3],
    [4, 5, 6]
]
B = [
    [7, 8, 9],
    [10, 11, 12]
]

print("Matrix A:")
print_matrix(A)  # Print matrix A
print("Matrix B:")
print_matrix(B)  # Print matrix B

# Perform matrix operations
print("Addition of A and B:")
C_add = add_matrices(A, B)
print_matrix(C_add)  # Print result of addition

print("Subtraction of A from B:")
C_sub = subtract_matrices(A, B)
print_matrix(C_sub)  # Print result of subtraction

print("Multiplication of A and B:")
# To demonstrate multiplication, transpose B to make dimensions compatible
B_T = transpose_matrix(B)
C_mul = multiply_matrices(A, B_T)
print_matrix(C_mul)  # Print result of multiplication

print("Transpose of A:")
C_trans = transpose_matrix(A)
print_matrix(C_trans)  # Print result of transpose


#<------------------------------------------ END OF PROGRAM ----------------------------------------->



#<-------------------------------------------- OUTPUT ----------------------------------------------->

'''

Matrix A:
1 2 3
4 5 6

Matrix B:
7 8 9
10 11 12

Addition of A and B:
8 10 12
14 16 18

Subtraction of A from B:
-6 -6 -6
-6 -6 -6

Multiplication of A and B:
50 68
122 167

Transpose of A:
1 4
2 5
3 6

'''

