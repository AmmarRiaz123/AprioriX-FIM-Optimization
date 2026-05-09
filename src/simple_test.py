
import time
import os
import psutil
from apriori import load_transactions, apriori
from optimized_apriori import vertical_apriori
from huim_algorithm import huim_mining_optimized

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def benchmark_algorithms(dataset_path, min_sup_ratio):
    print(f"Benchmarking: {dataset_path}")
    transactions = load_transactions(dataset_path)
    min_sup_count = int(min_sup_ratio * len(transactions))
    
    print("-- Running Baseline Apriori --")
    start_t = time.time()
    fi_apriori, candidates_count = apriori(transactions, min_sup_count)
    print(f"Time: {time.time() - start_t:.4f}s")

if __name__ == "__main__":
    dataset_path = "../datasets/chess.dat"
    if os.path.exists(dataset_path):
        benchmark_algorithms(dataset_path, 0.5)
    else:
        print(f"File not found: {dataset_path}")
