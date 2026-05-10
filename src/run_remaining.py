"""
Run remaining benchmarks that weren't completed.
Starts from the saved results and adds Chess 80% (Apriori+Optimized only),
Connect, Accidents, and Online Retail.
"""
import time
import os
import json
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluate import benchmark_algorithms

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
datasets_dir = os.path.join(base_dir, "datasets")
results_dir = os.path.join(base_dir, "results")
results_file = os.path.join(results_dir, "benchmark_results.json")

# Load existing results
with open(results_file, 'r') as f:
    all_results = json.load(f)

print(f"Loaded {len(all_results)} existing results. Continuing...")

# Remaining tasks
remaining = [
    # Chess 80% - skip HUIM (took too long)
    {"path": os.path.join(datasets_dir, "chess.dat"), "name": "Chess (Real FIMI Benchmark)", "ratio": 0.8, "huim": False},
    # Connect - 3 thresholds, HUIM only at highest
    {"path": os.path.join(datasets_dir, "connect.dat"), "name": "Connect (Real FIMI Benchmark)", "ratio": 0.97, "huim": True},
    {"path": os.path.join(datasets_dir, "connect.dat"), "name": "Connect (Real FIMI Benchmark)", "ratio": 0.95, "huim": False},
    {"path": os.path.join(datasets_dir, "connect.dat"), "name": "Connect (Real FIMI Benchmark)", "ratio": 0.93, "huim": False},
    # Accidents - 3 thresholds, HUIM only at highest
    {"path": os.path.join(datasets_dir, "accidents.dat"), "name": "Accidents (Real FIMI Benchmark)", "ratio": 0.9, "huim": True},
    {"path": os.path.join(datasets_dir, "accidents.dat"), "name": "Accidents (Real FIMI Benchmark)", "ratio": 0.85, "huim": False},
    {"path": os.path.join(datasets_dir, "accidents.dat"), "name": "Accidents (Real FIMI Benchmark)", "ratio": 0.8, "huim": False},
    # Online Retail - 3 thresholds, HUIM only at highest
    {"path": os.path.join(datasets_dir, "online_retail_itemids.dat"), "name": "Online Retail (Real-World)", "ratio": 0.1, "huim": True},
    {"path": os.path.join(datasets_dir, "online_retail_itemids.dat"), "name": "Online Retail (Real-World)", "ratio": 0.05, "huim": False},
    {"path": os.path.join(datasets_dir, "online_retail_itemids.dat"), "name": "Online Retail (Real-World)", "ratio": 0.02, "huim": False},
]

for task in remaining:
    if not os.path.exists(task["path"]):
        print(f"Skipping {task['name']} - File not found")
        continue
    
    print(f"\n{'='*70}")
    print(f"RUNNING: {task['name']} @ {task['ratio']} (HUIM={'YES' if task['huim'] else 'NO'})")
    print(f"{'='*70}")
    
    try:
        res = benchmark_algorithms(task["path"], min_sup_ratio=task["ratio"], num_runs=3, run_huim=task["huim"])
        all_results.append({
            'dataset': task['name'],
            'support': task['ratio'],
            'results': res
        })
        
        # Incremental save after each
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=4)
        print(f"Saved. Total results: {len(all_results)}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*70}")
print(f"ALL BENCHMARKS COMPLETE. Total: {len(all_results)} data points.")
print(f"Results saved to: {results_file}")
print("="*70)
