/*
Queues are frequently used in computer programming, and a typical example is the creation of a job queue by an operating system. If the operating system does not use priorities, then the jobs are processed in the order they enter the system. Write C++ program for simulating job queue. Write functions to add job and delete job from queue.
*/

#include <iostream>
#define MAX 10

using namespace std;

struct Queue {
    int data[MAX];
    int front, rear;

    Queue() : front(-1), rear(-1) {}

    bool isEmpty() { return front == rear; }
    bool isFull() { return rear == MAX - 1; }

    void enqueue(int x) {
        if (!isFull()) {
            data[++rear] = x;
        }
    }

    int delQueue() {
        if (!isEmpty()) {
            return data[++front];
        }
        return -1; // Indicating queue is empty
    }

    void display() {
        for (int i = front + 1; i <= rear; i++)
            cout << data[i] << " ";
        cout << endl;
    }
};

int main() {
    Queue obj;
    int choice, x;

    do {
        cout << "\n1. Insert Job\n2. Delete Job\n3. Display\n4. Exit\nEnter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "\nEnter data: ";
                cin >> x;
                obj.enqueue(x);
                if (obj.isFull()) cout << "Queue is overflow!!!\n";
                break;
            case 2:
                if (!obj.isEmpty()) {
                    cout << "\nDeleted Element = " << obj.delQueue() << endl;
                    cout << "Remaining Jobs: ";
                    obj.display();
                } else {
                    cout << "\nQueue is underflow!!!\n";
                }
                break;
            case 3:
                if (!obj.isEmpty()) {
                    cout << "\nQueue contains: ";
                    obj.display();
                } else {
                    cout << "\nQueue is empty!!!\n";
                }
                break;
            case 4:
                cout << "\nExiting Program...\n";
                break;
            default:
                cout << "\nInvalid choice!\n";
        }
    } while (choice != 4);

    return 0;
}