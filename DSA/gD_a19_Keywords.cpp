#include <iostream>
using namespace std;

// Structure for a dictionary entry (AVL Tree Node)
struct Entry {
    string keyword;
    string meaning;
    Entry* left;
    Entry* right;
    int height;
};

// Function to get height of a node
int getHeight(Entry* node) {
    return (node == NULL) ? 0 : node->height;
}

// Utility to get max of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// Function to create a new Entry
Entry* createEntry(string keyword, string meaning) {
    Entry* entry = new Entry;
    entry->keyword = keyword;
    entry->meaning = meaning;
    entry->left = entry->right = NULL;
    entry->height = 1;
    return entry;
}

// Right rotation
Entry* rightRotate(Entry* y) {
    Entry* x = y->left;
    Entry* T2 = x->right;
    x->right = y;
    y->left = T2;

    y->height = max(getHeight(y->left), getHeight(y->right)) + 1;
    x->height = max(getHeight(x->left), getHeight(x->right)) + 1;
    return x;
}

// Left rotation
Entry* leftRotate(Entry* x) {
    Entry* y = x->right;
    Entry* T2 = y->left;
    y->left = x;
    x->right = T2;

    x->height = max(getHeight(x->left), getHeight(x->right)) + 1;
    y->height = max(getHeight(y->left), getHeight(y->right)) + 1;
    return y;
}

// Get balance factor
int getBalance(Entry* node) {
    return (node == NULL) ? 0 : getHeight(node->left) - getHeight(node->right);
}

// Insert a new entry
Entry* insertEntry(Entry* root, string keyword, string meaning) {
    if (root == NULL)
        return createEntry(keyword, meaning);

    if (keyword < root->keyword)
        root->left = insertEntry(root->left, keyword, meaning);
    else if (keyword > root->keyword)
        root->right = insertEntry(root->right, keyword, meaning);
    else {
        cout << "Keyword already exists.\n";
        return root;
    }

    root->height = 1 + max(getHeight(root->left), getHeight(root->right));
    int balance = getBalance(root);

    // Balance the tree
    if (balance > 1 && keyword < root->left->keyword)
        return rightRotate(root);
    if (balance < -1 && keyword > root->right->keyword)
        return leftRotate(root);
    if (balance > 1 && keyword > root->left->keyword) {
        root->left = leftRotate(root->left);
        return rightRotate(root);
    }
    if (balance < -1 && keyword < root->right->keyword) {
        root->right = rightRotate(root->right);
        return leftRotate(root);
    }

    return root;
}

// Find node with minimum keyword
Entry* findMin(Entry* node) {
    Entry* current = node;
    while (current && current->left != NULL)
        current = current->left;
    return current;
}

// Delete entry
Entry* deleteEntry(Entry* root, string keyword) {
    if (root == NULL)
        return root;

    if (keyword < root->keyword)
        root->left = deleteEntry(root->left, keyword);
    else if (keyword > root->keyword)
        root->right = deleteEntry(root->right, keyword);
    else {
        if (root->left == NULL || root->right == NULL) {
            Entry* temp = root->left ? root->left : root->right;
            if (temp == NULL) {
                temp = root;
                root = NULL;
            } else
                *root = *temp;
            delete temp;
        } else {
            Entry* temp = findMin(root->right);
            root->keyword = temp->keyword;
            root->meaning = temp->meaning;
            root->right = deleteEntry(root->right, temp->keyword);
        }
    }

    if (root == NULL)
        return root;

    root->height = 1 + max(getHeight(root->left), getHeight(root->right));
    int balance = getBalance(root);

    // Balance the tree
    if (balance > 1 && getBalance(root->left) >= 0)
        return rightRotate(root);
    if (balance > 1 && getBalance(root->left) < 0) {
        root->left = leftRotate(root->left);
        return rightRotate(root);
    }
    if (balance < -1 && getBalance(root->right) <= 0)
        return leftRotate(root);
    if (balance < -1 && getBalance(root->right) > 0) {
        root->right = rightRotate(root->right);
        return leftRotate(root);
    }

    return root;
}

// Update entry
bool updateEntry(Entry* root, string keyword, string newMeaning) {
    if (root == NULL)
        return false;
    if (keyword == root->keyword) {
        root->meaning = newMeaning;
        return true;
    } else if (keyword < root->keyword)
        return updateEntry(root->left, keyword, newMeaning);
    else
        return updateEntry(root->right, keyword, newMeaning);
}

// Display entries in ascending order
void displayAscending(Entry* root) {
    if (root != NULL) {
        displayAscending(root->left);
        cout << root->keyword << " : " << root->meaning << endl;
        displayAscending(root->right);
    }
}

// Display entries in descending order
void displayDescending(Entry* root) {
    if (root != NULL) {
        displayDescending(root->right);
        cout << root->keyword << " : " << root->meaning << endl;
        displayDescending(root->left);
    }
}

// Search for a keyword and return comparison count
Entry* searchEntry(Entry* root, string keyword, int& comparisons) {
    comparisons++;
    if (root == NULL || root->keyword == keyword)
        return root;
    if (keyword < root->keyword)
        return searchEntry(root->left, keyword, comparisons);
    else
        return searchEntry(root->right, keyword, comparisons);
}

// Menu-driven main function
int main() {
    Entry* root = NULL;
    int choice;
    string keyword, meaning;
    do {
        cout << "\n--- Dictionary using AVL Tree ---\n";
        cout << "1. Add Keyword\n";
        cout << "2. Delete Keyword\n";
        cout << "3. Update Meaning\n";
        cout << "4. Display in Ascending Order\n";
        cout << "5. Display in Descending Order\n";
        cout << "6. Search Keyword\n";
        cout << "7. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;
        cin.ignore();

        switch (choice) {
        case 1:
            cout << "Enter keyword: ";
            getline(cin, keyword);
            cout << "Enter meaning: ";
            getline(cin, meaning);
            root = insertEntry(root, keyword, meaning);
            break;
        case 2:
            cout << "Enter keyword to delete: ";
            getline(cin, keyword);
            root = deleteEntry(root, keyword);
            break;
        case 3:
            cout << "Enter keyword to update: ";
            getline(cin, keyword);
            cout << "Enter new meaning: ";
            getline(cin, meaning);
            if (updateEntry(root, keyword, meaning))
                cout << "Updated successfully.\n";
            else
                cout << "Keyword not found.\n";
            break;
        case 4:
            cout << "\nDictionary in Ascending Order:\n";
            displayAscending(root);
            break;
        case 5:
            cout << "\nDictionary in Descending Order:\n";
            displayDescending(root);
            break;
        case 6: {
            int comparisons = 0;
            cout << "Enter keyword to search: ";
            getline(cin, keyword);
            Entry* result = searchEntry(root, keyword, comparisons);
            if (result != NULL) {
                cout << "Found:\nKeyword: " << result->keyword << "\nMeaning: " << result->meaning << endl;
            } else {
                cout << "Keyword not found.\n";
            }
            cout << "Total comparisons made: " << comparisons << endl;
            break;
        }
        case 7:
            cout << "Exiting...\n";
            break;
        default:
            cout << "Invalid choice. Try again.\n";
        }
    } while (choice != 7);

    return 0;
}

