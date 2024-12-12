/*
A pizza parlor is accepting a maximum of M orders. Orders are served on a first-come, first-served basis. Once placed, an order cannot be canceled. Write a C++ program to simulate this system using a circular queue with an array.
*/

#include <iostream>
using namespace std;

class PizzaParlor {
    int front, rear, *q, maxSize;

public:
    PizzaParlor(int size) : front(-1), rear(-1), maxSize(size) {
        q = new int[maxSize];  // Allocate memory for the queue
    }

    ~PizzaParlor() {
        delete[] q;  // Free allocated memory
    }

    bool isFull() {
        return (front == 0 && rear == maxSize - 1) || (front == rear + 1);
    }

    bool isEmpty() {
        return front == -1 && rear == -1;
    }

    void addOrder() {
        if (!isFull()) {
            int id;
            cout << "\nEnter the Pizza ID: ";
            cin >> id;

            if (isEmpty()) {
                front = rear = 0;
            } else {
                rear = (rear + 1) % maxSize;
            }
            q[rear] = id;

            char choice;
            cout << "Do you want to add another order? (y/n): ";
            cin >> choice;
            if (choice == 'y' || choice == 'Y') {
                addOrder();
            }
        } else {
            cout << "\nOrders are full.";
        }
    }

    void serveOrder() {
        if (!isEmpty()) {
            cout << "\nOrder served: " << q[front];
            if (front == rear) {
                front = rear = -1;  // Queue is now empty
            } else {
                front = (front + 1) % maxSize;
            }
        } else {
            cout << "\nOrders are empty.";
        }
    }

    void displayOrders() {
        if (!isEmpty()) {
            cout << "\nCurrent Orders: ";
            for (int i = front; i != rear; i = (i + 1) % maxSize) {
                cout << q[i] << " <- ";
            }
            cout << q[rear];
        } else {
            cout << "\nOrders are empty.";
        }
    }

    void menu() {
        int choice;
        do {
            cout << "\n\n * * * * PIZZA PARLOUR * * * *";
            cout << "\n1. Add a Pizza\n2. Display Orders\n3. Serve a Pizza\n4. Exit\nEnter your choice: ";
            cin >> choice;

            switch (choice) {
                case 1: addOrder(); break;
                case 2: displayOrders(); break;
                case 3: serveOrder(); break;
                case 4: exit(0);
                default: cout << "Invalid choice.";
            }
        } while (choice != 4);
    }
};

int main() {
    int M;
    cout << "Enter the maximum number of orders (M): ";
    cin >> M;

    PizzaParlor p1(M);
    p1.menu();
    return 0;
}
