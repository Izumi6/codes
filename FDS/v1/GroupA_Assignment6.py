'''
Assignment 6: Write a python program to store first year percentage of students in array.
                    Write function for sorting array of floating point numbers in ascending order using
                    quick sort and display top five scores.
'''

#<------------------------------------------ START OF PROGRAM ----------------------------------------->

# Function to accept the percentage of the students
def input_percentage():
    perc = []
    number_of_students = int(input("Enter the number of students: "))
    for i in range(number_of_students):
        perc.append(float(input(f"Enter the percentage of Student {i+1}: ")))
    return perc

#<------------------------------------------------------------------------------------------------->

# Function to print the percentages of the students
def print_percentage(perc):
    for p in perc:
        print(p)

#<------------------------------------------------------------------------------------------------->

# Function to perform partitioning for Quick Sort
def percentage_partition(perc, start, end):
    pivot = perc[start]
    lower_bound = start + 1
    upper_bound = end

    while True:
        while lower_bound <= upper_bound and perc[lower_bound] <= pivot:
            lower_bound += 1

        while lower_bound <= upper_bound and perc[upper_bound] >= pivot:
            upper_bound -= 1

        if lower_bound <= upper_bound:
            perc[lower_bound], perc[upper_bound] = perc[upper_bound], perc[lower_bound]
        else:
            break

    perc[start], perc[upper_bound] = perc[upper_bound], perc[start]
    return upper_bound

#<------------------------------------------------------------------------------------------------->

# Function to perform Quick Sort
def quick_sort(perc, start, end):
    if start < end:
        partition_index = percentage_partition(perc, start, end)
        quick_sort(perc, start, partition_index - 1)
        quick_sort(perc, partition_index + 1, end)
    return perc

#<------------------------------------------------------------------------------------------------->

# Function to display the top five percentages
def display_top_five(perc):
    print("Top Five Percentages are:")
    for p in perc[-5:]:
        print(p)

#<------------------------------------------------------------------------------------------------->

# Main program
def main():
    unsorted_percentage = []
    sorted_percentage = []

    while True:
        print("\n--------------------MENU--------------------")
        print("1. Accept the Percentage of Students")
        print("2. Display the Percentages of Students")
        print("3. Perform Quick Sort on the Data")
        print("4. Exit")

        ch = int(input("Enter your choice (from 1 to 4): "))

        if ch == 1:
            unsorted_percentage = input_percentage()

        elif ch == 2:
            print_percentage(unsorted_percentage)

        elif ch == 3:
            print("Percentages of Students after performing Quick Sort:")
            sorted_percentage = quick_sort(unsorted_percentage, 0, len(unsorted_percentage) - 1)
            print_percentage(sorted_percentage)
            if input("Do you want to display the Top 5 Percentages of Students (yes/no): ").strip().lower() == 'yes':
                display_top_five(sorted_percentage)

        elif ch == 4:
            print("Thanks for using this program!!")
            break

        else:
            print("Invalid Choice!!")

#<------------------------------------------------------------------------------------------------->

# Run the main program
if __name__ == "__main__":
    main()

#<------------------------------------------ END OF PROGRAM ----------------------------------------->



#<-------------------------------------------- OUTPUT ----------------------------------------------->

'''
--------------------MENU--------------------
1. Accept the Percentage of Students  
2. Display the Percentages of Students
3. Perform Quick Sort on the Data     
4. Exit
Enter your choice (from 1 to 4): 1    
Enter the number of students: 3
Enter the percentage of Student 1: 45.5
Enter the percentage of Student 2: 60.3
Enter the percentage of Student 3: 55.5

--------------------MENU--------------------
1. Accept the Percentage of Students        
2. Display the Percentages of Students      
3. Perform Quick Sort on the Data
4. Exit
Enter your choice (from 1 to 4): 2
45.5
60.3
55.5

--------------------MENU--------------------
1. Accept the Percentage of Students        
2. Display the Percentages of Students      
3. Perform Quick Sort on the Data
4. Exit
Enter your choice (from 1 to 4): 3
Percentages of Students after performing Quick Sort:
45.5
55.5
60.3
Do you want to display the Top 5 Percentages of Students (yes/no): yes 
Top Five Percentages are:
45.5
55.5
60.3
'''
