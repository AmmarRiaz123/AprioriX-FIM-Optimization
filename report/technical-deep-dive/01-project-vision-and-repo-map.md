# 1. Project vision and repository map

## 1.1 What this project is for

**AprioriX-FIM-Optimization** is a course project (CS-378: Design and Analysis of Algorithms) that studies **Frequent Itemset Mining (FIM)** from three angles:

1. **Baseline**: Classical **Apriori** on a **horizontal** transaction database (scan every transaction for every candidate).
2. **Optimized FIM**: A **vertical** representation (transaction IDs per item) combined with **bitwise AND** to emulate TID-list intersection with word-level parallelism—conceptually close to **Eclat**-style mining.
3. **“2022+” angle**: **High-Utility Itemset Mining (HUIM)**—patterns ranked by **utility** (e.g., revenue) rather than raw frequency alone, implemented in the same vertical/bitset spirit for a **direct engineering comparison** with the optimized frequent miner.

The **scientific goal** is not only to implement working code but to **measure** wall-clock time, memory delta, candidate counts, and output sizes across **real FIMI-style benchmarks** (Chess, Connect, Accidents) and a **real-world** e-commerce basket dataset (Online Retail), with **multi-run averaging** to reduce noise.

## 1.2 Core narrative (how the pieces fit)

- **Frequency** asks: “Which itemsets appear in at least *min_sup × |D|* transactions?”
- **Utility** asks: “Which itemsets contribute at least *U* total utility when summed over transactions where they appear?”

On **binary** data (every item utility = 1), a simplified HUIM threshold can align with support-like semantics, but the **algorithms still differ** in how they aggregate evidence (support count vs summed utility). The project uses that alignment **only for benchmarking convenience** when comparing runtimes on the same file; see [09-design-tradeoffs-and-limitations.md](09-design-tradeoffs-and-limitations.md) for caveats.

## 1.3 Repository layout (what lives where)

| Path | Role |
|------|------|
| `src/apriori.py` | Classical Apriori: load transactions as sets, generate candidates, count by subset tests. |
| `src/optimized_apriori.py` | Vertical Apriori: build per-item bitsets, join itemsets, AND bitsets, popcount for support. |
| `src/huim_algorithm.py` | HUIM variant: optional `item,utility` tokens; bitset intersection; utility sum over matching TIDs. |
| `src/evaluate.py` | Main experiment driver: 3-run averages, JSON output to `results/benchmark_results.json`. |
| `src/visualize.py` | Reads JSON, emits per-dataset time/memory bar charts under `results/plots/`. |
| `src/benchmark.py` | Early / alternate harness (see section doc for API mismatch with `vertical_apriori`). |
| `src/run_remaining.py` | Continuation script to append benchmarks to an existing results JSON. |
| `src/simple_test.py`, `src/test_env.py` | Quick sanity checks. |
| `datasets/` | `.dat` transaction files; `item_mapping.txt` for retail IDs; optional source CSV/XLSX. |
| `convert_dataset.py` | Retail CSV → `online_retail_itemids.dat` + `online_retail_utility.dat`. |
| `analyze_datasets.py` | Exploratory printout of retail CSV stats and suitability notes. |
| `download_dataset.py` | KaggleHub download helper (optional; dependency not in `requirements.txt`). |
| `scripts/generate_datasets.py` | Synthetic `.dat` generator (use with care vs real FIMI names). |
| `report/` | IEEE-style writeups (`main.md`, etc.) and this **technical-deep-dive** folder. |
| `run_experiments.bat` | Windows batch file pointing at `src/benchmark.py`. |

## 1.4 Dependencies (`requirements.txt`)

- **psutil**: Resident set size (RSS) snapshots for a rough **memory delta** per run.
- **matplotlib**, **numpy**: Plotting in `visualize.py`.
- **pandas**: Used by `convert_dataset.py` and `analyze_datasets.py`.

Optional dev tools (pytest, pylint, black) and Jupyter are listed for analysis workflows.

## 1.5 Intellectual lineage (names the team invokes)

- **Apriori** (Agrawal & Srikant): candidate generation + downward closure (anti-monotonicity of support).
- **Vertical / Eclat-style** ideas: store **tidsets** or **diffsets** to replace repeated full scans.
- **HUIM** literature: utility upper bounds, transaction-weighted utilities, two-phase methods, HUI-Miner / FHM families—the **codebase implementation** is a **pedagogical** vertical join + utility accumulation, not a full reproduction of a named 2022 paper’s pruning tree.

That distinction matters for grading and for research honesty: the project compares **engineering patterns** (horizontal vs vertical+bitops) and introduces a **utility metric**, while the written HUIM doc ([HUIM_ALGORITHM_DOCUMENTATION.md](../../HUIM_ALGORITHM_DOCUMENTATION.md)) provides broader **survey-level** context.

## 1.6 Success criteria (what “done” meant for the team)

- Three implementations runnable on shared `.dat` inputs.
- A **repeatable** benchmark harness with **averaged** timings and saved **JSON** for the report and plots.
- Plots that communicate **scale differences** (log time axis) across support thresholds.
- Written analysis tying **observed speedups** to **algorithmic** causes (fewer scans, bitwise parallelism) and acknowledging **HUIM** cost on binary data.

The following sections open the hood on each code area in detail.
