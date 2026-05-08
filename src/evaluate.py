import time
import os
import psutil
from apriori import load_transactions, apriori
from optimized_apriori import vertical_apriori

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) # MB

def benchmark_algorithms(dataset_path, min_sup_ratio):
    print(f"Benchmarking dataset: {dataset_path} with min_sup={min_sup_ratio}")
    transactions = load_transactions(dataset_path)
    num_transactions = len(transactions)
    min_sup_count = int(min_sup_ratio * num_transactions)
    
    # Measure Baseline Apriori
    print("-- Running Baseline Apriori --")
    start_v = get_memory_usage()
    start_t = time.time()
    fi_apriori, candidates = apriori(transactions, min_sup_count)
    end_t = time.time()
    end_v = get_memory_usage()
    
    apriori_time = end_t - start_t
    apriori_mem = end_v - start_v
    print(f"Time: {apriori_time:.4f}s | Memory: {apriori_mem:.2f} MB | Candidates: {candidates}")
    
    # Measure Optimized Apriori
    print("-- Running Optimized Apriori (Vertical Format) --")
    start_v = get_memory_usage()
    start_t = time.time()
    fi_opt = vertical_apriori(dataset_path, min_sup_count)
    end_t = time.time()
    end_v = get_memory_usage()
    
    opt_time = end_t - start_t
    opt_mem = end_v - start_v
    print(f"Time: {opt_time:.4f}s | Memory: {opt_mem:.2f} MB")
    
    speedup = apriori_time / opt_time if opt_time > 0 else float('inf')
    print(f"Speedup achieved: {speedup:.2f}x\n")

if __name__ == "__main__":
    # Ensure psutil is installed (pip install psutil)
    # Download datasets "chess.dat", "connect.dat", "accidents.dat" from FIMI repo and place them in ../datasets/
    # Sample run (uncomment when dataset is available):
    # benchmark_algorithms("../datasets/chess.dat", min_sup_ratio=0.8)
    pass
