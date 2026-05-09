# AprioriX-FIM-Optimization

**A comprehensive comparison of classical Apriori with optimized Frequent Itemset Mining techniques and 2022+ SOTA algorithms.**

![Status](https://img.shields.io/badge/Status-Completed-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Academic-green)

## 📋 Project Overview

This project implements and compares three primary approaches to Frequent Itemset Mining (FIM):
- **Classical Apriori Algorithm** (Baseline, horizontal format)
- **Optimized Vertical Apriori** (Vertical data format with TID-list intersections - Eclat style)
- **High-Utility Itemset Mining (HUIM)** (2022+ State-of-the-Art algorithm)

Developed for the CS-378 Design and Analysis of Algorithms course, this project demonstrates algorithmic design principles, complexity analysis, and rigorous empirical evaluation using real-world benchmark datasets.

## 🚀 Key Features

- ✅ **2022+ Algorithm**: Implementation of High-Utility Itemset Mining (HUIM) for weighted pattern discovery.
- ✅ **Optimized Evaluation**: Multi-run averaging (3 runs) for scientific accuracy and noise reduction.
- ✅ **Real-World Data**: Integration of standard FIMI benchmarks (Chess, Connect, Accidents) and Online Retail data.
- ✅ **Vertical Format**: Reduced I/O overhead by switching from database scans to set intersections.
- ✅ **Visualization**: Automated generation of scalability curves for time and memory metrics.

## 📁 Project Structure

```
AprioriX-FIM-Optimization/
├── src/                            # Source code
│   ├── apriori.py                 # Classical Apriori (Baseline)
│   ├── optimized_apriori.py       # Vertical format optimization
│   ├── huim_algorithm.py          # 2022+ SOTA Algorithm
│   ├── evaluate.py                # Benchmarking suite (3-run averaging)
│   └── visualize.py               # Plotting and visualization
├── datasets/                       # Real-world FIMI benchmarks (.dat & .txt)
├── report/                         # IEEE format research report
├── results/                        # Benchmark outputs and PNG plots
├── HANDOVER.md                    # Detailed project documentation ⭐
└── README.md                      # This file
```

## 📊 Performance Highlights

**Real-World Benchmark (Chess Dataset):**

| Algorithm | Support | Avg Execution Time | Speedup |
|-----------|---------|--------------------|---------|
| Classical Apriori | 90% | 0.350s | 1.00x |
| **Optimized (Vertical)** | 90% | 0.170s | **2.06x** |
| HUIM (2022+ SOTA) | 90% | 34.39s | 0.01x* |

*\*HUIM overhead is due to utility-weighted calculation logic vs. standard binary frequency.*

## 📖 Documentation

- **[PROJECT_ANALYSIS.md](PROJECT_ANALYSIS.md)** - Full audit and completion roadmap.
- **[HANDOVER.md](HANDOVER.md)** - Implementation details and architecture.
- **[HUIM_ALGORITHM_DOCUMENTATION.md](HUIM_ALGORITHM_DOCUMENTATION.md)** - Technical details of the 2022+ SOTA algorithm.
- **[report/main.md](report/main.md)** - The final IEEE Conference Report.

## 🛠️ Installation & Usage

1. **Clone**: `git clone https://github.com/AmmarRiaz123/AprioriX-FIM-Optimization.git`
2. **Setup**: `pip install -r requirements.txt`
3. **Benchmark**: `python src/evaluate.py`
4. **Visualize**: `python src/visualize.py`

---

## 👥 Team

- **Muhammad Ammar Riaz**
- **Hashir Awaiz**
- **Hamza Elahi**
- **Taaha Shabbir**

**Course:** CS-378: Design and Analysis of Algorithms  
**University:** GIKI  
**Date:** May 2026
