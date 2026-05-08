import time
import psutil
import os
from apriori import apriori
from optimized_apriori import optimized_apriori

def load_dataset(file_path):
    transactions = []
    with open(file_path, 'r') as f:
        for line in f:
            transactions.append(line.strip().split())
    return transactions

def run_benchmark(algorithm, transactions, min_sup):
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024 # MB
    
    start_time = time.time()
    itemsets = algorithm(transactions, min_sup)
    end_time = time.time()
    
    mem_after = process.memory_info().rss / 1024 / 1024
    
    return {
        'time_ms': (end_time - start_time) * 1000,
        'memory_mb': mem_after - mem_before,
        'itemsets_found': len(itemsets)
    }

if __name__ == "__main__":
    print("Please place the dataset files (connect.dat, chess.dat, accident.dat) in the '../datasets/' folder.")
    # Example usage:
    # transactions = load_dataset('../datasets/chess.dat')
    # Use standard support threshold, e.g., 50% = 0.5 * len(transactions)
    # results = run_benchmark(optimized_apriori, transactions, min_sup=1500)
