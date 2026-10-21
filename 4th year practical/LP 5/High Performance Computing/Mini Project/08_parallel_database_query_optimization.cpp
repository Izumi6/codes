/*
 * LP-5 High Performance Computing - Mini Project 8
 * Parallelization of Database Query Optimization
 *
 * Problem Statement:
 * Implement Parallelization of Database Query optimization.
 *
 * Compilation & Execution:
 *   Linux / Windows (with OpenMP):
 *     g++ -std=c++17 -O2 -fopenmp 08_parallel_database_query_optimization.cpp -o db_opt
 *     ./db_opt
 *   macOS (Clang++):
 *     clang++ -std=c++17 -O2 08_parallel_database_query_optimization.cpp -o db_opt
 *     ./db_opt
 *
 * Sample Output:
 * Records Processed: 500000 orders
 * Sequential Query Time: 5.53 ms
 * Parallel Query Time: 2.15 ms
 * Speedup Factor: 2.57x
 *
 * Query Aggregation Results (by Region):
 * Region 1 -> Count: 17398, Total Sales: $17458619, Avg: $1003
 * Region 2 -> Count: 17107, Total Sales: $17066769, Avg: $997
 * Region 3 -> Count: 17006, Total Sales: $16988632, Avg: $998
 * Region 4 -> Count: 17407, Total Sales: $17412472, Avg: $1000
 * Region 5 -> Count: 17246, Total Sales: $17294785, Avg: $1002
 */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <chrono>
#include <random>
#include <iomanip>

#ifdef _OPENMP
#include <omp.h>
#else
inline int omp_get_max_threads() { return 4; }
inline int omp_get_thread_num() { return 0; }
inline double omp_get_wtime() {
    auto now = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double>(now.time_since_epoch()).count();
}
#endif

// Database Table Schema 1: Orders (Fact Table)
struct Order {
    int order_id;
    int customer_id;
    int region_id;
    double amount;
    int status; // 1 = Completed
};

// Database Table Schema 2: Customers (Dimension Table)
struct Customer {
    int customer_id;
    int tier; // 1 = VIP, 2 = Regular
};

// Aggregation Result Bucket
struct AggResult {
    long long count = 0;
    double total_amount = 0.0;
};

int main() {
    const int NUM_ORDERS = 500000;
    const int NUM_CUSTOMERS = 10000;
    const int NUM_REGIONS = 5;

    std::vector<Order> orders(NUM_ORDERS);
    std::vector<Customer> customers(NUM_CUSTOMERS);

    // Populate database tables with realistic benchmark data
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> cust_dist(1, NUM_CUSTOMERS);
    std::uniform_int_distribution<int> region_dist(1, NUM_REGIONS);
    std::uniform_real_distribution<double> amt_dist(50.0, 1500.0);
    std::uniform_int_distribution<int> status_dist(0, 1);

    for (int i = 0; i < NUM_ORDERS; ++i) {
        orders[i] = {i + 1, cust_dist(rng), region_dist(rng), amt_dist(rng), status_dist(rng)};
    }
    for (int i = 0; i < NUM_CUSTOMERS; ++i) {
        customers[i] = {i + 1, (i % 2 == 0) ? 1 : 2};
    }

    // Build Hash Index for Customer Dimension Table
    std::unordered_map<int, int> customer_hash_table;
    customer_hash_table.reserve(NUM_CUSTOMERS);
    for (const auto& c : customers) {
        customer_hash_table[c.customer_id] = c.tier;
    }

    // --- Query Plan 1: Sequential Query Execution ---
    // SELECT region_id, COUNT(*), SUM(amount) FROM orders JOIN customers
    // WHERE orders.status == 1 AND orders.amount > 500 AND customers.tier == 1 GROUP BY region_id;
    double t_seq_start = omp_get_wtime();
    std::vector<AggResult> seq_agg(NUM_REGIONS + 1);

    for (int i = 0; i < NUM_ORDERS; ++i) {
        if (orders[i].status == 1 && orders[i].amount > 500.0) {
            auto it = customer_hash_table.find(orders[i].customer_id);
            if (it != customer_hash_table.end() && it->second == 1) {
                int r = orders[i].region_id;
                seq_agg[r].count++;
                seq_agg[r].total_amount += orders[i].amount;
            }
        }
    }
    double t_seq_end = omp_get_wtime();
    double seq_ms = (t_seq_end - t_seq_start) * 1000.0;

    // --- Query Plan 2: Parallel Query Optimization (OpenMP Multithreading) ---
    double t_par_start = omp_get_wtime();
    int threads = omp_get_max_threads();
    std::vector<std::vector<AggResult>> local_aggs(threads, std::vector<AggResult>(NUM_REGIONS + 1));

    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        #pragma omp for
        for (int i = 0; i < NUM_ORDERS; ++i) {
            if (orders[i].status == 1 && orders[i].amount > 500.0) {
                auto it = customer_hash_table.find(orders[i].customer_id);
                if (it != customer_hash_table.end() && it->second == 1) {
                    int r = orders[i].region_id;
                    local_aggs[tid][r].count++;
                    local_aggs[tid][r].total_amount += orders[i].amount;
                }
            }
        }
    }

    // Merge Thread-Local Aggregation Buckets
    std::vector<AggResult> par_agg(NUM_REGIONS + 1);
    for (int tid = 0; tid < threads; ++tid) {
        for (int r = 1; r <= NUM_REGIONS; ++r) {
            par_agg[r].count += local_aggs[tid][r].count;
            par_agg[r].total_amount += local_aggs[tid][r].total_amount;
        }
    }
    double t_par_end = omp_get_wtime();
    double par_ms = (t_par_end - t_par_start) * 1000.0;

    // Display Performance Results
    double speedup = seq_ms / par_ms;

    std::cout << "Records Processed: " << NUM_ORDERS << " orders" << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Sequential Query Time: " << seq_ms << " ms" << std::endl;
    std::cout << "Parallel Query Time:   " << par_ms << " ms" << std::endl;
    std::cout << "Speedup Factor:        " << speedup << "x" << std::endl;

    std::cout << "\nQuery Aggregation Results (by Region):" << std::endl;
    for (int r = 1; r <= NUM_REGIONS; ++r) {
        double avg = par_agg[r].count > 0 ? (par_agg[r].total_amount / par_agg[r].count) : 0.0;
        std::cout << "Region " << r << " -> Count: " << par_agg[r].count
                  << ", Total Sales: $" << (long long)par_agg[r].total_amount
                  << ", Avg: $" << (int)avg << std::endl;
    }

    return 0;
}
