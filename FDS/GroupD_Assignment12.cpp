/*
Write a program to implement a priority queue in C++ using an ordered list to store the items in the queue. Create a class that includes template data items and an integer for priority. The ordered list should contain these objects, with the operator<= overloaded so that the items with the highest priority appear at the start of the list.

*/

#include <iostream>

using namespace std;

template <typename T>
class PriorityQueue {
private:
    struct Node {
        T data;
        int priority;
        Node* next;

        Node(T d, int p) : data(d), priority(p), next(nullptr) {}
    };

    Node* head;

public:
    PriorityQueue() : head(nullptr) {}

    ~PriorityQueue() {
        while (head) {
            dequeue();
        }
    }

    void enqueue(T data, int priority) {
        Node* newNode = new Node(data, priority);
        if (!head || head->priority < priority) {
            newNode->next = head;
            head = newNode;
        } else {
            Node* current = head;
            while (current->next && current->next->priority >= priority) {
                current = current->next;
            }
            newNode->next = current->next;
            current->next = newNode;
        }
    }

    void dequeue() {
        if (!head) {
            cout << "Queue is empty!" << endl;
            return;
        }
        Node* temp = head;
        cout << "Dequeued item: " << head->data << " with priority: " << head->priority << endl;
        head = head->next;
        delete temp;
    }

    void display() const {
        if (!head) {
            cout << "Queue is empty!" << endl;
            return;
        }
        Node* current = head;
        cout << "Priority Queue (highest priority first):" << endl;
        while (current) {
            cout << "Data: " << current->data << ", Priority: " << current->priority << endl;
            current = current->next;
        }
    }
};

int main() {
    PriorityQueue<int> pq;
    int choice, priority, data;

    do {
        cout << "\n1. Enqueue\n2. Dequeue\n3. Display\n4. Exit\nEnter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter data: ";
                cin >> data;
                cout << "Enter priority: ";
                cin >> priority;
                pq.enqueue(data, priority);
                break;
            case 2:
                pq.dequeue();
                break;
            case 3:
                pq.display();
                break;
            case 4:
                cout << "Exiting program..." << endl;
                break;
            default:
                cout << "Invalid choice! Please try again." << endl;
        }
    } while (choice != 4);

    return 0;
}
