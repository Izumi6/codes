'''
Assignemt 4.b: Write a Python program to store roll numbers of student array who attended training pro-gram in sorted order. 
               Write function for searching whether particular student attended training program or not, using Binary search and Fibonacci search
'''

#<------------------------------------------ START OF PROGRAM ----------------------------------------->

# Function to perform binary search without bisect
def binary_search(arr, roll_number):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Calculate middle index
        
        if arr[mid] == roll_number:
            return True  # Found the roll number
        elif arr[mid] < roll_number:
            left = mid + 1  # Search in the right subarray
        else:
            right = mid - 1  # Search in the left subarray

    return False  # Roll number not found

#<------------------------------------------------------------------------------------------------->

# Function to perform Fibonacci search
def fibonacci_search(arr, roll_number):
    n = len(arr)
    fib_m_2 = 0  # Fibonacci number F(m-2)
    fib_m_1 = 1  # Fibonacci number F(m-1)
    fib_m = fib_m_1 + fib_m_2  # Fibonacci number F(m)

    # Find the smallest Fibonacci number greater than or equal to n
    while fib_m < n:
        fib_m_2 = fib_m_1
        fib_m_1 = fib_m
        fib_m = fib_m_1 + fib_m_2

    offset = -1  # Initial offset

    # Perform the Fibonacci search
    while fib_m > 1:
        i = min(offset + fib_m_2, n - 1)  # Calculate index to compare

        if arr[i] < roll_number:
            # Roll number is in the right subarray
            fib_m = fib_m_1
            fib_m_1 = fib_m_2
            fib_m_2 = fib_m - fib_m_1
            offset = i  # Move the offset to the right

        elif arr[i] > roll_number:
            # Roll number is in the left subarray
            fib_m = fib_m_2
            fib_m_1 -= fib_m_2
            fib_m_2 = fib_m - fib_m_1

        else:
            # Roll number found
            return True

    # Check the last element
    if fib_m_1 and offset + 1 < n and arr[offset + 1] == roll_number:
        return True

    return False

#<------------------------------------------------------------------------------------------------->

# Generate a list of roll numbers in sorted order
def generate_sorted_roll_numbers(n):
    return list(range(1000, 1000 + n))  # Sorted roll numbers from 1000 to 1000 + n

#<------------------------------------------------------------------------------------------------->

# Main function to demonstrate the search methods
def main():
    n = 10  # Number of students
    roll_numbers = generate_sorted_roll_numbers(n)
    print("Sorted roll numbers of students who attended the training program:", roll_numbers)

    roll_number_to_search = int(input("Enter the roll number to search: "))

    # Binary Search
    found = binary_search(roll_numbers, roll_number_to_search)
    print(f"Binary Search: Roll number {roll_number_to_search} {'found' if found else 'not found'}")

    # Fibonacci Search
    found = fibonacci_search(roll_numbers, roll_number_to_search)
    print(f"Fibonacci Search: Roll number {roll_number_to_search} {'found' if found else 'not found'}")

#<------------------------------------------------------------------------------------------------->

main()

#<------------------------------------------ END OF PROGRAM ----------------------------------------->



#<-------------------------------------------- OUTPUT ----------------------------------------------->

'''
Sorted roll numbers of students who attended the training program: [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]
Enter the roll number to search: 1005
Binary Search: Roll number 1005 found
Fibonacci Search: Roll number 1005 found

Enter the roll number to search: 1015
Binary Search: Roll number 1015 not found
Fibonacci Search: Roll number 1015 not found

'''

