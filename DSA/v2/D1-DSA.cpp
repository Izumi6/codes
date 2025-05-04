
#include <iostream>
#include <climits>
using namespace std;

// Function to compute sum of frequencies using prefix sum array
int sum(int prefix[], int i, int j) {
    if (i == 0)
        return prefix[j];
    return prefix[j] - prefix[i - 1];
}

// Function to construct the Optimal BST
int optimalSearchTree(int keys[], int freq[], int n) {
    int cost[n][n];  // cost[i][j] stores the optimal cost for keys[i..j]

    // Compute prefix sum array to calculate frequency sum efficiently
    int prefix[n];
    prefix[0] = freq[0];
    for (int i = 1; i < n; i++)
        prefix[i] = prefix[i - 1] + freq[i];

    // Initialize cost[i][i]
    for (int i = 0; i < n; i++)
        cost[i][i] = freq[i];

    // Fill the cost matrix
    for (int L = 2; L <= n; L++) { // L is the chain length
        for (int i = 0; i <= n - L; i++) {
            int j = i + L - 1;
            cost[i][j] = INT_MAX;

            // Try all keys from i to j as root
            for (int r = i; r <= j; r++) {
                int left = (r > i) ? cost[i][r - 1] : 0;
                int right = (r < j) ? cost[r + 1][j] : 0;
                int totalFreq = sum(prefix, i, j);
                int c = left + right + totalFreq;

                if (c < cost[i][j])
                    cost[i][j] = c;
            }
        }
    }

    // The result is the minimum cost for the full range of keys
    return cost[0][n - 1];
}

int main() {
    int number_of_keys;
    cout << "\nEnter number of keys : ";
    cin >> number_of_keys;

    int keys[number_of_keys];
    int freq[number_of_keys];

    for (int i = 0; i < number_of_keys; ++i) {
        cout << "Enter key and frequency : ";
        cin >> keys[i] >> freq[i];
    }

    int cost = optimalSearchTree(keys, freq, number_of_keys);
    cout << "\nCost of Optimal BST : " << cost << "\n";

    return 0;
}
