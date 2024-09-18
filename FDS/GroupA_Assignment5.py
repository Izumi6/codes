'''
Assignment 5: Write a python program to store first year percentage of students in an array.
                      Write function for sorting array of floating point numbers in ascending order using:
                      a) Selection Sort
                      b) Bubble Sort and display top five scores
'''

#<------------------------------------------ START OF PROGRAM ----------------------------------------->

# Function for Selection Sort of elements
def Selection_Sort(marks):
    for i in range(len(marks)):

        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, len(marks)):
            if marks[min_idx] > marks[j]:
                min_idx = j

        # Swap the minimum element with the first element
        marks[i], marks[min_idx] = marks[min_idx], marks[i]

    print("Marks of students after performing Selection Sort on the list : ")
    for i in range(len(marks)):
        print(marks[i])

#<--------------------------------------------------------------------------------------->

# Function for Bubble Sort of elements
def Bubble_Sort(marks):
    n = len(marks)
    # Traverse through all array elements
    for i in range(n - 1):
        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if marks[j] > marks[j + 1]:
                marks[j], marks[j + 1] = marks[j + 1], marks[j]

    print("Marks of students after performing Bubble Sort on the list :")
    for i in range(len(marks)):
        print(marks[i])

#<--------------------------------------------------------------------------------------->

# Function for displaying top five marks

def top_five_marks(marks):
    print("Top",len(marks),"Marks are : ")
    print(*marks[::-1], sep="\n")

#<---------------------------------------------------------------------------------------->

# Main

marks=[]
n = int(input("Enter number of students whose marks are to be displayed : "))
print("Enter marks for",n,"students (Press ENTER after every students marks): ")
for i in range(0, n):
    ele = int(input())
    marks.append(ele)  # adding the element

print("The marks of",n,"students are : ", marks)

while True:
    print("\n---------------MENU---------------")
    print("1. Selection Sort of the marks")
    print("2. Bubble Sort of the marks")
    print("3. Exit")
    ch=int(input("\n\nEnter your choice (from 1 to 3) : "))

    if ch==1:
        Selection_Sort(marks)
        a=input("\nDo you want to display top marks from the list (yes/no) : ")
        if a=='yes':
            top_five_marks(marks)
        else:
            break

    elif ch==2:
        Bubble_Sort(marks)
        a = input("\nDo you want to display top five marks from the list (yes/no) : ")
        if a == 'yes':
            top_five_marks(marks)
        else:
            break

    elif ch==3:
        break

    else:
        print("\nEnter a valid choice!!")
        break


#<------------------------------------------ END OF PROGRAM ----------------------------------------->




#<-------------------------------------------- OUTPUT ----------------------------------------------->

'''
Enter number of students whose marks are to be displayed : 5
Enter marks for 5 students (Press ENTER after every students marks): 
12
45
62
13
14
The marks of 5 students are :  [12, 45, 62, 13, 14]

---------------MENU---------------
1. Selection Sort of the marks
2. Bubble Sort of the marks
3. Exit


Enter your choice (from 1 to 3) : 1
Marks of students after performing Selection Sort on the list : 
12
13
14
45
62

Do you want to display top marks from the list (yes/no) : yes
Top 5 Marks are : 
62
45
14
13
12

---------------MENU---------------
1. Selection Sort of the marks
2. Bubble Sort of the marks
3. Exit


Enter your choice (from 1 to 3) : 2
Marks of students after performing Bubble Sort on the list :
12
13
14
45
62
'''
