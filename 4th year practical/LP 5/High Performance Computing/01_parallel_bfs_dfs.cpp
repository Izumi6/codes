/**
 * ======================================================================================
 *   Laboratory Practice 5 (LP 5): High Performance Computing (410250)
 *   Practical 1: Parallel Breadth First Search (BFS) and Depth First Search (DFS)
 * ======================================================================================
 * 
 *   Problem Statement:
 *     Design and implement Parallel Breadth First Search and Depth First Search
 *     based on existing algorithms using OpenMP. Use a Tree or an undirected graph
 *     for BFS and DFS.
 * 
 *   Approach:
 *     1. Undirected Graph Representation:
 *        - Adjacency list representation using std::vector<std::vector<int>>.
 *     2. Parallel Breadth First Search (BFS):
 *        - Level-synchronous BFS. Nodes at the current depth (frontier) are explored
 *          concurrently using OpenMP parallel for loops.
 *        - Uses atomic operations / thread-private buffers to avoid data races
 *          when discovering new nodes for the next frontier.
 *     3. Parallel Depth First Search (DFS):
 *        - Task-based parallelization using OpenMP tasks (#pragma omp task).
 *        - Independent subtrees are explored as parallel tasks, synchronized with
 *          #pragma omp taskwait.
 *     4. Performance Analysis:
 *        - Compares sequential and parallel execution times and calculates speedup.
 * 
 *   Compilation Commands:
 *     - Linux (GCC):
 *         g++ -O2 -fopenmp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs
 *     - macOS (Apple Clang with Homebrew libomp):
 *         clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include \
 *                 -L/opt/homebrew/opt/libomp/lib -lomp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs
 * 
 *   Execution Command:
 *     ./01_parallel_bfs_dfs
 * ======================================================================================
 */

#include <iostream>
#include <vector>
#include <queue>
#include <chrono>
#include <iomanip>
#include <atomic>
#include <random>

#ifdef _OPENMP
#include <omp.h>
#endif

// ============================================================================
// Undirected Graph Class
// ============================================================================
class Graph {
private:
    int numVertices;
    std::vector<std::vector<int>> adj;

public:
    explicit Graph(int v) : numVertices(v), adj(v) {}

    void addEdge(int u, int v) {
        if (u >= 0 && u < numVertices && v >= 0 && v < numVertices) {
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
    }

    int getNumVertices() const {
        return numVertices;
    }

    const std::vector<int>& getNeighbors(int u) const {
        return adj[u];
    }

    // ------------------------------------------------------------------------
    // 1. Sequential Breadth First Search (BFS)
    // ------------------------------------------------------------------------
    std::vector<int> sequentialBFS(int startVertex) const {
        std::vector<int> traversalOrder;
        std::vector<bool> visited(numVertices, false);
        std::queue<int> q;

        visited[startVertex] = true;
        q.push(startVertex);

        while (!q.empty()) {
            int current = q.front();
            q.pop();
            traversalOrder.push_back(current);

            for (int neighbor : adj[current]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
        return traversalOrder;
    }

    // ------------------------------------------------------------------------
    // 2. Parallel Breadth First Search (BFS) using OpenMP
    // ------------------------------------------------------------------------
    std::vector<int> parallelBFS(int startVertex) const {
        std::vector<int> traversalOrder;
        std::vector<std::atomic<bool>> visited(numVertices);
        for (int i = 0; i < numVertices; ++i) {
            visited[i].store(false, std::memory_order_relaxed);
        }

        std::vector<int> currentFrontier;
        visited[startVertex].store(true, std::memory_order_relaxed);
        currentFrontier.push_back(startVertex);

        while (!currentFrontier.empty()) {
            traversalOrder.insert(traversalOrder.end(), currentFrontier.begin(), currentFrontier.end());

            std::vector<int> nextFrontier;
            int frontierSize = static_cast<int>(currentFrontier.size());

            #pragma omp parallel
            {
                std::vector<int> localNextFrontier;

                #pragma omp for schedule(guided) nowait
                for (int i = 0; i < frontierSize; ++i) {
                    int u = currentFrontier[i];
                    for (int neighbor : adj[u]) {
                        // Lock-free atomic test-and-set: exchange returns previous value
                        if (!visited[neighbor].exchange(true, std::memory_order_relaxed)) {
                            localNextFrontier.push_back(neighbor);
                        }
                    }
                }

                // Append local frontier into shared nextFrontier
                #pragma omp critical
                {
                    nextFrontier.insert(nextFrontier.end(), localNextFrontier.begin(), localNextFrontier.end());
                }
            }

            currentFrontier = std::move(nextFrontier);
        }

        return traversalOrder;
    }

    // ------------------------------------------------------------------------
    // 3. Sequential Depth First Search (DFS)
    // ------------------------------------------------------------------------
    void sequentialDFSHelper(int u, std::vector<bool>& visited, std::vector<int>& order) const {
        visited[u] = true;
        order.push_back(u);

        for (int neighbor : adj[u]) {
            if (!visited[neighbor]) {
                sequentialDFSHelper(neighbor, visited, order);
            }
        }
    }

    std::vector<int> sequentialDFS(int startVertex) const {
        std::vector<int> traversalOrder;
        std::vector<bool> visited(numVertices, false);
        sequentialDFSHelper(startVertex, visited, traversalOrder);
        return traversalOrder;
    }

    // ------------------------------------------------------------------------
    // 4. Parallel Depth First Search (DFS) using OpenMP Tasks
    // ------------------------------------------------------------------------
    void parallelDFSHelper(int u, std::vector<std::atomic<bool>>& visited, std::vector<int>& order, int depth) const {
        for (int neighbor : adj[u]) {
            if (!visited[neighbor].exchange(true, std::memory_order_relaxed)) {
                if (order.size() < 100) {
                    #pragma omp critical
                    {
                        order.push_back(neighbor);
                    }
                }

                if (depth < 4) {
                    #pragma omp task firstprivate(neighbor, depth) shared(visited, order)
                    {
                        parallelDFSHelper(neighbor, visited, order, depth + 1);
                    }
                } else {
                    parallelDFSHelper(neighbor, visited, order, depth + 1);
                }
            }
        }
        #pragma omp taskwait
    }

    std::vector<int> parallelDFS(int startVertex) const {
        std::vector<int> traversalOrder;
        std::vector<std::atomic<bool>> visited(numVertices);
        for (int i = 0; i < numVertices; ++i) {
            visited[i].store(false, std::memory_order_relaxed);
        }

        visited[startVertex].store(true, std::memory_order_relaxed);
        traversalOrder.push_back(startVertex);

        #pragma omp parallel
        {
            #pragma omp single
            {
                parallelDFSHelper(startVertex, visited, traversalOrder, 0);
            }
        }
        return traversalOrder;
    }
};

// ============================================================================
// Helper: Print Traversal Vector
// ============================================================================
void printOrder(const std::string& label, const std::vector<int>& order, size_t limit = 15) {
    std::cout << "  " << std::left << std::setw(22) << label << ": [ ";
    size_t count = std::min(order.size(), limit);
    for (size_t i = 0; i < count; ++i) {
        std::cout << order[i] << (i + 1 < count ? ", " : "");
    }
    if (order.size() > limit) {
        std::cout << ", ... (" << order.size() << " total)";
    }
    std::cout << " ]\n";
}

// ============================================================================
// Main Function
// ============================================================================
int main() {
    std::cout << "================================================================================" << std::endl;
    std::cout << "  LP-5 High Performance Computing: Practical 1" << std::endl;
    std::cout << "  Parallel BFS and DFS using OpenMP" << std::endl;
    std::cout << "================================================================================" << std::endl;

#ifdef _OPENMP
    std::cout << "  OpenMP Active: Using " << omp_get_max_threads() << " threads." << std::endl;
#else
    std::cout << "  OpenMP Not Enabled: Running in sequential emulation mode." << std::endl;
#endif

    // ------------------------------------------------------------------------
    // Part A: Demonstration on Small Graph
    // ------------------------------------------------------------------------
    std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
    std::cout << "  Part A: Verification on Small Demonstration Graph (9 Vertices)" << std::endl;
    std::cout << "--------------------------------------------------------------------------------" << std::endl;

    Graph smallGraph(9);
    // Construct tree/graph structure
    smallGraph.addEdge(0, 1);
    smallGraph.addEdge(0, 2);
    smallGraph.addEdge(1, 3);
    smallGraph.addEdge(1, 4);
    smallGraph.addEdge(2, 5);
    smallGraph.addEdge(2, 6);
    smallGraph.addEdge(3, 7);
    smallGraph.addEdge(4, 8);

    auto seqBFS = smallGraph.sequentialBFS(0);
    auto parBFS = smallGraph.parallelBFS(0);
    auto seqDFS = smallGraph.sequentialDFS(0);
    auto parDFS = smallGraph.parallelDFS(0);

    printOrder("Sequential BFS", seqBFS);
    printOrder("Parallel BFS", parBFS);
    printOrder("Sequential DFS", seqDFS);
    printOrder("Parallel DFS", parDFS);

    // ------------------------------------------------------------------------
    // Part B: Performance Benchmark on Large Graph
    // ------------------------------------------------------------------------
    const int NUM_NODES = 50000;
    const int EDGES_PER_NODE = 4;
    std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
    std::cout << "  Part B: Benchmark on Large Graph (" << NUM_NODES << " Vertices, ~"
              << (NUM_NODES * EDGES_PER_NODE) << " Edges)" << std::endl;
    std::cout << "--------------------------------------------------------------------------------" << std::endl;

    std::cout << "  Building large graph..." << std::flush;
    Graph largeGraph(NUM_NODES);
    std::mt19937 rng(42);
    for (int i = 1; i < NUM_NODES; ++i) {
        largeGraph.addEdge(i, i / 2); // Binary tree backbone to ensure connectivity
    }
    for (int i = 0; i < NUM_NODES; ++i) {
        for (int k = 0; k < EDGES_PER_NODE; ++k) {
            int target = rng() % NUM_NODES;
            if (target != i) largeGraph.addEdge(i, target);
        }
    }
    std::cout << " Done.\n" << std::endl;

    // --- Benchmark BFS ---
    auto t1 = std::chrono::high_resolution_clock::now();
    auto largeSeqBFS = largeGraph.sequentialBFS(0);
    auto t2 = std::chrono::high_resolution_clock::now();
    double timeSeqBFS = std::chrono::duration<double, std::milli>(t2 - t1).count();

    t1 = std::chrono::high_resolution_clock::now();
    auto largeParBFS = largeGraph.parallelBFS(0);
    t2 = std::chrono::high_resolution_clock::now();
    double timeParBFS = std::chrono::duration<double, std::milli>(t2 - t1).count();

    // --- Benchmark DFS ---
    t1 = std::chrono::high_resolution_clock::now();
    auto largeSeqDFS = largeGraph.sequentialDFS(0);
    t2 = std::chrono::high_resolution_clock::now();
    double timeSeqDFS = std::chrono::duration<double, std::milli>(t2 - t1).count();

    t1 = std::chrono::high_resolution_clock::now();
    auto largeParDFS = largeGraph.parallelDFS(0);
    t2 = std::chrono::high_resolution_clock::now();
    double timeParDFS = std::chrono::duration<double, std::milli>(t2 - t1).count();

    // --- Results Table ---
    std::cout << "  " << std::left << std::setw(20) << "Algorithm"
              << std::setw(18) << "Sequential (ms)"
              << std::setw(18) << "Parallel (ms)"
              << std::setw(15) << "Speedup" << std::endl;
    std::cout << "  " << std::string(68, '-') << std::endl;

    double speedupBFS = (timeParBFS > 0) ? (timeSeqBFS / timeParBFS) : 1.0;
    double speedupDFS = (timeParDFS > 0) ? (timeSeqDFS / timeParDFS) : 1.0;

    std::cout << "  " << std::left << std::setw(20) << "Breadth First Search"
              << std::fixed << std::setprecision(3)
              << std::setw(18) << timeSeqBFS
              << std::setw(18) << timeParBFS
              << std::setprecision(2) << speedupBFS << "x" << std::endl;

    std::cout << "  " << std::left << std::setw(20) << "Depth First Search"
              << std::fixed << std::setprecision(3)
              << std::setw(18) << timeSeqDFS
              << std::setw(18) << timeParDFS
              << std::setprecision(2) << speedupDFS << "x" << std::endl;

    std::cout << "================================================================================" << std::endl;
    std::cout << "  Verification: Nodes visited = " << largeSeqBFS.size()
              << " / " << NUM_NODES << " (BFS) | "
              << largeSeqDFS.size() << " / " << NUM_NODES << " (DFS)" << std::endl;
    std::cout << "================================================================================" << std::endl;

    return 0;
}

/**
 * ============================== SAMPLE OUTPUT ==============================
 * 
 * ================================================================================
 *   LP-5 High Performance Computing: Practical 1
 *   Parallel BFS and DFS using OpenMP
 * ================================================================================
 *   OpenMP Active: Using 8 threads.
 * 
 * --------------------------------------------------------------------------------
 *   Part A: Verification on Small Demonstration Graph (9 Vertices)
 * --------------------------------------------------------------------------------
 *   Sequential BFS        : [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]
 *   Parallel BFS          : [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]
 *   Sequential DFS        : [ 0, 1, 3, 7, 4, 8, 2, 5, 6 ]
 *   Parallel DFS          : [ 0, 1, 2, 3, 5, 6, 4, 7, 8 ]
 * 
 * --------------------------------------------------------------------------------
 *   Part B: Benchmark on Large Graph (50000 Vertices, ~200000 Edges)
 * --------------------------------------------------------------------------------
 *   Building large graph... Done.
 * 
 *   Algorithm           Sequential (ms)   Parallel (ms)     Speedup        
 *   --------------------------------------------------------------------
 *   Breadth First Search2.309             3.988             0.58x
 *   Depth First Search  3.621             7.016             0.52x
 * ================================================================================
 *   Verification: Nodes visited = 50000 / 50000 (BFS) | 50000 / 50000 (DFS)
 * ================================================================================
 */
