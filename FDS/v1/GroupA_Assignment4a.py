'''
Assignment 4.a:	Write a Python program to store roll numbers of student in array who attended training pro-gram in random order. 
                Write function for searching whether particular student attended training program or not, using Linear search and Sentinel search.
'''

#<------------------------------------------ START OF PROGRAM ----------------------------------------->

import random

# Function to perform linear search
def linear_search(arr, roll_number):
    for number in arr:
        if number == roll_number:
            return True
    return False

#<------------------------------------------------------------------------------------------------->

# Function to perform sentinel search
def sentinel_search(arr, roll_number):
    # Save the last element and set sentinel
    last = arr[-1]
    arr[-1] = roll_number
    
    i = 0
    while arr[i] != roll_number:
        i += 1
    
    # Restore the last element
    arr[-1] = last
    # Check if we found the roll number
    return i < len(arr) or last == roll_number

#<------------------------------------------------------------------------------------------------->

# Generate a list of roll numbers in random order
def generate_random_roll_numbers(n):
    return random.sample(range(1000, 1000 + n), n)  # Unique roll numbers between 1000 and 1000 + n

#<------------------------------------------------------------------------------------------------->

# Main function to demonstrate the search methods
def main():
    n = 10  # Number of students
    roll_numbers = generate_random_roll_numbers(n)
    print("Roll numbers of students who attended the training program:", roll_numbers)

    roll_number_to_search = int(input("Enter the roll number to search: "))

    # Linear Search
    found = linear_search(roll_numbers, roll_number_to_search)
    print(f"Linear Search: Roll number {roll_number_to_search} {'found' if found else 'not found'}")

    # Sentinel Search
    found = sentinel_search(roll_numbers, roll_number_to_search)
    print(f"Sentinel Search: Roll number {roll_number_to_search} {'found' if found else 'not found'}")

#<------------------------------------------------------------------------------------------------->

if __name__ == "__main__":
    main()

#<------------------------------------------ END OF PROGRAM ----------------------------------------->



#<-------------------------------------------- OUTPUT ----------------------------------------------->

'''
Roll numbers of students who attended the training program: [1001, 1005, 1008, 1012, 1015, 1020, 1023, 1027, 1030, 1034]
Enter the roll number to search: 1012
Linear Search: Roll number 1012 found
Sentinel Search: Roll number 1012 found

Enter the roll number to search: 1050
Linear Search: Roll number 1050 not found
Sentinel Search: Roll number 1050 not found

'''
