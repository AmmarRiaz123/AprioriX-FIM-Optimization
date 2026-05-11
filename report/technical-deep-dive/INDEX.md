# Technical Deep-Dive: AprioriX-FIM-Optimization

This folder contains **section-by-section** documentation of the repository: goals, algorithms, benchmarking, data pipeline, and design tradeoffs. It is meant to complement [README.md](../../README.md), [HANDOVER.md](../../HANDOVER.md), and the course report under [report/main.md](../main.md).

## How to read these documents

1. Start with **Project vision and repository map** for context and file roles.
2. Read **Algorithms** in order: classical Apriori → vertical/bitset → HUIM (each builds on the previous idea).
3. Read **Evaluation and visualization** to see how experiments are run and plotted.
4. Finish with **Data pipeline** and **Limitations** for reproducibility and honest caveats.

## Document map

| Section | File | What it covers |
|--------|------|----------------|
| 1 | [01-project-vision-and-repo-map.md](01-project-vision-and-repo-map.md) | Course goals, three-way comparison, directory layout, dependencies |
| 2 | [02-classical-apriori.md](02-classical-apriori.md) | `src/apriori.py`: horizontal format, candidate generation, complexity |
| 3 | [03-optimized-vertical-apriori.md](03-optimized-vertical-apriori.md) | `src/optimized_apriori.py`: TID bitsets, joins, why it is faster |
| 4 | [04-huim-algorithm.md](04-huim-algorithm.md) | `src/huim_algorithm.py`: utility vs support, binary fast path, relation to SOTA |
| 5 | [05-evaluation-and-benchmarking.md](05-evaluation-and-benchmarking.md) | `src/evaluate.py`, `run_remaining.py`, `benchmark.py`, metrics, HUIM scheduling |
| 6 | [06-visualization.md](06-visualization.md) | `src/visualize.py`, JSON schema, plots |
| 7 | [07-data-pipeline-and-datasets.md](07-data-pipeline-and-datasets.md) | FIMI `.dat`, Online Retail conversion, synthetic generation, downloads |
| 8 | [08-testing-and-auxiliary.md](08-testing-and-auxiliary.md) | `simple_test.py`, `test_env.py`, batch runner |
| 9 | [09-design-tradeoffs-and-limitations.md](09-design-tradeoffs-and-limitations.md) | Bitset scale, Apriori vs true HUIM pruning, fair comparison notes |

## Quick reference: entry points

| Task | Command / script |
|------|------------------|
| Full benchmark suite (3-run average) | `python src/evaluate.py` |
| Plots from saved JSON | `python src/visualize.py` |
| Resume / extend benchmarks | `python src/run_remaining.py` (expects existing `results/benchmark_results.json`) |
| Online Retail → `.dat` | `python convert_dataset.py` (expects `datasets/Assignment-1_Data.csv`) |
| Environment smoke test | `python src/test_env.py` (run from `src/`) |

---

