'''
Experiment No. 7 : Write a python program for MAGIC SQUARE.
                   A magic square is an n*n matrix of the integers 1 to (n^2) such that the sum of each row,
                   column and diagonals the same.
                   The figure given below is an example of the magic square for case n=5. In this example
                   the common sum is 65.

                   9  |   3  |  22  |  16  |  15  |
                   2  |  21  |  20  |  14  |   8  |
                  25  |  19  |  13  |   7  |   1  |
                  18  |  12  |   6  |   5  |  24  |
                  11  |  10  |   4  |  23  |  17  |

Conditions for placing the values in the matrix in appropriate manner (CIRCULAR ARRAY) :

   1. The position of next number is calculated by decrementing row number of previous number by 1, and incrementing
      the column number of previous number by 1. At any time, if the calculated row position becomes -1, it will wrap
      around to n-1. Similarly, if the calculated column position becomes n, it will wrap around to 0.

   2. If the magic square already contains a number at the calculated position, calculated column position will be
      decremented by 2, and calculated row position will be incremented by 1.

   3. If the calculated row position is -1 & calculated column position is n, the new position would be: (0, n-2).
'''

#<------------------------------------------------------------------------------------------------->

# A function to generate odd sized magic squares
def generate_Magic_Square(size):
    magic_square=[[0 for x in range(size)] for y in range(size)]

    # Initializing first position of matrix
    i=int(size/2)
    j=size-1

    # Fill the magic square by placing values at appropriate position
    for num in range(1, size*size + 1): # range(start, end, step)
        magic_square[i][j] = num
        new_i, new_j = (i - 1) % size, (j + 1) % size
        
        # Check if the next cell is already filled or out of bounds
        if magic_square[new_i][new_j] != 0:
            new_i = (i + 1) % size  # Move down
            new_j = j  # Stay in the same column
        
        i, j = new_i, new_j


    # Printing of magic square
    sum=size*(size*size+1)/2
    print("Sum of each row or column is : ",sum)
    print("Magic Square of size",size,"*",size,"is : \n")

    for i in range(0,size):
        for j in range(0,size):
            print(' %2d ' % (magic_square[i][j]),end=' | ')

            # To display magic square in matrix form
            if j==size-1:
                print()

#<------------------------------------------------------------------------------------------------->

while True:
    n=int(input("\nEnter the size of the MAGIC SQUARE : "))
    if n%2==0:
        s=int(input("Please enter an ODD Number (for example - 3,5,7,9,....) : "))
        generate_Magic_Square(s)
    else:
        generate_Magic_Square(n)

    # generate new Magic Square
    a = input("\nDo you want to print Magic Square of some other size (y/N) : ")
    if a=='n' or a=='N' or a==' ' or a=='':
      break

#<------------------------------------------ END OF PROGRAM ----------------------------------------->



#<-------------------------------------------- OUTPUT ----------------------------------------------->

'''
Enter the size of the MAGIC SQUARE : 5
Sum of each row or column is :  65.0
Magic Square of size 5 * 5 is : 

 21  |   3  |  10  |  12  |  19  | 
  2  |   9  |  11  |  18  |  25  | 
  8  |  15  |  17  |  24  |   1  | 
 14  |  16  |  23  |   5  |   7  | 
 20  |  22  |   4  |   6  |  13  | 

Do you want to print Magic Square of some other size (y/N) : y

Enter the size of the MAGIC SQUARE : 7
Sum of each row or column is :  175.0
Magic Square of size 7 * 7 is : 

 42  |  44  |   4  |  13  |  15  |  24  |  33  | 
 43  |   3  |  12  |  21  |  23  |  32  |  41  | 
  2  |  11  |  20  |  22  |  31  |  40  |  49  | 
 10  |  19  |  28  |  30  |  39  |  48  |   1  | 
 18  |  27  |  29  |  38  |  47  |   7  |   9  | 
 26  |  35  |  37  |  46  |   6  |   8  |  17  | 
 34  |  36  |  45  |   5  |  14  |  16  |  25  | 

'''
