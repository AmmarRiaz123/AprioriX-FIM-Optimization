import time
import os
import psutil
import json
import statistics
from apriori import load_transactions, apriori
from optimized_apriori import vertical_apriori
from huim_algorithm import huim_mining_optimized

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

def benchmark_algorithms(dataset_path, min_sup_ratio, num_runs=3, run_huim=True):
    print(f"\n{'='*70}")
    print(f"Benchmarking dataset: {os.path.basename(dataset_path)} with min_sup={min_sup_ratio:.2f} (Avg of {num_runs} runs)")
    print(f"{'='*70}")
    
    # Load transactions once for Apriori
    transactions = load_transactions(dataset_path)
    num_transactions = len(transactions)
    min_sup_count = int(min_sup_ratio * num_transactions)
    
    # For HUIM, convert support count to utility threshold (approximate)
    min_utility_threshold = min_sup_count * 1.0  # Default item utility = 1.0
    
    results_summary = {}

    # Measure Baseline Apriori
    print(f"-- Running Baseline Apriori ({num_runs} runs) --")
    try:
        stats = run_benchmark_averaged(apriori, (transactions, min_sup_count), num_runs)
        results_summary['apriori'] = stats
        print(f"Time: {stats['avg_time']:.4f}s (±{stats['std_time']:.4f}s) | Memory: {stats['avg_mem']:.2f} MB | Candidates: {stats['candidates']}")
    except Exception as e:
        print(f"Error in Apriori: {e}")
        results_summary['apriori'] = None
    
    # Measure Optimized Apriori
    print(f"-- Running Optimized Apriori (Vertical Format) ({num_runs} runs) --")
    try:
        stats = run_benchmark_averaged(vertical_apriori, (dataset_path, min_sup_count), num_runs)
        results_summary['optimized'] = stats
        print(f"Time: {stats['avg_time']:.4f}s (±{stats['std_time']:.4f}s) | Memory: {stats['avg_mem']:.2f} MB | Candidates: {stats['candidates']}")
    except Exception as e:
        print(f"Error in Optimized Apriori: {e}")
        results_summary['optimized'] = None
    
    # Measure HUIM (2022+ State-of-the-Art Algorithm)
    if run_huim:
        print(f"-- Running HUIM (2022+ SOTA) ({num_runs} runs) --")
        try:
            stats = run_benchmark_averaged(huim_mining_optimized, (dataset_path, min_utility_threshold), num_runs)
            results_summary['huim'] = stats
            print(f"Time: {stats['avg_time']:.4f}s (±{stats['std_time']:.4f}s) | Memory: {stats['avg_mem']:.2f} MB | Candidates: {stats['candidates']}")
        except Exception as e:
            print(f"Error in HUIM: {e}")
            results_summary['huim'] = None
    else:
        results_summary['huim'] = None
        
    # Calculate speedups
    print(f"\n{'='*70}")
    print("SPEEDUP ANALYSIS")
    print(f"{'='*70}")
    
    ap_time = results_summary['apriori']['avg_time'] if results_summary['apriori'] and results_summary['apriori']['avg_time'] > 0 else 0
    
    if results_summary['optimized'] and results_summary['optimized']['avg_time'] > 0:
        speedup_opt = ap_time / results_summary['optimized']['avg_time'] if ap_time > 0 else 0
        print(f"Optimized Apriori speedup: {speedup_opt:.2f}x")
    
    if results_summary['huim'] and results_summary['huim']['avg_time'] > 0:
        speedup_huim = ap_time / results_summary['huim']['avg_time'] if ap_time > 0 else 0
        print(f"HUIM (2022+) speedup: {speedup_huim:.2f}x")
    
    return results_summary

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FINAL PROJECT EVALUATION: REAL-WORLD DATASET BENCHMARKING")
    print("="*70)
    print("Averaging results over 3 runs for scientific accuracy.")
    print("="*70)
    
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    datasets_dir = os.path.join(base_dir, "datasets")
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, "benchmark_results.json")
    
    # Benchmark datasets with custom support ratios to ensure completion
    # Dense datasets need higher support, sparse ones need lower.
    test_suite = [
        {
            "path": os.path.join(datasets_dir, "chess.dat"),
            "name": "Chess (Real FIMI Benchmark)",
            "ratios": [0.9, 0.85, 0.8]
        },
        {
            "path": os.path.join(datasets_dir, "connect.dat"),
            "name": "Connect (Real FIMI Benchmark)",
            "ratios": [0.97, 0.95, 0.93]
        },
        {
            "path": os.path.join(datasets_dir, "accidents.dat"),
            "name": "Accidents (Real FIMI Benchmark)",
            "ratios": [0.9, 0.85, 0.8]
        },
        {
            "path": os.path.join(datasets_dir, "online_retail_itemids.dat"),
            "name": "Online Retail (Real-World)",
            "ratios": [0.1, 0.05, 0.02]
        }
    ]
    
    all_results = []
    
    for dataset in test_suite:
        dataset_path = dataset["path"]
        dataset_name = dataset["name"]
        
        print(f"\n\n{'='*70}")
        print(f"DATASET: {dataset_name}")
        print(f"{'='*70}")
        
        if not os.path.exists(dataset_path):
            print(f"Skipping {dataset_name} - File not found: {dataset_path}")
            continue
        
        for j, ratio in enumerate(dataset["ratios"]):
            # Run all algorithms for 3 runs (Scientific accuracy as required)
            # Only run HUIM at highest support threshold per dataset (j==0)
            # to avoid exponential runtime at lower thresholds
            run_huim_flag = (j == 0)
            res = benchmark_algorithms(dataset_path, min_sup_ratio=ratio, num_runs=3, run_huim=run_huim_flag)
            all_results.append({
                'dataset': dataset_name,
                'support': ratio,
                'results': res
            })
            
            # Incremental save
            with open(results_file, 'w') as f:
                json.dump(all_results, f, indent=4)
        
    print(f"\n{'='*70}")
    print(f"BENCHMARK COMPLETE. Results saved to: {results_file}")
    print("="*70)
