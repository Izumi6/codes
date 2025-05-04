#include <iostream>
using namespace std;

struct Node {
	int value;
	Node* left;
	Node* right;
	bool rightThread;
};

Node* newNode(int value) {
	Node* temp = new Node;
	temp->value = value;
	temp->left = temp->right = NULL;
	temp->rightThread = false;
	return temp;
}

Node* convert(Node* root) {
	if (root == NULL) return NULL;

	// Thread the left subtree
	if (root->left) {
		Node* leftSubtree = convert(root->left);
		while (leftSubtree->right && !leftSubtree->rightThread) {
			leftSubtree = leftSubtree->right;
		}
		leftSubtree->right = root;
		leftSubtree->rightThread = true;
	}

	// Thread the right subtree
	if (root->right) {
		return convert(root->right);
	}

	return root;
}

Node* leftmost(Node* root) {
	while (root && root->left) {
		root = root->left;
	}
	return root;
}

void inorder(Node* root) {
	Node* current = leftmost(root);
	while (current) {
		cout << current->value << " ";
		if (current->rightThread) {
			current = current->right;
		} else {
			current = leftmost(current->right);
		}
	}
}

int main() {
	int rt, l1, l2, l3, r1, r2, r3;

	cout << "Enter Root Node: ";
	cin >> rt;
	Node* root = newNode(rt);

	cout << "Enter Left Child of " << rt << ": ";
	cin >> l1;
	root->left = newNode(l1);

	cout << "Enter Right Child of " << rt << ": ";
	cin >> r1;
	root->right = newNode(r1);

	cout << "Enter Left Child of " << l1 << ": ";
	cin >> l2;
	root->left->left = newNode(l2);

	cout << "Enter Left Child of " << r1 << ": ";
	cin >> l3;
	root->right->left = newNode(l3);

	cout << "Enter Right Child of " << r1 << ": ";
	cin >> r2;
	root->right->right = newNode(r2);

	cout << "Enter Right Child of " << l2 << ": ";
	cin >> r3;
	root->left->left->right = newNode(r3);

	convert(root);

	cout << "\nInOrder Traversal of Threaded Binary Tree:\n";
	inorder(root);
	cout << endl;

	return 0;
}
