/*
 * ==============================================================================
 * LP-5 Practical 5: HPC Application for AI/ML Domain
 * 
 * Problem Statement:
 *   Implement HPC application for AI/ML domain.
 * 
 * Application Description:
 *   Parallel Forward Propagation of a Neural Network Layer (Dense / Linear Layer)
 *   with ReLU Activation using OpenMP.
 *   In AI/ML, forward pass computation Y = ReLU(W * X + B) across batches of
 *   data is the fundamental building block of deep learning models.
 * 
 * How to Compile & Run:
 *   - On Windows (MinGW GCC):
 *       g++ -fopenmp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain.exe
 *       05_hpc_ai_ml_domain.exe
 * 
 *   - On Linux / Ubuntu:
 *       g++ -fopenmp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain
 *       ./05_hpc_ai_ml_domain
 * ==============================================================================
 */

#include <iostream>
#include <vector>
#include <cstdlib>
#include <iomanip>
#include <omp.h>

using namespace std;

// ReLU Activation Function: f(x) = max(0, x)
float relu(float x) {
    return (x > 0.0f) ? x : 0.0f;
}

// -------------------------------------------------------------
// 1. Sequential Forward Pass for Neural Network Layer
// -------------------------------------------------------------
void sequentialForward(const vector<float>& input,
                       const vector<vector<float>>& weights,
                       const vector<float>& bias,
                       vector<float>& output,
                       int inNodes, int outNodes) {
    for (int i = 0; i < outNodes; i++) {
        float sum = bias[i];
        for (int j = 0; j < inNodes; j++) {
            sum += weights[i][j] * input[j];
        }
        output[i] = relu(sum);
    }
}

// -------------------------------------------------------------
// 2. Parallel Forward Pass using OpenMP
// -------------------------------------------------------------
void parallelForward(const vector<float>& input,
                     const vector<vector<float>>& weights,
                     const vector<float>& bias,
                     vector<float>& output,
                     int inNodes, int outNodes) {
    // Parallelize computation across output neurons
    #pragma omp parallel for
    for (int i = 0; i < outNodes; i++) {
        float sum = bias[i];
        for (int j = 0; j < inNodes; j++) {
            sum += weights[i][j] * input[j];
        }
        output[i] = relu(sum);
    }
}

int main() {
    cout << "=================================================" << endl;
    cout << "  LP-5 Practical 5: HPC in AI/ML (Neural Net Layer)" << endl;
    cout << "=================================================" << endl;

    // Part 1: Small Demonstration (4 Input Neurons -> 4 Output Neurons)
    int inNodes = 4;
    int outNodes = 4;

    vector<float> input = {0.5f, -0.2f, 0.8f, 0.1f};
    vector<float> bias = {0.1f, 0.2f, -0.5f, 0.0f};

    vector<vector<float>> weights = {
        { 0.2f,  0.8f, -0.5f,  1.0f},
        { 0.5f, -0.3f,  0.2f, -0.1f},
        {-0.4f,  0.1f,  0.9f,  0.4f},
        { 0.7f,  0.6f, -0.2f,  0.3f}
    };

    vector<float> outputSeq(outNodes);
    vector<float> outputPar(outNodes);

    sequentialForward(input, weights, bias, outputSeq, inNodes, outNodes);
    parallelForward(input, weights, bias, outputPar, inNodes, outNodes);

    cout << "Input Feature Vector X: ";
    for (float val : input) cout << fixed << setprecision(2) << val << " ";
    cout << endl;

    cout << "\nSequential Output Neurons (after ReLU): ";
    for (float val : outputSeq) cout << fixed << setprecision(4) << val << " ";
    cout << endl;

    cout << "Parallel Output Neurons   (after ReLU): ";
    for (float val : outputPar) cout << fixed << setprecision(4) << val << " ";
    cout << endl;

    // Part 2: Large Scale AI/ML Batch Performance (2000 Neurons x 2000 Inputs)
    int bigIn = 2000;
    int bigOut = 2000;

    vector<float> bigInput(bigIn, 0.5f);
    vector<float> bigBias(bigOut, 0.1f);
    vector<vector<float>> bigWeights(bigOut, vector<float>(bigIn, 0.01f));
    vector<float> bigOutputSeq(bigOut);
    vector<float> bigOutputPar(bigOut);

    cout << "\n--- Large Scale Layer Performance (" << bigIn << " inputs -> " << bigOut << " outputs) ---" << endl;

    double start = omp_get_wtime();
    sequentialForward(bigInput, bigWeights, bigBias, bigOutputSeq, bigIn, bigOut);
    double end = omp_get_wtime();
    cout << "Sequential Inference Time: " << fixed << setprecision(3) << (end - start) * 1000 << " ms" << endl;

    start = omp_get_wtime();
    parallelForward(bigInput, bigWeights, bigBias, bigOutputPar, bigIn, bigOut);
    end = omp_get_wtime();
    cout << "Parallel Inference Time  : " << fixed << setprecision(3) << (end - start) * 1000 << " ms" << endl;

    // Verify outputs match
    bool match = true;
    for (int i = 0; i < bigOut; i++) {
        if (bigOutputSeq[i] != bigOutputPar[i]) {
            match = false;
            break;
        }
    }
    cout << "Verification: " << (match ? "PASSED (Outputs match)" : "FAILED") << endl;

    cout << "=================================================" << endl;
    return 0;
}

/*
============================== SAMPLE OUTPUT ==============================
=================================================
  LP-5 Practical 5: HPC in AI/ML (Neural Net Layer)
=================================================
Input Feature Vector X: 0.50 -0.20 0.80 0.10 

Sequential Output Neurons (after ReLU): 0.0000 0.6600 0.0400 0.1000 
Parallel Output Neurons   (after ReLU): 0.0000 0.6600 0.0400 0.1000 

--- Large Scale Layer Performance (2000 inputs -> 2000 outputs) ---
Sequential Inference Time: 6.432 ms
Parallel Inference Time  : 1.360 ms
Verification: PASSED (Outputs match)
=================================================
===========================================================================
*/
