# 6. Visualization (`src/visualize.py`)

## 6.1 Role

`visualize.py` turns **`results/benchmark_results.json`** into **per-dataset PNG charts** under **`results/plots/`**. It is the bridge from raw numbers to figures suitable for slides or the IEEE-style report.

## 6.2 Input contract

The script expects the JSON produced by **`evaluate.py`** (or extended by **`run_remaining.py`**): a **list** of records, each with:

- `dataset`: string label (e.g., `"Chess (Real FIMI Benchmark)"`).
- `support`: float ratio used for that row.
- `results`: object with keys `apriori`, `optimized`, `huim`, each either **metric dict** or **`null`** on failure / skip.

Each metric dict includes at least `avg_time` and `avg_mem` (and others ignored by plotting).

## 6.3 Processing flow: `plot_results`

```6:67:src/visualize.py
def plot_results(results_file, output_dir):
    with open(results_file, 'r') as f:
        data = json.load(f)
        
    os.makedirs(output_dir, exist_ok=True)
    
    datasets = sorted(list(set(r['dataset'] for r in data)))
    
    for dataset in datasets:
        dataset_results = [r for r in data if r['dataset'] == dataset]
        dataset_results.sort(key=lambda x: x['support'], reverse=True)
        
        supports = [r['support'] for r in dataset_results]
        labels = [f"{int(s*100)}%" for s in supports]
        
        # 1. Execution Time Plot
        plt.figure(figsize=(10, 6))
        
        ap_times = [r['results']['apriori']['avg_time'] if r['results']['apriori'] else 0 for r in dataset_results]
        opt_times = [r['results']['optimized']['avg_time'] if r['results']['optimized'] else 0 for r in ...]
        huim_times = [r['results']['huim']['avg_time'] if r['results']['huim'] else 0 for r in ...]
        ...
        plt.yscale('log')
        plt.savefig(os.path.join(output_dir, f"{dataset.split(' ')[0].lower()}_time.png"))
```

**Grouping:** Unique `dataset` strings define chart families—keep naming **consistent** across benchmark runs or you will split one logical dataset into two chart groups.

**Sort order:** `reverse=True` on support means **x-axis labels** run from **stricter to looser** minimum support (left to right: e.g., 97% → 95% → 93% for Connect). That matches intuition: lower support thresholds tend to **increase** work toward the right.

**Null handling:** Missing algorithm entries become **0** in the arrays. On a **log y-axis**, zeros are problematic (log(0) undefined). Matplotlib typically masks or drops zeros with a warning depending on version; if plots look empty for a series, check whether HUIM was skipped (`null`) vs actually ~0 seconds.

**Filenames:** `dataset.split(' ')[0].lower()` takes the first token (“chess”, “connect”, …) for compact filenames. Works for current labels; fragile if you rename datasets to start with punctuation.

## 6.4 Memory chart

Second figure per dataset repeats the same grouping but plots **`avg_mem`** on a **linear** scale with grid lines. This shows **RSS delta** patterns rather than absolute footprint.

## 6.5 CLI entry

```69:79:src/visualize.py
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_file = os.path.join(base_dir, "results", "benchmark_results.json")
    output_dir = os.path.join(base_dir, "results", "plots")
```

Run from anywhere via `python src/visualize.py`; paths resolve to repo root.

## 6.6 Possible extensions (not implemented)

- Error bars using `std_time` from JSON.
- Candidate count or itemset count as secondary y-axis.
- Combined multi-dataset grid figure for appendix pages.

