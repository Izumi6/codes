/*
 * ==============================================================================
 * LP-5 Practical 1: Parallel BFS and DFS using OpenMP
 * 
 * Problem Statement:
 *   Design and implement Parallel Breadth First Search and Depth First Search
 *   based on existing algorithms using OpenMP. Use a Tree or an undirected graph
 *   for BFS and DFS.
 * 
 * How to Compile & Run:
 *   - On Windows (MinGW GCC):
 *       g++ -fopenmp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs.exe
 *       01_parallel_bfs_dfs.exe
 * 
 *   - On Linux / Ubuntu:
 *       g++ -fopenmp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs
 *       ./01_parallel_bfs_dfs
 * ==============================================================================
 */

#include <iostream>
#include <vector>
#include <queue>
#include <iomanip>
#include <omp.h>

using namespace std;

// Class representing an Undirected Graph
class Graph {
public:
    int V; // Number of vertices
    vector<vector<int>> adj; // Adjacency list

    Graph(int vertices) {
        V = vertices;
        adj.resize(V);
    }

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // -------------------------------------------------------------
    // Sequential Breadth First Search (BFS)
    // -------------------------------------------------------------
    void sequentialBFS(int startNode) {
        vector<bool> visited(V, false);
        queue<int> q;

        visited[startNode] = true;
        q.push(startNode);

        cout << "Sequential BFS Traversal: ";
        while (!q.empty()) {
            int curr = q.front();
            q.pop();
            cout << curr << " ";

            for (int neighbor : adj[curr]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
        cout << endl;
    }

    // -------------------------------------------------------------
    // Parallel Breadth First Search (BFS) using OpenMP
    // -------------------------------------------------------------
    void parallelBFS(int startNode) {
        vector<bool> visited(V, false);
        vector<int> currentFrontier;

        visited[startNode] = true;
        currentFrontier.push_back(startNode);

        cout << "Parallel BFS Traversal  : ";
        while (!currentFrontier.empty()) {
            vector<int> nextFrontier;

            // Process all nodes at the current level in parallel
            #pragma omp parallel
            {
                vector<int> localFrontier;

                #pragma omp for nowait
                for (size_t i = 0; i < currentFrontier.size(); i++) {
                    int curr = currentFrontier[i];

                    #pragma omp critical
                    cout << curr << " ";

                    for (int neighbor : adj[curr]) {
                        bool mustVisit = false;
                        #pragma omp critical
                        {
                            if (!visited[neighbor]) {
                                visited[neighbor] = true;
                                mustVisit = true;
                            }
                        }
                        if (mustVisit) {
                            localFrontier.push_back(neighbor);
                        }
                    }
                }

                // Merge thread-local frontiers into next level frontier
                #pragma omp critical
                {
                    nextFrontier.insert(nextFrontier.end(), localFrontier.begin(), localFrontier.end());
                }
            }
            currentFrontier = nextFrontier;
        }
        cout << endl;
    }

    // -------------------------------------------------------------
    // Sequential Depth First Search (DFS)
    // -------------------------------------------------------------
    void sequentialDFSHelper(int node, vector<bool>& visited) {
        visited[node] = true;
        cout << node << " ";

        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                sequentialDFSHelper(neighbor, visited);
            }
        }
    }

    void sequentialDFS(int startNode) {
        vector<bool> visited(V, false);
        cout << "Sequential DFS Traversal: ";
        sequentialDFSHelper(startNode, visited);
        cout << endl;
    }

    // -------------------------------------------------------------
    // Parallel Depth First Search (DFS) using OpenMP Tasks
    // -------------------------------------------------------------
    void parallelDFSHelper(int node, vector<bool>& visited) {
        bool shouldVisit = false;
        #pragma omp critical
        {
            if (!visited[node]) {
                visited[node] = true;
                cout << node << " ";
                shouldVisit = true;
            }
        }

        if (!shouldVisit) return;

        // Explore neighbors in parallel using OpenMP tasks
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                #pragma omp task
                parallelDFSHelper(neighbor, visited);
            }
        }
        #pragma omp taskwait
    }

    void parallelDFS(int startNode) {
        vector<bool> visited(V, false);
        cout << "Parallel DFS Traversal  : ";
        #pragma omp parallel
        {
            #pragma omp single
            {
                parallelDFSHelper(startNode, visited);
            }
        }
        cout << endl;
    }
};

int main() {
    cout << "=================================================" << endl;
    cout << "  LP-5 Practical 1: Parallel BFS and DFS" << endl;
    cout << "=================================================" << endl;

    // Creating sample undirected graph (7 vertices: 0 to 6)
    //        0
    //       / \
    //      1   2
    //     / \   \
    //    3   4   5
    //             \
    //              6
    int numVertices = 7;
    Graph g(numVertices);

    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 4);
    g.addEdge(2, 5);
    g.addEdge(5, 6);

    cout << "Graph created with 7 vertices and 6 edges." << endl;
    cout << "Starting traversals from vertex 0:\n" << endl;

    // 1. Breadth First Search
    double start = omp_get_wtime();
    g.sequentialBFS(0);
    double end = omp_get_wtime();
    cout << "Sequential BFS Time: " << fixed << setprecision(3) << (end - start) * 1000 << " ms\n" << endl;

    start = omp_get_wtime();
    g.parallelBFS(0);
    end = omp_get_wtime();
    cout << "Parallel BFS Time  : " << fixed << setprecision(3) << (end - start) * 1000 << " ms\n" << endl;

    // 2. Depth First Search
    start = omp_get_wtime();
    g.sequentialDFS(0);
    end = omp_get_wtime();
    cout << "Sequential DFS Time: " << fixed << setprecision(3) << (end - start) * 1000 << " ms\n" << endl;

    start = omp_get_wtime();
    g.parallelDFS(0);
    end = omp_get_wtime();
    cout << "Parallel DFS Time  : " << fixed << setprecision(3) << (end - start) * 1000 << " ms\n" << endl;

    cout << "=================================================" << endl;
    return 0;
}

/*
============================== SAMPLE OUTPUT ==============================
=================================================
  LP-5 Practical 1: Parallel BFS and DFS
=================================================
Graph created with 7 vertices and 6 edges.
Starting traversals from vertex 0:

Sequential BFS Traversal: 0 1 2 3 4 5 6 
Sequential BFS Time: 0.015 ms

Parallel BFS Traversal  : 0 1 2 3 4 5 6 
Parallel BFS Time  : 0.280 ms

Sequential DFS Traversal: 0 1 3 4 2 5 6 
Sequential DFS Time: 0.008 ms

Parallel DFS Traversal  : 0 1 3 4 2 5 6 
Parallel DFS Time  : 0.350 ms

=================================================
===========================================================================
*/
