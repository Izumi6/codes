/**
Assignment 8: Write C++ program for storing binary number using doubly linked lists. Write functions-
              a)	To compute 1‘s and 2‘s complement
              b)	Add two binary numbers 
*/

#include <iostream>
using namespace std;

// Node class for doubly linked list
class Node {
public:
    int bit;         // 0 or 1
    Node* next;      // pointer to the next node
    Node* prev;      // pointer to the previous node

    Node(int b) : bit(b), next(nullptr), prev(nullptr) {}
};

// Doubly linked list class
class DoublyLinkedList {
private:
    Node* head;

public:
    DoublyLinkedList() : head(nullptr) {}

    // Function to insert a new bit at the end
    void insert(int bit) {
        Node* newNode = new Node(bit);
        if (!head) {
            head = newNode;
        } else {
            Node* temp = head;
            while (temp->next) {
                temp = temp->next;
            }
            temp->next = newNode;
            newNode->prev = temp;
        }
    }

    // Function to display the binary number
    void display() {
        Node* temp = head;
        while (temp) {
            cout << temp->bit;
            temp = temp->next;
        }
        cout << endl;
    }

    // Function to compute 1's complement
    void computeOnesComplement() {
        Node* temp = head;
        while (temp) {
            temp->bit = 1 - temp->bit; // Flip the bits
            temp = temp->next;
        }
    }

    // Function to compute 2's complement
    void computeTwosComplement() {
        computeOnesComplement(); // Compute 1's complement

        // Add 1 to the 1's complement
        Node* temp = head;
        bool carry = true; // Start with carry set to 1
        while (temp) {
            if (carry) {
                if (temp->bit == 1) {
                    temp->bit = 0; // 1 + 1 = 0 with carry
                } else {
                    temp->bit = 1; // 0 + 1 = 1, stop carry
                    carry = false;
                }
            }
            temp = temp->next;
        }
        // If carry is still true, we need to insert 1 at the beginning
        if (carry) {
            Node* newNode = new Node(1);
            newNode->next = head;
            if (head) head->prev = newNode;
            head = newNode;
        }
    }

    // Function to add two binary numbers
    static DoublyLinkedList addBinary(DoublyLinkedList& num1, Dou-blyLinkedList& num2) {
        Node* ptr1 = num1.head;
        Node* ptr2 = num2.head;
        DoublyLinkedList result;
        bool carry = false;

        // Traverse both lists
        while (ptr1 || ptr2 || carry) {
            int sum = carry; // Start with carry

            if (ptr1) {
                sum += ptr1->bit;
                ptr1 = ptr1->next;
            }
            if (ptr2) {
                sum += ptr2->bit;
                ptr2 = ptr2->next;
            }

            // Resulting bit is sum mod 2
            result.insert(sum % 2);
            // Update carry
            carry = sum / 2;
        }

        return result;
    }
};

int main() {
    DoublyLinkedList binary1, binary2;

    // Input for first binary number
    cout << "Enter first binary number (0s and 1s, end with -1): ";
    int bit;
    while (true) {
        cin >> bit;
        if (bit == -1) break;
        binary1.insert(bit);
    }

    // Input for second binary number
    cout << "Enter second binary number (0s and 1s, end with -1): ";
    while (true) {
        cin >> bit;
        if (bit == -1) break;
        binary2.insert(bit);
    }

    cout << "First binary number: ";
    binary1.display();
    cout << "Second binary number: ";
    binary2.display();

    // Compute and display 1's complement
    binary1.computeOnesComplement();
    cout << "1's complement of first binary number: ";
    binary1.display();

    // Compute and display 2's complement
    binary1.computeTwosComplement();
    cout << "2's complement of first binary number: ";
    binary1.display();

    // Add two binary numbers and display result
    DoublyLinkedList sum = DoublyLinkedList::addBinary(binary1, binary2);
    cout << "Sum of two binary numbers: ";
    sum.display();

    return 0;
}
