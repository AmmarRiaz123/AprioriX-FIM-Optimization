# Final Project Implementation Summary

This document maps the project implementation to the official requirements provided in the course brief.

### 1. Algorithms Implemented
*   **Classical Apriori (`src/apriori.py`)**: The foundational baseline using horizontal database scans and candidate generation.
*   **Vertical Optimized Apriori (`src/optimized_apriori.py`)**: Implements **TID-list intersections** to eliminate database scans, achieving significant speedups on dense datasets.
*   **2022+ SOTA Algorithm (`src/huim_algorithm.py`)**: Implements **High-Utility Itemset Mining (HUIM)**, a contemporary evolution of FIM focusing on utility/profit-weighted pattern discovery.

### 2. Benchmarking Suite (`src/evaluate.py`)
*   **Averaging**: Automatically runs each experiment **3 times** and reports the mean and standard deviation.
*   **Metrics**: Captures Wall-clock time (seconds), Peak Memory Delta (MB), Candidate counts, and Speedup ratios.
*   **Real-World Data**: Validated against standard FIMI benchmarks (Chess, Connect, Accidents) and Online Retail CSV data.

### 3. Visualization (`src/visualize.py`)
*   Generates **Scalability Curves** (PNG plots) automatically from the benchmark JSON results, facilitating the "Analytical Discussion" required by the IEEE format.

### 4. IEEE Conference Report (`report/main.md`)
*   A complete research paper following the double-column format.
*   Includes **9 professional citations**, full **Complexity Analysis**, and **Pseudocode** for all three algorithmic approaches.
*   Contains a dedicated **Author Contributions** section as per course requirements.

### 5. Final Results Snapshot (Chess @ 90% Support)
*   **Baseline Apriori**: 0.35s (Avg)
*   **Vertical Optimized**: 0.17s (Avg) -> **2.06x Speedup**
*   **HUIM**: Integrated for utility-aware analysis.

---
**Status: READY FOR SUBMISSION**
**Team:** Muhammad Ammar Riaz, Hashir Awaiz, Hamza Elahi, Taaha Shabbir
