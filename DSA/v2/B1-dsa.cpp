#include <iostream>
#include <string>
using namespace std;

struct Node {
    string label;
    int childCount;
    Node* children[10];

    Node() : childCount(0) {
        for (int i = 0; i < 10; ++i)
            children[i] = nullptr;
    }
};

class BookTree {
public:
    BookTree() : root(nullptr) {}
    ~BookTree() {
        deleteTree(root);
    }

    void createTree();
    void displayTree();

private:
    Node* root;

    void deleteTree(Node* node);
};

// Recursive delete to free memory
void BookTree::deleteTree(Node* node) {
    if (!node) return;
    for (int i = 0; i < node->childCount; ++i) {
        deleteTree(node->children[i]);
    }
    delete node;
}

// Create the book hierarchy
void BookTree::createTree() {
    if (root != nullptr) {
        char choice;
        cout << "Book tree already exists. Do you want to recreate it? (y/n): ";
        cin >> choice;
        cin.ignore();
        if (choice != 'y' && choice != 'Y') return;

        deleteTree(root);
        root = nullptr;
    }

    root = new Node;

    cout << "Enter name of the Book: ";
    getline(cin, root->label);

    cout << "Enter number of Chapters (max 10): ";
    cin >> root->childCount;
    cin.ignore();
    if (root->childCount > 10) {
        cout << "Maximum of 10 chapters allowed. Truncating to 10." << endl;
        root->childCount = 10;
    }

    for (int i = 0; i < root->childCount; ++i) {
        root->children[i] = new Node;
        cout << "Enter name of Chapter " << i + 1 << ": ";
        getline(cin, root->children[i]->label);

        cout << "Enter number of Sections in Chapter \"" << root->children[i]->label << "\" (max 10): ";
        cin >> root->children[i]->childCount;
        cin.ignore();
        if (root->children[i]->childCount > 10) {
            cout << "Maximum of 10 sections allowed. Truncating to 10." << endl;
            root->children[i]->childCount = 10;
        }

        for (int j = 0; j < root->children[i]->childCount; ++j) {
            root->children[i]->children[j] = new Node;
            cout << "Enter name of Section " << j + 1 << ": ";
            getline(cin, root->children[i]->children[j]->label);
        }
    }
}

// Display the tree structure
void BookTree::displayTree() {
    if (!root) {
        cout << "Book tree does not exist. Please create it first." << endl;
        return;
    }

    cout << "\n------- Book Hierarchy -------" << endl;
    cout << "Book Title: " << root->label << endl;

    for (int i = 0; i < root->childCount; ++i) {
        Node* chapter = root->children[i];
        cout << "\n  Chapter " << i + 1 << ": " << chapter->label << endl;
        cout << "    Sections:" << endl;
        for (int j = 0; j < chapter->childCount; ++j) {
            cout << "      - " << chapter->children[j]->label << endl;
        }
    }
    cout << "------------------------------\n" << endl;
}

int main() {
    BookTree bookTree;
    int choice;

    while (true) {
        cout << "\n=========== Book Tree Menu ===========\n";
        cout << "1. Create Book Tree\n";
        cout << "2. Display Book Tree\n";
        cout << "3. Quit\n";
        cout << "Enter your choice: ";
        cin >> choice;
        cin.ignore(); // flush newline after choice

        switch (choice) {
            case 1:
                bookTree.createTree();
                break;
            case 2:
                bookTree.displayTree();
                break;
            case 3:
                cout << "Thank you for using the Book Tree program!" << endl;
                return 0;
            default:
                cout << "Invalid choice. Please enter 1, 2, or 3." << endl;
        }
    }

    return 0;
}
