/*
OUESTION:
    Represent a given graph using adjacency matrix/list to perform DFS and using adjacency
    list to perform BFS. Use the map of the area around the college as the graph. Identify
    the prominent land marks as nodes and perform DFS and BFS on that.

OUTPUT:
    Enter no. of cities: 3
    Enter city #0 (Airport Code): 111
    Enter city #1 (Airport Code): 222
    Enter city #2 (Airport Code): 333
    
    Your cities are: 
    city #0: 111
    city #1: 222
    city #2: 333
    Enter distance between 111 and 222 : 1
    Enter distance between 111 and 333 : 2
    Enter distance between 222 and 333 : 3
    
            111             222             333
    111     0               1               2
    
    222     1               0               3
    
    333     2               3               0
    Enter Starting Vertex: 2
    DFS: 333 111 222 
    BFS: 333 111 222 

*/


#include <iostream>     // Includes the input/output stream library
#include <queue>        // Includes the queue data structure library

using namespace std;

// Adjacency matrix for representing the graph, initialized with 0
int adj_mat[50][50] = {0, 0}; 

// Visited array to track which nodes have been visited during DFS
int visited[50] = {0};

// Depth-First Search (DFS) function to explore the graph
void dfs(int s, int n, string arr[]) {
    visited[s] = 1;               // Mark the current node as visited
    cout << arr[s] << " ";        // Print the current city/airport code
    for (int i = 0; i < n; i++) {
        if (adj_mat[s][i] && !visited[i])  // Check if there's an edge and the node hasn't been visited
            dfs(i, n, arr);        // Recursively call DFS for the next unvisited node
    }
}

// Breadth-First Search (BFS) function to explore the graph
void bfs(int s, int n, string arr[]) {
    bool visited[n];              // Create a local visited array for BFS
    for (int i = 0; i < n; i++)
        visited[i] = false;       // Initially mark all nodes as unvisited

    int v;
    queue<int> bfsq;              // Queue to store nodes for BFS traversal
    if (!visited[s]) {            // Start BFS if the node has not been visited
        cout << arr[s] << " ";     // Print the starting city/airport code
        bfsq.push(s);              // Push the starting node to the queue
        visited[s] = true;         // Mark the starting node as visited
        while (!bfsq.empty()) {    // Continue until the queue is empty
            v = bfsq.front();      // Get the front element of the queue
            for (int i = 0; i < n; i++) {
                if (adj_mat[v][i] && !visited[i]) {  // Check for adjacent unvisited nodes
                    cout << arr[i] << " ";    // Print the adjacent city/airport code
                    visited[i] = true;        // Mark the adjacent node as visited
                    bfsq.push(i);             // Push the adjacent node to the queue
                }
            }
            bfsq.pop();   // Remove the front node after processing it
        }
    }
}

int main() {
    cout << "Enter no. of cities: ";   // Prompt user to enter the number of cities
    int n, u;
    cin >> n;  // Input the number of cities
    string cities[n];  // Create an array of strings to hold the names of the cities

    // Input city names (airport codes)
    for (int i = 0; i < n; i++) {
        cout << "Enter city #" << i << " (Airport Code): ";
        cin >> cities[i];
    }
    
    cout << "\nYour cities are: " << endl;   // Print out the cities
    for (int i = 0; i < n; i++)
        cout << "city #" << i << ": " << cities[i] << endl;

    // Input the distances between the cities and fill the adjacency matrix
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            cout << "Enter distance between " << cities[i] << " and " << cities[j] << " : ";
            cin >> adj_mat[i][j];  // Input the distance between city i and city j
            adj_mat[j][i] = adj_mat[i][j];  // Since the graph is undirected, mirror the distance
        }
    }

    cout << endl;
    for (int i = 0; i < n; i++)
        cout << "\t" << cities[i] << "\t";  // Print column headers (city names)

    // Print the adjacency matrix
    for (int i = 0; i < n; i++) {
        cout << "\n" << cities[i];  // Print row header (city name)
        for (int j = 0; j < n; j++)
            cout << "\t" << adj_mat[i][j] << "\t";  // Print the matrix elements
        cout << endl;
    }

    // Input the starting city index for DFS and BFS
    cout << "Enter Starting Vertex: ";
    cin >> u;  // Start at city u (provided by the user)

    cout << "DFS: ";
    dfs(u, n, cities);  // Call DFS function starting from city u
    cout << endl;

    cout << "BFS: ";
    bfs(u, n, cities);  // Call BFS function starting from city u
    cout << endl;

    return 0;
}


