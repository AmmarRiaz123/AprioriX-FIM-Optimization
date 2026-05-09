# Project Handover Documentation (COMPLETED)

**Project Name:** AprioriX-FIM-Optimization  
**Course:** CS-378 Design and Analysis of Algorithms  
**Semester:** Spring 2026  
**Status:** ✅ 100% Complete & Ready for Submission

---

## 1. Project Objective
This project rigorously analyzes and compares the performance of the classical **Apriori algorithm** against modern optimizations and a contemporary **2022+ State-of-the-Art (SOTA) algorithm**. We implemented two primary optimizations: **Vertical Data Formatting (TID-lists)** and **Transaction Pruning**, while selecting **High-Utility Itemset Mining (HUIM)** as our 2022+ algorithmic comparison.

## 2. Implementation Overview

### A. Algorithms (`src/`)
*   **`apriori.py`**: Classical Apriori using horizontal database scans and candidate generation.
*   **`optimized_apriori.py`**: Eclat-inspired Vertical Apriori using TID-list intersections.
*   **`huim_algorithm.py`**: 2022+ SOTA algorithm focusing on utility-weighted pattern discovery.

### B. Benchmarking Suite (`src/evaluate.py`)
*   **3-Run Averaging**: Every metric is averaged across three independent runs to ensure scientific accuracy.
*   **Metric Tracking**: Captures Wall-clock time, Peak Memory Delta, Candidate counts, and Frequent itemset totals.
*   **Real Data Integration**: Benchmarks conducted on official FIMI datasets: **Chess, Connect, Accidents**, and the real-world **Online Retail** dataset.

### C. Research Report (`report/main.md`)
*   A full IEEE double-column conference paper.
*   Includes **Abstract, Introduction, Literature Review (9+ citations), Algorithm Analysis (Pseudocode + Complexity), Experimental Results, Discussion, and Conclusion**.
*   Contains the required **Author Contributions** and **Workload Distribution** section.

## 3. Results Summary
Our benchmarking revealed that the **Vertical Optimized Apriori** achieved a **2.06x speedup** on dense datasets (Chess) by transitioning from I/O-intensive database scans to memory-efficient set intersections. While **HUIM** introduces computational overhead on binary data, it provides significantly deeper actionable insights for utility-weighted scenarios.

## 4. How to Reproduce Results
1.  Ensure all dependencies are installed: `pip install -r requirements.txt`.
2.  Run the full benchmark suite: `python src/evaluate.py`.
3.  Generate the scalability curves: `python src/visualize.py`.
4.  Final plots will be available in `results/plots/`.

## 5. Team Composition
*   **Muhammad Ammar Riaz**: HUIM Implementation & Evaluation Suite.
*   **Hashir Awaiz**: Classical Apriori & Dataset Pre-processing.
*   **Hamza Elahi**: Complexity Analysis & IEEE Report Drafting.
*   **Taaha Shabbir**: Result Visualization & Data Analysis.

---
**Finalized on:** May 10, 2026
