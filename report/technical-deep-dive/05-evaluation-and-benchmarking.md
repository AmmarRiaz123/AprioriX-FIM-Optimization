# 5. Evaluation and benchmarking

This section covers **`src/evaluate.py`** (primary harness), **`src/run_remaining.py`** (incremental completion), and **`src/benchmark.py`** (legacy / alternate).

## 5.1 `evaluate.py`: design goals

The evaluation script is the **scientific core** of the repo:

1. **Fair inputs:** Same dataset path and support **ratio** for Apriori and vertical Apriori; derived **absolute** `min_sup_count` from `|D|`.
2. **Low-variance reporting:** Default **`num_runs=3`** with mean and sample standard deviation for wall time.
3. **Resource observability:** RSS-based **memory delta** around each run (best-effort in Python; not a hardware perf counter substitute).
4. **Search-space telemetry:** `candidates` from each algorithm’s counter.
5. **Output size telemetry:** `itemsets_count` sums bucket sizes for dict-shaped results.
6. **Persistence:** Incremental writes to **`results/benchmark_results.json`** after each configuration finishes.

## 5.2 Memory and timing helpers

```10:43:src/evaluate.py
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) # MB

def run_benchmark_averaged(func, args, num_runs=3):
    times = []
    memories = []
    result = None
    candidates = 0
    
    for i in range(num_runs):
        print(f"  - Run {i+1}/{num_runs}...", end="", flush=True)
        start_v = get_memory_usage()
        start_t = time.time()
        
        # Unpack args and call function
        res, cand = func(*args)
        
        elapsed = time.time() - start_t
        times.append(elapsed)
        memories.append(max(0, get_memory_usage() - start_v))
        print(f" {elapsed:.4f}s")
        
        if i == 0:
            result = res
            candidates = cand
            
    return {
        'avg_time': statistics.mean(times),
        'std_time': statistics.stdev(times) if len(times) > 1 else 0,
        'avg_mem': statistics.mean(memories),
        'candidates': candidates,
        'itemsets_count': sum(len(v) for v in result.values()) if isinstance(result, dict) else 0
    }
```

**Thinking behind `start_v` / delta:**

- RSS fluctuates due to allocator behavior; taking **after − before** per run isolates a rough “growth during this call” signal.
- `max(0, ...)` avoids negative deltas when the GC frees objects between samples.

**Thinking behind using run 1’s `candidates`:**

- Candidate generation is deterministic for fixed input; repeating it three times for the counter would be redundant. **Time** still averages three runs.

**Caveat:** Only the **first run’s** `result` is retained for `itemsets_count`. If an algorithm were nondeterministic (not the case here), you would want explicit equality checks across runs.

## 5.3 `benchmark_algorithms`: orchestration

```45:108:src/evaluate.py
def benchmark_algorithms(dataset_path, min_sup_ratio, num_runs=3, run_huim=True):
    ...
    transactions = load_transactions(dataset_path)
    num_transactions = len(transactions)
    min_sup_count = int(min_sup_ratio * num_transactions)
    
    # For HUIM, convert support count to utility threshold (approximate)
    min_utility_threshold = min_sup_count * 1.0  # Default item utility = 1.0
    
    results_summary = {}
    ...
    stats = run_benchmark_averaged(apriori, (transactions, min_sup_count), num_runs)
    ...
    stats = run_benchmark_averaged(vertical_apriori, (dataset_path, min_sup_count), num_runs)
    ...
    if run_huim:
        stats = run_benchmark_averaged(huim_mining_optimized, (dataset_path, min_utility_threshold), num_runs)
```

**Three-way call pattern:**

| Algorithm | Arguments | Why |
|-----------|-----------|-----|
| `apriori` | `(transactions, min_sup_count)` | Needs horizontal structure already loaded. |
| `vertical_apriori` | `(dataset_path, min_sup_count)` | Reads file to build bitsets independently. |
| `huim_mining_optimized` | `(dataset_path, min_utility_threshold)` | Parses utilities; threshold aligned to support count on unit utilities. |

**HUIM gating (`run_huim`):** Long runtimes at low support motivate **`run_huim=False`** for some configurations (see main block).

## 5.4 Main benchmark suite (`__main__`)

Key behaviors:

- Resolves **`base_dir`** as repo root (parent of `src`).
- Ensures **`results/`** exists.
- **`test_suite`** lists datasets and **per-dataset support ratios** tuned to typical density:
  - Dense FIMI (Chess, Connect, Accidents): **high** ratios (e.g., 0.9–0.97).
  - Sparse retail: **low** ratios (0.02–0.1).
- **HUIM scheduling:** `run_huim_flag = (j == 0)` runs HUIM **only on the first (strictest) threshold** per dataset in the loop, to avoid exponential blowups at looser thresholds while still showing a **2022+** data point.

**Dataset paths:** Expects files such as `chess.dat`, `connect.dat`, `accidents.dat`, `online_retail_itemids.dat` under `datasets/`. If a file is missing, that dataset block is skipped with a message.

**JSON shape** (each element of the top-level list):

```json
{
  "dataset": "Chess (Real FIMI Benchmark)",
  "support": 0.9,
  "results": {
    "apriori": { "avg_time", "std_time", "avg_mem", "candidates", "itemsets_count" } | null,
    "optimized": { ... } | null,
    "huim": { ... } | null
  }
}
```

## 5.5 `run_remaining.py`

Purpose: **resume** experiments by loading existing `benchmark_results.json`, running a hand-built list of remaining `(dataset, ratio, huim?)` tasks, and **appending** after each task with incremental save.

This is useful when:

- A long HUIM run was skipped mid-suite.
- Connect/Accidents/Retail files were added later.
- Chess needed an extra ratio without HUIM.

**Operational note:** It assumes `results/benchmark_results.json` already exists; otherwise it errors on load.

## 5.6 `benchmark.py` (legacy)

```14:28:src/benchmark.py
def run_benchmark(algorithm, transactions, min_sup):
    ...
    itemsets = algorithm(transactions, min_sup)
```

The example path suggests calling **`vertical_apriori`** like **`apriori`** with `(transactions, min_sup)`, but **`vertical_apriori` expects `(filepath, min_sup_count)`** and returns `(dict, candidates)` not a bare list. **`run_experiments.bat`** runs `python benchmark.py` from `src/`—as-is, it only prints a reminder comment unless the user uncomments and fixes the call shape.

**Recommendation for maintainers:** Either update `benchmark.py` to wrap `vertical_apriori(dataset_path, min_sup_count)` or point the batch file at `evaluate.py`.

## 5.7 Experimental interpretation tips

- **Speedup lines** in console output compare HUIM or optimized times to Apriori when both exist.
- **Log-scale plots** (`visualize.py`) help when Apriori and HUIM differ by orders of magnitude across thresholds.
- When HUIM is **skipped** for some rows, plots still render with **zero** placeholders—read labels carefully.
