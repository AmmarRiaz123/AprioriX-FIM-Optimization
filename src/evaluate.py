import time
import os
import psutil
from apriori import load_transactions, apriori
from optimized_apriori import vertical_apriori

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) # MB

def benchmark_algorithms(dataset_path, min_sup_ratio):
    print(f"Benchmarking dataset: {dataset_path} with min_sup={min_sup_ratio:.2f}")
    transactions = load_transactions(dataset_path)
    num_transactions = len(transactions)
    min_sup_count = int(min_sup_ratio * num_transactions)
    
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
        
    speedup = apriori_time / opt_time if opt_time > 0 and opt_time != float('inf') else float('inf')
    if speedup != float('inf'):
        print(f"Speedup achieved: {speedup:.2f}x\n")
    else:
        print("Speedup achieved: N/A\n")

if __name__ == "__main__":
    for ratio in [0.4, 0.2, 0.1]:
        benchmark_algorithms("../datasets/chess.dat", min_sup_ratio=ratio)
