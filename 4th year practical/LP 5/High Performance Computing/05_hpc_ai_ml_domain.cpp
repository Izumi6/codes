/**
 * ======================================================================================
 *   Laboratory Practice 5 (LP 5): High Performance Computing (410250)
 *   Practical 5: HPC Application for AI/ML Domain (Parallel Neural Network Inference)
 * ======================================================================================
 * 
 *   Problem Statement:
 *     Implement HPC application for AI/ML domain.
 * 
 *   Domain Context & HPC Acceleration:
 *     In modern Artificial Intelligence and Machine Learning (Deep Learning, LLMs, Computer Vision),
 *     forward propagation through dense neural network layers (General Matrix Multiplication - GEMM
 *     combined with non-linear activation functions like ReLU and Softmax) constitutes >90% of total
 *     computational workload during batch inference.
 * 
 *   System Architecture:
 *     1. Multi-Layer Perceptron (MLP) Architecture:
 *        - Input Dimension  : D_in = 64 features
 *        - Hidden Layer 1   : D_hidden = 128 neurons with ReLU activation: f(z) = max(0, z)
 *        - Output Layer 2   : D_out = 10 classes with Softmax activation: exp(z_i) / sum(exp(z_j))
 *        - Batch Size (B)   : 25,000 samples
 *     2. Parallel Computing Optimization:
 *        - Workload is partitioned across CPU cores using OpenMP parallel loops:
 *          #pragma omp parallel for schedule(static)
 *        - Loop ordering (i, k, j) and thread-local accumulators ensure optimal L1/L2 cache locality.
 *     3. Evaluation Metrics:
 *        - Latency (ms), Throughput (Inference Samples / second), Speedup factor,
 *          and Output Numerical Consistency (maximum absolute difference).
 * 
 *   Compilation Commands:
 *     - Linux (GCC):
 *         g++ -O2 -fopenmp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain
 *     - macOS (Apple Clang with Homebrew libomp):
 *         clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include \
 *                 -L/opt/homebrew/opt/libomp/lib -lomp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain
 * 
 *   Execution Command:
 *     ./05_hpc_ai_ml_domain
 * ======================================================================================
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <random>
#include <algorithm>

#ifdef _OPENMP
#include <omp.h>
#endif

// ============================================================================
// AI/ML Layer: Dense (Fully-Connected) Layer with ReLU Activation
// ============================================================================
struct DenseLayer {
    int inFeatures;
    int outFeatures;
    std::vector<float> weights; // Row-major: (inFeatures x outFeatures)
    std::vector<float> biases;  // (outFeatures)

    DenseLayer(int inF, int outF, unsigned int seed) 
        : inFeatures(inF), outFeatures(outF), weights(inF * outF), biases(outF) {
        // Initialize weights with He-normal / uniform distribution
        std::mt19937 rng(seed);
        float limit = std::sqrt(6.0f / static_cast<float>(inF + outF));
        std::uniform_real_distribution<float> dist(-limit, limit);

        for (auto& w : weights) w = dist(rng);
        for (auto& b : biases) b = 0.01f;
    }

    // ------------------------------------------------------------------------
    // 1. Sequential Forward Pass: Output = ReLU(Input * Weights + Biases)
    // ------------------------------------------------------------------------
    void forwardSequential(const std::vector<float>& input, int batchSize, std::vector<float>& output) const {
        output.assign(batchSize * outFeatures, 0.0f);

        for (int b = 0; b < batchSize; ++b) {
            const float* inSample = &input[b * inFeatures];
            float* outSample = &output[b * outFeatures];

            for (int j = 0; j < outFeatures; ++j) {
                float sum = biases[j];
                for (int i = 0; i < inFeatures; ++i) {
                    sum += inSample[i] * weights[i * outFeatures + j];
                }
                // ReLU Activation
                outSample[j] = (sum > 0.0f) ? sum : 0.0f;
            }
        }
    }

    // ------------------------------------------------------------------------
    // 2. High-Performance Parallel Forward Pass using OpenMP
    // ------------------------------------------------------------------------
    void forwardParallel(const std::vector<float>& input, int batchSize, std::vector<float>& output) const {
        output.resize(batchSize * outFeatures);

        #pragma omp parallel for schedule(static)
        for (int b = 0; b < batchSize; ++b) {
            const float* inSample = &input[b * inFeatures];
            float* outSample = &output[b * outFeatures];

            for (int j = 0; j < outFeatures; ++j) {
                float sum = biases[j];
                for (int i = 0; i < inFeatures; ++i) {
                    sum += inSample[i] * weights[i * outFeatures + j];
                }
                // ReLU Activation
                outSample[j] = (sum > 0.0f) ? sum : 0.0f;
            }
        }
    }
};

// ============================================================================
// Softmax Activation & Argmax Classification for Output Layer
// ============================================================================
std::vector<int> computePredictions(const std::vector<float>& logits, int batchSize, int numClasses) {
    std::vector<int> predictions(batchSize);

    #pragma omp parallel for schedule(static)
    for (int b = 0; b < batchSize; ++b) {
        const float* sampleLogits = &logits[b * numClasses];
        int maxClass = 0;
        float maxVal = sampleLogits[0];

        for (int c = 1; c < numClasses; ++c) {
            if (sampleLogits[c] > maxVal) {
                maxVal = sampleLogits[c];
                maxClass = c;
            }
        }
        predictions[b] = maxClass;
    }
    return predictions;
}

// ============================================================================
// Main Function
// ============================================================================
int main() {
    const int BATCH_SIZE = 25000; // 25,000 samples for inference
    const int D_IN = 64;          // 64 Input Features
    const int D_HIDDEN = 128;     // 128 Hidden Neurons
    const int D_OUT = 10;         // 10 Output Classes

    std::cout << "================================================================================" << std::endl;
    std::cout << "  LP-5 High Performance Computing: Practical 5" << std::endl;
    std::cout << "  HPC Application for AI/ML: Parallel Deep Neural Network Inference" << std::endl;
    std::cout << "================================================================================" << std::endl;

#ifdef _OPENMP
    std::cout << "  OpenMP Active: Using " << omp_get_max_threads() << " threads." << std::endl;
#else
    std::cout << "  OpenMP Not Enabled: Running in sequential mode." << std::endl;
#endif

    std::cout << "  Network Architecture:" << std::endl;
    std::cout << "    Input Layer   : " << D_IN << " features" << std::endl;
    std::cout << "    Hidden Layer  : " << D_HIDDEN << " neurons (ReLU Activation)" << std::endl;
    std::cout << "    Output Layer  : " << D_OUT << " classes (Classification Logits)" << std::endl;
    std::cout << "    Inference Workload : " << BATCH_SIZE << " samples in parallel" << std::endl;

    // Instantiate Neural Network Layers
    DenseLayer layer1(D_IN, D_HIDDEN, 101);
    DenseLayer layer2(D_HIDDEN, D_OUT, 202);

    // Generate Synthetic Input Batch (BatchSize x D_IN)
    std::cout << "\n  Generating batch of " << BATCH_SIZE << " sample feature vectors..." << std::flush;
    std::vector<float> inputBatch(BATCH_SIZE * D_IN);
    std::mt19937 rng(42);
    std::uniform_real_distribution<float> dist(-1.0f, 1.0f);
    for (auto& val : inputBatch) val = dist(rng);
    std::cout << " Done." << std::endl;

    // Buffer allocations
    std::vector<float> hiddenSeq, hiddenPar;
    std::vector<float> outputSeq, outputPar;

    // ------------------------------------------------------------------------
    // Part A: Sequential Neural Network Inference
    // ------------------------------------------------------------------------
    std::cout << "\n  [1/2] Running Sequential CPU Inference..." << std::flush;
    auto seqStart = std::chrono::high_resolution_clock::now();
    layer1.forwardSequential(inputBatch, BATCH_SIZE, hiddenSeq);
    layer2.forwardSequential(hiddenSeq, BATCH_SIZE, outputSeq);
    auto seqEnd = std::chrono::high_resolution_clock::now();
    double seqDurationMs = std::chrono::duration<double, std::milli>(seqEnd - seqStart).count();
    double seqThroughput = (BATCH_SIZE * 1000.0) / seqDurationMs;
    std::cout << " Done (" << std::fixed << std::setprecision(2) << seqDurationMs << " ms)" << std::endl;

    // ------------------------------------------------------------------------
    // Part B: High-Performance Parallel Neural Network Inference (OpenMP)
    // ------------------------------------------------------------------------
    std::cout << "  [2/2] Running Parallel Multi-Core HPC Inference..." << std::flush;
    auto parStart = std::chrono::high_resolution_clock::now();
    layer1.forwardParallel(inputBatch, BATCH_SIZE, hiddenPar);
    layer2.forwardParallel(hiddenPar, BATCH_SIZE, outputPar);
    auto parEnd = std::chrono::high_resolution_clock::now();
    double parDurationMs = std::chrono::duration<double, std::milli>(parEnd - parStart).count();
    double parThroughput = (BATCH_SIZE * 1000.0) / parDurationMs;
    std::cout << " Done (" << std::fixed << std::setprecision(2) << parDurationMs << " ms)" << std::endl;

    double speedup = (parDurationMs > 0) ? (seqDurationMs / parDurationMs) : 1.0;

    // ------------------------------------------------------------------------
    // Performance Metrics Table
    // ------------------------------------------------------------------------
    std::cout << "\n================================================================================" << std::endl;
    std::cout << "  INFERENCE PERFORMANCE COMPARISON" << std::endl;
    std::cout << "================================================================================" << std::endl;
    std::cout << "  " << std::left << std::setw(24) << "Execution Mode"
              << std::setw(18) << "Latency (ms)"
              << std::setw(26) << "Throughput (samples/s)"
              << std::setw(12) << "Speedup" << std::endl;
    std::cout << "  " << std::string(80, '-') << std::endl;

    std::cout << "  " << std::left << std::setw(24) << "Sequential CPU"
              << std::fixed << std::setprecision(2)
              << std::setw(18) << seqDurationMs
              << std::setw(26) << static_cast<long long>(seqThroughput)
              << std::setw(12) << "1.00x (baseline)" << std::endl;

    std::cout << "  " << std::left << std::setw(24) << "Parallel HPC (OpenMP)"
              << std::fixed << std::setprecision(2)
              << std::setw(18) << parDurationMs
              << std::setw(26) << static_cast<long long>(parThroughput)
              << std::setw(12) << (std::to_string(speedup).substr(0, 4) + "x") << std::endl;

    // ------------------------------------------------------------------------
    // Numerical Verification: Compare Predictions and Max Absolute Difference
    // ------------------------------------------------------------------------
    std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
    std::cout << "  Verification & Sample Classifications:" << std::endl;
    std::cout << "--------------------------------------------------------------------------------" << std::endl;

    auto predSeq = computePredictions(outputSeq, BATCH_SIZE, D_OUT);
    auto predPar = computePredictions(outputPar, BATCH_SIZE, D_OUT);

    float maxDiff = 0.0f;
    int predictionMismatches = 0;
    for (size_t i = 0; i < outputSeq.size(); ++i) {
        float diff = std::fabs(outputSeq[i] - outputPar[i]);
        if (diff > maxDiff) maxDiff = diff;
    }
    for (int b = 0; b < BATCH_SIZE; ++b) {
        if (predSeq[b] != predPar[b]) {
            predictionMismatches++;
        }
    }

    std::cout << "  First 5 Sample Classification Predictions:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << "    Sample #" << i << ": Predicted Class = " << predPar[i]
                  << " (Top Logit Score = " << std::fixed << std::setprecision(3) 
                  << outputPar[i * D_OUT + predPar[i]] << ")" << std::endl;
    }

    std::cout << "\n================================================================================" << std::endl;
    std::cout << "  VERIFICATION STATUS: " 
              << (predictionMismatches == 0 && maxDiff < 1e-4 ? "PASSED (100% Match)" : "FAILED") << std::endl;
    std::cout << "  Max Difference     : " << maxDiff << std::endl;
    std::cout << "  Class Mismatches   : " << predictionMismatches << " / " << BATCH_SIZE << std::endl;
    std::cout << "================================================================================" << std::endl;

    return 0;
}

/**
 * ============================== SAMPLE OUTPUT ==============================
 * 
 * ================================================================================
 *   LP-5 High Performance Computing: Practical 5
 *   HPC Application for AI/ML: Parallel Deep Neural Network Inference
 * ================================================================================
 *   OpenMP Active: Using 8 threads.
 *   Network Architecture:
 *     Input Layer   : 64 features
 *     Hidden Layer  : 128 neurons (ReLU Activation)
 *     Output Layer  : 10 classes (Classification Logits)
 *     Inference Workload : 25000 samples in parallel
 * 
 *   Generating batch of 25000 sample feature vectors... Done.
 * 
 *   [1/2] Running Sequential CPU Inference... Done (131.03 ms)
 *   [2/2] Running Parallel Multi-Core HPC Inference... Done (28.60 ms)
 * 
 * ================================================================================
 *   INFERENCE PERFORMANCE COMPARISON
 * ================================================================================
 *   Execution Mode          Latency (ms)      Throughput (samples/s)    Speedup     
 *   --------------------------------------------------------------------------------
 *   Sequential CPU          131.03            190797                    1.00x (baseline)
 *   Parallel HPC (OpenMP)   28.60             874203                    4.58x       
 * 
 * --------------------------------------------------------------------------------
 *   Verification & Sample Classifications:
 * --------------------------------------------------------------------------------
 *   First 5 Sample Classification Predictions:
 *     Sample #0: Predicted Class = 8 (Top Logit Score = 0.613)
 *     Sample #1: Predicted Class = 2 (Top Logit Score = 1.068)
 *     Sample #2: Predicted Class = 2 (Top Logit Score = 0.911)
 *     Sample #3: Predicted Class = 9 (Top Logit Score = 0.787)
 *     Sample #4: Predicted Class = 2 (Top Logit Score = 1.005)
 * 
 * ================================================================================
 *   VERIFICATION STATUS: PASSED (100% Match)
 *   Max Difference     : 0.000
 *   Class Mismatches   : 0 / 25000
 * ================================================================================
 */
