/*
OUESTION:
    Convert given binary tree into threaded binary tree. Analyze time and space complexity of the algorithm.


OUTPUT:
    Enter tree nodes in pre-order (-1 for NULL):
    50 37 75 -1 -1 -1 -1 
    Inorder traversal of the double-threaded binary tree:
    75 37 50 

*/

#include <iostream>
using namespace std;

// Node structure for the binary tree.
struct Node {
    int data;
    Node *left, *right;
    bool leftThread, rightThread; // true if the pointer is a thread

    Node(int d)
        : data(d), left(nullptr), right(nullptr),
          leftThread(false), rightThread(false) {}
};

// Function to create a binary tree from user input.
// Input is expected in pre-order with -1 indicating a NULL child.
Node* createTree() {
    int val;
    cin >> val;
    if(val == -1)
        return nullptr;
    
    Node* root = new Node(val);
    // Recursively build left and right subtrees.
    root->left  = createTree();
    root->right = createTree();
    return root;
}

// Recursive function that converts the binary tree into a double-threaded tree.
// 'prev' is used to keep track of the previously visited node in the inorder traversal.
void createThreaded(Node* root, Node*& prev) {
    if (root == nullptr)
        return;
    
    // Process left subtree
    createThreaded(root->left, prev);
    
    // If the left child is NULL, then make left pointer a thread to the inorder predecessor.
    if (root->left == nullptr) {
        root->left = prev;
        root->leftThread = true;
    }
    
    // For the previous node, if its right child is NULL, make it a thread to the current node.
    if (prev != nullptr && prev->right == nullptr) {
        prev->right = root;
        prev->rightThread = true;
    }
    
    // Update prev to current node.
    prev = root;
    
    // Process right subtree.
    createThreaded(root->right, prev);
}

// A wrapper function to start the threading process.
void convertToThreaded(Node* root) {
    Node* prev = nullptr;
    createThreaded(root, prev);
}

// Utility function to find the leftmost node starting from 'node'.
// This is used to begin the inorder traversal.
Node* leftmost(Node* node) {
    if (node == nullptr)
        return nullptr;
    while(node->left != nullptr && !node->leftThread)
        node = node->left;
    return node;
}

// Inorder traversal of a double-threaded binary tree using the threads.
void inorderThreaded(Node* root) {
    Node* cur = leftmost(root);
    while(cur != nullptr) {
        cout << cur->data << " ";
        // If the right pointer is a thread, simply follow it.
        if(cur->rightThread)
            cur = cur->right;
        else
            // Otherwise, go to the leftmost node in the right subtree.
            cur = leftmost(cur->right);
    }
    cout << endl;
}

int main() {
    cout << "Enter tree nodes in pre-order (-1 for NULL):\n";
    /*
       Example Input (for a tree):
         10 5 -1 -1 20 -1 -1
       This creates the tree:
                  10
                 /  \
                5    20
    */
    Node* root = createTree();
    
    // Convert the given binary tree into a double-threaded binary tree.
    convertToThreaded(root);
    
    cout << "Inorder traversal of the double-threaded binary tree:\n";
    inorderThreaded(root);
    
    return 0;
}
