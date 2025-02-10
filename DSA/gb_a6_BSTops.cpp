#include<bits/stdc++.h>
using namespace std;

struct Node
{
    int data;
    Node *left;
    Node *right;
    Node(int data)
    {
        this->data = data;
        left = NULL;
        right = NULL;
    }
};

void traversal(Node* root) 
{
    if (root == NULL)
    {
        return;
    }
    cout << root->data << " ";
    traversal(root->left);
    traversal(root->right);
}

Node* insert(Node* &root, int x)
{
    if (root == NULL)
    {
        root = new Node(x);
    }
    else if (x < root->data) // Insert smaller values to the left
    {
        root->left = insert(root->left, x);
    }
    else // Insert greater or equal values to the right
    {
        root->right = insert(root->right, x);
    }
    return root;
}

int height(Node* root)
{
    if (root == NULL)
    {
        return 0; // Height of an empty tree is 0
    }    
    int left_subtree = height(root->left);
    int right_subtree = height(root->right);
    return max(left_subtree, right_subtree) + 1;
}

int minimum(Node* root)
{
    if (root == NULL)
    {
        cout << "Tree is empty!" << endl;
        return -1; // Return an invalid value for empty tree
    }
    while (root->left != NULL) // Traverse to the leftmost node
    {
        root = root->left;
    }
    return root->data;
}

void search(Node* root, int key, bool &present)
{
    if (root == NULL)
    {
        return;
    }
    if (root->data == key)
    {
        present = true;
        return; // Stop further recursion once found
    }
    else if (root->data > key)
    {
        search(root->left, key, present);
    }
    else
    {
        search(root->right, key, present);
    }
}

void mirror(Node* &root)
{
    if (root == NULL)
    {
        return;
    }
    
    // Swap left and right subtrees
    swap(root->left, root->right);
    
    // Recursively mirror the left and right subtrees
    mirror(root->left);
    mirror(root->right);
    
}

int main()
{
    Node *root = NULL;
    int n;
    cout << "Enter the number of nodes to be inserted in the BST-\n";
    cin >> n;
    
    for (int i = 0; i < n; i++)
    {
        int element;
        cout << "Enter the data value to be inserted-\n";
        cin >> element;
        insert(root, element);
    }

    cout << "Displaying the elements of the BST before mirroring-\n";
    traversal(root);
    cout << endl;


    cout << "Height of the tree is " << height(root) << endl;
    cout << "Minimum value in the BST is " << minimum(root) << endl;

    
    // Mirror the tree
    mirror(root);
    
    cout << "Displaying the elements of the BST after mirroring-\n";
    traversal(root);
    cout << endl;
    
     
    int key;
    cout << "Enter the data value to be searched in the BST-\n";
    cin >> key;
    
    bool present = false; 
    search(root, key, present);
    if (present == true)
    {
        cout << "Key is present in the BST!" << endl;
    }
    else
    {
        cout << "Key is not present in the BST!" << endl;
    }
    return 0;
}
