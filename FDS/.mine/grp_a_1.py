# [ Question ]
# In second year computer engineering class, group A student’s play cricket, group B
# students play badminton and group C students play football.
# Write a Python program using functions to compute following: -
# a) List of students who play both cricket and badminton
# b) List of students who play either cricket or badminton but not both
# c) Number of students who play neither cricket nor badminton
# d) Number of students who play cricket and football but not badminton
# (Note- While realizing the group, duplicate entries should be avoided, Do not use SET
# built-in functions)


# [ Code ]

# logic
# a) intersection
# b) union - intersection
# c) union
# d) intersection - B

# functions
## remove duplicates
def remove_duplicates(lst):
    new_lst = []
    for l in lst:
        if l not in new_lst: new_lst.append(l)
    return new_lst

def intersection(l1, l2):
    in_lst = []
    for i in l1:
        if i in l2: in_lst.append(i)
    return in_lst

def union(l1, l2):
    u_lst = []
    for i in l1:
        if i not in u_lst: u_lst.append(i)
    for i in l2:
        if i not in u_lst: u_lst.append(i)
    return u_lst

def minus(l1, l2):
    # l1 - l2
    m_lst = []
    for i in l1:
        if i not in l2: m_lst.append(i)
    return m_lst


# main
def main():
    # taking inputs
    a = input("Enter names students who play cricket (each seperated by space): ").split()
    b = input("Enter names students who play badminton (each seperated by space): ").split()
    c = input("Enter names students who play football (each seperated by space): ").split()


    while True:
        # choose options
        try:
            o = input('''\nChoose one of the following:
        a) List of students who play both cricket and badminton
        b) List of students who play either cricket or badminton but not both
        c) Number of students who play neither cricket nor badminton
        d) Number of students who play cricket and football but not badminton
    > ''')
        except:
            print("[!] Invalid input")

        
        # a) List of students who play both cricket and badminton
        if o == 'a': print('\na: ', intersection(a, b))

        # b) List of students who play either cricket or badminton but not both
        elif o == 'b': print('\nb:', minus(union(a, b), intersection(a, b)))

        # c) Number of students who play neither cricket nor badminton
        elif o == 'c': print('\nc:', minus(c, union(a, b)))

        # d) Number of students who play cricket and football but not badminton
        elif o == 'd': print('\nd:', len(minus(intersection(a, c), b)))

        else: print("[!] Wrong choice")


if __name__ == '__main__':
    main()
