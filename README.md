# AprioriX-FIM-Optimization

**A comprehensive comparison of classical Apriori with optimized Frequent Itemset Mining techniques**

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Academic-green)

## 📋 Quick Overview

This project implements and compares two approaches to Frequent Itemset Mining (FIM):
- **Classical Apriori Algorithm** (baseline, horizontal format)
- **Optimized Apriori** (vertical data format with TID-list intersections)

Perfect for: CS-378 Algorithms course project, data mining education, performance benchmarking

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repo-url>
cd AprioriX-FIM-Optimization
python -m venv .venv
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Generate Datasets
```bash
cd src
python ../scripts/generate_datasets.py
```

### 3. Run Benchmarks
```bash
python evaluate.py
```

### 4. Check Results
```
Benchmarking dataset: ../datasets/chess.dat with min_sup=0.40
-- Running Baseline Apriori --
Time: 0.0049s | Memory: 0.00 MB | Candidate Count: X
-- Running Optimized Apriori (Vertical Format) --
Time: 0.1472s | Memory: 0.07 MB
Speedup achieved: 3.41x
```

## 📁 Project Structure

```
AprioriX-FIM-Optimization/
├── src/                            # Source code
│   ├── apriori.py                 # Classical Apriori
│   ├── optimized_apriori.py       # Vertical format optimization
│   ├── evaluate.py                # Benchmarking script
│   └── datasets/                  # Test data
├── report/                         # IEEE format research report
├── scripts/                        # Utilities (dataset generation)
├── results/                        # Benchmark outputs
├── HANDOVER.md                    # Detailed project documentation ⭐
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🔍 What's Implemented

### ✅ Classical Apriori (`src/apriori.py`)
- BFS-based candidate generation
- Anti-monotonic pruning
- Full database scans for support counting
- Returns all frequent itemsets by level

### ✅ Optimized Vertical Format (`src/optimized_apriori.py`)
- Converts horizontal (transaction) data to vertical (TID-list) format
- Counts support via set intersection (no full DB scans)
- Transaction reduction optimization
- Memory-time trade-off for dense datasets

### ✅ Comprehensive Benchmarking (`src/evaluate.py`)
- Measures execution time and memory usage
- Calculates speedup ratios
- Tests multiple support thresholds
- Works with multiple datasets

### ✅ Report Template (`report/`)
- IEEE conference paper format
- Sections for algorithms, complexity analysis, experiments, results
- Ready for results and conclusions

## 📊 Current Results

**Synthetic Dataset Benchmarks:**

| Dataset | Support | Apriori | Optimized | Speedup |
|---------|---------|---------|-----------|---------|
| Chess (3K tx) | 40% | 0.0049s | 0.1472s | 0.29x |
| Chess | 20% | 0.0368s | 3.2527s | 0.11x |
| Chess | 10% | 0.0337s | 206.3s | 0.0002x |

**Note:** Vertical format performs better on sparse datasets. Current synthetic data is too dense.

## 🔧 Configuration

Edit `.env` for:
- Dataset paths and parameters
- Support thresholds to test
- Memory/time profiling options
- Output format preferences
- Report configuration

See `.env.example` for all available options.

## 📖 Documentation

**For detailed information, see:**
- **[HANDOVER.md](HANDOVER.md)** - Complete project documentation, setup guide, results analysis, and remaining tasks
- **[ProjectDescDoc.md](ProjectDescDoc.md)** - Original project requirements

## 🎯 Remaining Tasks

- [ ] Obtain real FIMI datasets (current data is synthetic)
- [ ] Fix `apriori()` return value structure
- [ ] Complete experimental results with all configurations
- [ ] Generate performance comparison graphs
- [ ] Fill report with empirical findings
- [ ] Add discussion and conclusions

## 💡 Key Insights

1. **Vertical Format Advantages:**
   - Better for sparse datasets
   - Eliminates repeated full database scans
   - Set intersection is faster than item checking

2. **Vertical Format Trade-offs:**
   - Higher memory usage (stores all TID-lists)
   - Slower on dense datasets with many items
   - Support threshold matters (lower = more intersections)

3. **When to Use Each:**
   - **Classical Apriori:** High support (>30%), small datasets, memory-constrained
   - **Vertical Format:** Low support (<20%), large sparse datasets, abundant RAM

## 🛠️ For Partners: How to Continue

1. **Read [HANDOVER.md](HANDOVER.md) first** - Contains all implementation details
2. **Fix the bugs listed** in "Remaining Tasks" section
3. **Obtain real datasets** from SPMF or Kaggle
4. **Run complete benchmarks** with multiple support levels
5. **Create visualization graphs** using matplotlib
6. **Complete the written report** in `report/main.md`

## 📚 References

- Agrawal & Srikant (1994) - Original Apriori
- Zaki (2000) - Eclat and Vertical Format
- Han et al. (2000) - FP-Growth
- [Your 2022+ Algorithm Here]

## 🤝 Contributing

When extending this project:
1. Follow PEP 8 style guidelines
2. Add docstrings to new functions
3. Update this README
4. Test thoroughly before merging
5. Document changes in HANDOVER.md

## ⚠️ Known Issues

1. **Synthetic data is too dense** - Vertical format doesn't show advantage
   - **Fix:** Download real FIMI datasets from SPMF repository
   
2. **Apriori return structure mismatch** - evaluate.py expects different format
   - **Fix:** See HANDOVER.md section "Remaining Tasks"

3. **Low support causes combinatorial explosion**
   - **Workaround:** Start with support >= 10%

## 🔗 Useful Links

- **SPMF Dataset Repository:** https://www.philippe-fournier-viger.com/spmf/
- **FIMI Repository:** http://fimi.uantwerpen.be/ (note: URLs may be outdated)
- **IEEE Citation Format:** https://www.ieee.org/content/dam/ieee-org/ieee/web/org/conferences/style_guides_and_templates/ieee_conference_proceedings_template.docx

## 📝 License

Academic use for CS-378 course project

## 👥 Team

- **Original Developer:** Muhammad Ammar Riaz
- **Contributors:** Hashir Awaiz , Hamza Elahi , Taaha Shabbir
- **Course:** CS-378: Design and Analysis of Algorithms
- **Date:** May 2026

---

**📌 Important:** See [HANDOVER.md](HANDOVER.md) for complete project documentation, setup instructions, and next steps.
