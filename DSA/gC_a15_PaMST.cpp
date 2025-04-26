/*
OUESTION:
    You have a business with several offices; you want to lease phone lines to connect them
    up with each other; and the phone company charges different amounts of money to
    connect different pairs of cities. You want a set of lines that connects all your offices
    with a minimum total cost. Solve the problem by suggesting appropriate data structures.

OUTPUT:
    ========== PRIM'S ALGORITHM =================
    
    1. INPUT
    2. DISPLAY
    3. MINIMUM
    
    Enter your choice: 1
    ******* INPUT YOUR VALUES *******
    Enter the number of branches: 3
    
    Enter the number of connections: 2
    Enter the end branches of connection: 
    2
    1
    Enter the phone company charges for this connection: 12
    Enter the end branches of connection: 
    5
    4
    Enter the phone company charges for this connection: 43
    ========== PRIM'S ALGORITHM =================
    
    1. INPUT
    2. DISPLAY
    3. MINIMUM
    
    Enter your choice: 2
    ******* DISPLAY THE CONTENTS *******
    
    Adjacency matrix:
    999   12   999   
    
    12   999   999   
    
    999   999   999   
    ========== PRIM'S ALGORITHM =================
    
    1. INPUT
    2. DISPLAY
    3. MINIMUM
    
    Enter your choice: 3
    ********* MINIMUM ************
    Minimum cost connection is 1 -> 2  with charge : 12
    Minimum cost connection is 1 -> 2  with charge : 999
    The minimum total cost of connections of all branches is: 1011
*/


#include <iostream>  // Include the standard input-output stream library
using namespace std; // Using the standard namespace to avoid prefixing std::

// Class definition for tree (used for finding Minimum Spanning Tree using Prim's Algorithm)
class tree {
    int a[20][20], l, u, w, i, j, v, e, visited[20]; // Variables for adjacency matrix, connections, and tracking visited nodes

public:
    void input();   // Function to input the graph (branches and connections)
    void display(); // Function to display the adjacency matrix
    void minimum(); // Function to find the minimum spanning tree using Prim’s algorithm
};

// Function to take input for the graph
void tree::input() {
    cout << "Enter the number of branches: ";
    cin >> v; // Number of vertices (branches)

    // Initialize adjacency matrix and visited array
    for (i = 0; i < v; i++) {
        visited[i] = 0;  // Mark all nodes as unvisited initially
        for (j = 0; j < v; j++) {
            a[i][j] = 999; // Initialize adjacency matrix with a large value (representing no direct connection)
        }
    }

    cout << "\nEnter the number of connections: ";
    cin >> e; // Number of edges (connections)

    // Input each connection along with its weight (phone company charges)
    for (i = 0; i < e; i++) {
        cout << "Enter the end branches of connection: " << endl;
        cin >> l >> u; // Input two connected branches
        cout << "Enter the phone company charges for this connection: ";
        cin >> w; // Input weight of the edge
        a[l - 1][u - 1] = a[u - 1][l - 1] = w; // Storing weight in adjacency matrix (undirected graph)
    }
}

// Function to display the adjacency matrix
void tree::display() {
    cout << "\nAdjacency matrix:";
    for (i = 0; i < v; i++) {
        cout << endl;
        for (j = 0; j < v; j++) {
            cout << a[i][j] << "   "; // Print adjacency matrix values
        }
        cout << endl;
    }
}

// Function implementing Prim's Algorithm to find Minimum Spanning Tree (MST)
void tree::minimum() {
    int p = 0, q = 0, total = 0, min; // Variables to track the minimum edge and total cost
    visited[0] = 1; // Start from the first node

    // Loop to find the minimum spanning tree (MST)
    for (int count = 0; count < (v - 1); count++) {
        min = 999; // Reset min to a large value
        for (i = 0; i < v; i++) {
            if (visited[i] == 1) { // If the node is already included in MST
                for (j = 0; j < v; j++) {
                    if (visited[j] != 1) { // Check only unvisited nodes
                        if (min > a[i][j]) { // Find the smallest edge weight
                            min = a[i][j];
                            p = i;
                            q = j;
                        }
                    }
                }
            }
        }
        visited[p] = 1; // Mark both nodes as visited
        visited[q] = 1;
        total = total + min; // Add edge weight to total cost

        // Display the minimum cost edge added to the MST
        cout << "Minimum cost connection is " << (p + 1) << " -> " << (q + 1) << "  with charge : " << min << endl;
    }
    cout << "The minimum total cost of connections of all branches is: " << total << endl;
}

// Main function
int main() {
    int ch;
    tree t; // Object of class tree

    do {
        // Display menu
        cout << "========== PRIM'S ALGORITHM =================" << endl;
        cout << "\n1. INPUT\n2. DISPLAY\n3. MINIMUM\n" << endl;
        cout << "Enter your choice: ";
        cin >> ch;

        // Switch case to perform user-selected operation
        switch (ch) {
            case 1:
                cout << "******* INPUT YOUR VALUES *******" << endl;
                t.input();
                break;
            case 2:
                cout << "******* DISPLAY THE CONTENTS *******" << endl;
                t.display();
                break;
            case 3:
                cout << "********* MINIMUM ************" << endl;
                t.minimum();
                break;
        }

    } while (ch != 4); // Exit condition
    return 0;
}

