/**
Assignment 7: Third and final year of department can be granted membership on request. Similarly one may cancel the membership of club. First node is reserved for president of club and last node is reserved for secretary of club. Write C++ program to maintain club member‘s information using singly linked list. Store student PRN and Name. Write functions to:
              a)	Add and delete the members as well as president or even secretary.
              b)	Compute total number of members of club
              c)	Display members
              Two linked lists exists for two divisions. Concate-nate two lists.
*/

#include <iostream>
#include <string>
using namespace std;

class Node {
public:
    int prn;
    string name;
    Node* next;

    Node(int x, string nm) : prn(x), name(nm), next(nullptr) {}
};

class Club {
    Node* start;

public:
    Club() : start(nullptr) {}

    void create() {
        int no;
        string nam;
        if (start == nullptr) {
            cout << "Enter PRN number: ";
            cin >> no;
            cout << "Enter name: ";
            cin >> nam;
            start = new Node(no, nam);
            cout << "\n=============== List Created ===============";
        } else {
            cout << "\nList is already created.";
        }
    }

    void display() {
        Node* t = start;
        if (start == nullptr) {
            cout << "\nList is Empty";
        } else {
            cout << "\n=============== List: ===============\n";
            while (t != nullptr) {
                cout << t->prn << " " << t->name << " \n";
                t = t->next;
            }
        }
    }

    void insertAtBeginning() {
        int no;
        string nam;
        if (start == nullptr) {
            create();
        } else {
            cout << "\nEnter PRN Number : ";
            cin >> no;
            cout << "Enter Name : ";
            cin >> nam;
            Node* temp = new Node(no, nam);
            temp->next = start;
            start = temp;
            cout << "Inserted " << temp->name << " at the beginning.";
        }
    }

    void insertAtEnd() {
        int no;
        string nam;
        cout << "\nEnter PRN Number : ";
        cin >> no;
        cout << "Enter Name : ";
        cin >> nam;

        Node* newNode = new Node(no, nam);
        if (start == nullptr) {
            start = newNode;
        } else {
            Node* t = start;
            while (t->next != nullptr) {
                t = t->next;
            }
            t->next = newNode;
        }
        cout << "Inserted " << newNode->name << " at the end.";
    }

    void insertAfter() {
        int prev_no;
        cout << "\nEnter PRN No. after which you want to insert: ";
        cin >> prev_no;

        Node* t = start;
        while (t != nullptr && t->prn != prev_no) {
            t = t->next;
        }

        if (t != nullptr) {
            int no;
            string nam;
            cout << "\nEnter PRN Number: ";
            cin >> no;
            cout << "Enter Name: ";
            cin >> nam;

            Node* newNode = new Node(no, nam);
            newNode->next = t->next;
            t->next = newNode;
            cout << "Inserted " << newNode->name << " after " << prev_no << ".";
        } else {
            cout << "\n" << prev_no << " is not in the list.";
        }
    }

    void deleteAtFirst() {
        if (start == nullptr) {
            cout << "\nClub is Empty..";
        } else {
            Node* t = start;
            start = start->next;
            delete t;
            cout << "\nPresident deleted..";
        }
    }

    void deleteByValue() {
        int no;
        cout << "\nEnter PRN No. of member to be deleted: ";
        cin >> no;

        Node* t = start;
        Node* prev = nullptr;

        while (t != nullptr && t->prn != no) {
            prev = t;
            t = t->next;
        }

        if (t != nullptr) {
            if (prev == nullptr) {
                start = t->next; // Deleting the first node
            } else {
                prev->next = t->next; // Bypass the node to delete
            }
            delete t;
            cout << "\nMember with PRN No: " << no << " is deleted.";
        } else {
            cout << "\nMember not found in List.";
        }
    }

    void deleteAtEnd() {
        if (start == nullptr) {
            cout << "\nClub is Empty..";
            return;
        }

        Node* t = start;
        Node* prev = nullptr;

        while (t->next != nullptr) {
            prev = t;
            t = t->next;
        }

        if (prev == nullptr) {
            // Only one node
            start = nullptr;
        } else {
            prev->next = nullptr;
        }
        delete t;
        cout << "\nSecretary deleted.";
    }

    int computeTotal() {
        Node* t = start;
        int count = 0;
        while (t != nullptr) {
            count++;
            t = t->next;
        }
        return count;
    }

    void sortList() {
        if (start == nullptr) {
            cout << "\nList is empty.";
            return;
        }

        for (Node* i = start; i->next != nullptr; i = i->next) {
            for (Node* j = start; j->next != nullptr; j = j->next) {
                if (j->prn > j->next->prn) {
                    swap(j->prn, j->next->prn);
                    swap(j->name, j->next->name);
                }
            }
        }
        cout << "\nList is sorted.";
        display();
    }

    void concatList(Club& other) {
        if (other.start == nullptr) {
            cout << "\nList 2 is empty";
            return;
        }

        if (start == nullptr) {
            start = other.start;
        } else {
            Node* t = start;
            while (t->next != nullptr) {
                t = t->next;
            }
            t->next = other.start;
        }
        other.start = nullptr; // Clear the other list
        cout << "\nAfter concatenation list:\n";
        display();
    }

    void reverseDisplay(Node* t) {
        if (t == nullptr) return;
        reverseDisplay(t->next);
        cout << "\nPRN NO: " << t->prn << " Name: " << t->name;
    }

    void reverseDisplay() {
        if (start == nullptr) {
            cout << "\nList is empty.";
            return;
        }
        reverseDisplay(start);
    }
};

int main() {
    Club l1, l2;
    Club* currentClub = &l1;
    int choice;

    do {
        int selectList;
        cout << "\nSelect List\n1.List 1\n2.List 2\nEnter choice: ";
        cin >> selectList;

        currentClub = (selectList == 1) ? &l1 : (selectList == 2) ? &l2 : nullptr;

        if (currentClub == nullptr) {
            cout << "\nWrong list Number.";
            continue;
        }

        cout << "\n1. Create\n2. Insert President\n3. Insert Secretary\n4. Insert after position(member)\n"
             << "5. Display list\n6. Delete President\n7. Delete Secretary\n8. Delete Member\n"
             << "9. Find total No. of members\n10. Sort list\n11. Combine lists\n12. Reverse Display\n0. Exit\n"
             << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1: currentClub->create(); break;
            case 2: currentClub->insertAtBeginning(); break;
            case 3: currentClub->insertAtEnd(); break;
            case 4: currentClub->insertAfter(); break;
            case 5: currentClub->display(); break;
            case 6: currentClub->deleteAtFirst(); break;
            case 7: currentClub->deleteAtEnd(); break;
            case 8: currentClub->deleteByValue(); break;
            case 9: cout << "\nTotal members (including President & Secretary): " << currentClub->computeTotal(); break;
            case 10: currentClub->sortList(); break;
            case 11: l1.concatList(l2); break;
            case 12: currentClub->reverseDisplay(); break;
            case 0: cout << "\n=============== GOOD BYE ===============\n"; break;
            default: cout << "Wrong choice"; break;
        }
    } while (choice != 0);

    return 0;
}
