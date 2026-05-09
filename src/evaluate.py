import time
import os
import psutil
from apriori import load_transactions, apriori
from optimized_apriori import vertical_apriori
from huim_algorithm import huim_mining_optimized

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) # MB

def benchmark_algorithms(dataset_path, min_sup_ratio):
    print(f"\n{'='*70}")
    print(f"Benchmarking dataset: {dataset_path} with min_sup={min_sup_ratio:.2f}")
    print(f"{'='*70}")
    
    transactions = load_transactions(dataset_path)
    num_transactions = len(transactions)
    min_sup_count = int(min_sup_ratio * num_transactions)
    
    # For HUIM, convert support count to utility threshold (approximate)
    min_utility_threshold = min_sup_count * 1.0  # Default item utility = 1.0
    
    # Measure Baseline Apriori
    print("-- Running Baseline Apriori --")
    start_v = get_memory_usage()
    start_t = time.time()
    try:
        fi_apriori, candidates = apriori(transactions, min_sup_count)
        apriori_time = time.time() - start_t
        apriori_mem = get_memory_usage() - start_v
        print(f"Time: {apriori_time:.4f}s | Memory: {apriori_mem:.2f} MB | Candidate Count: {len(candidates) if candidates else 0}")
    except Exception as e:
        apriori_time = float('inf')
        print(f"Error: {e}")
    
    # Measure Optimized Apriori
    print("-- Running Optimized Apriori (Vertical Format) --")
    start_v = get_memory_usage()
    start_t = time.time()
    try:
        fi_opt = vertical_apriori(dataset_path, min_sup_count)
        opt_time = time.time() - start_t
        opt_mem = get_memory_usage() - start_v
        print(f"Time: {opt_time:.4f}s | Memory: {opt_mem:.2f} MB")
    except Exception as e:
        opt_time = float('inf')
        print(f"Error: {e}")
    
    # Measure HUIM (2022+ State-of-the-Art Algorithm)
    print("-- Running HUIM (2022+ State-of-the-Art: High-Utility Itemset Mining) --")
    start_v = get_memory_usage()
    start_t = time.time()
    try:
        fi_huim, huim_candidates = huim_mining_optimized(dataset_path, min_utility_threshold)
        huim_time = time.time() - start_t
        huim_mem = get_memory_usage() - start_v
        total_huim_itemsets = sum(len(itemsets) for itemsets in fi_huim.values())
        print(f"Time: {huim_time:.4f}s | Memory: {huim_mem:.2f} MB | Candidates: {huim_candidates} | Itemsets: {total_huim_itemsets}")
    except Exception as e:
        huim_time = float('inf')
        print(f"Error: {e}")
        
    # Calculate speedups
    print(f"\n{'='*70}")
    print("SPEEDUP ANALYSIS")
    print(f"{'='*70}")
    
    speedup_opt = apriori_time / opt_time if opt_time > 0 and opt_time != float('inf') else float('inf')
    speedup_huim = apriori_time / huim_time if huim_time > 0 and huim_time != float('inf') else float('inf')
    
    if speedup_opt != float('inf'):
        print(f"Optimized Apriori speedup vs Classical: {speedup_opt:.2f}x")
    else:
        print(f"Optimized Apriori speedup vs Classical: N/A")
    
    if speedup_huim != float('inf'):
        print(f"HUIM (2022+) speedup vs Classical: {speedup_huim:.2f}x")
    else:
        print(f"HUIM (2022+) speedup vs Classical: N/A")
    
    print()

if __name__ == "__main__":
    for ratio in [0.4, 0.2, 0.1]:
        benchmark_algorithms("../datasets/chess.dat", min_sup_ratio=ratio)
