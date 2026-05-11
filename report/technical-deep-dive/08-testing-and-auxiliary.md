# 8. Testing and auxiliary scripts

## 8.1 `src/simple_test.py`

**Intent:** Minimal smoke benchmark of **baseline Apriori** on `../datasets/chess.dat` at **50%** support.

```13:21:src/simple_test.py
def benchmark_algorithms(dataset_path, min_sup_ratio):
    print(f"Benchmarking: {dataset_path}")
    transactions = load_transactions(dataset_path)
    min_sup_count = int(min_sup_ratio * len(transactions))
    
    print("-- Running Baseline Apriori --")
    start_t = time.time()
    fi_apriori, candidates_count = apriori(transactions, min_sup_count)
    print(f"Time: {time.time() - start_t:.4f}s")
```

**Observations:**

- Imports `optimized_apriori` and `huim_algorithm` / `psutil` but **does not call** them in the shown path—likely leftovers from expansion or copy-paste.
- Uses **relative path** `../datasets/chess.dat`, which works when executed from **`src/`**.

**Use case:** Quick “did I break Apriori?” after edits.

## 8.2 `src/test_env.py`

**Intent:** Environment sanity printout:

- Python version and cwd.
- Whether **`psutil`** imports.
- Whether **`from apriori import load_transactions`** succeeds.

Run from **`src/`** so `apriori` is on the module path without packaging.

## 8.3 Testing gaps (honest assessment)

- No **`pytest`** suite asserts correctness of frequent itemsets vs a reference miner.
- No **property tests** for anti-monotonicity or output equivalence between `apriori` and `vertical_apriori` on small synthetic files.
- No **automated** threshold sweep regression.

For a course project, **empirical** checks + manual inspection of small examples often suffice; for research-grade mining software, you would add golden-file tests and Brute-force validators for *n* ≤ 20 items.


