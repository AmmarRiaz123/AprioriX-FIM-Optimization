import json
import matplotlib.pyplot as plt
import os
import numpy as np

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
        opt_times = [r['results']['optimized']['avg_time'] if r['results']['optimized'] else 0 for r in dataset_results]
        huim_times = [r['results']['huim']['avg_time'] if r['results']['huim'] else 0 for r in dataset_results]
        
        x = np.arange(len(labels))
        width = 0.25
        
        plt.bar(x - width, ap_times, width, label='Classical Apriori', color='gray', alpha=0.8)
        plt.bar(x, opt_times, width, label='Optimized (Vertical)', color='blue', alpha=0.8)
        plt.bar(x + width, huim_times, width, label='HUIM (2022+)', color='green', alpha=0.8)
        
        plt.xlabel('Minimum Support (%)')
        plt.ylabel('Time (seconds)')
        plt.title(f'Execution Time Comparison - {dataset}')
        plt.xticks(x, labels)
        plt.legend()
        plt.yscale('log') # Use log scale for better comparison of different magnitudes
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{dataset.split(' ')[0].lower()}_time.png"))
        plt.close()
        
        # 2. Memory Usage Plot
        plt.figure(figsize=(10, 6))
        
        ap_mem = [r['results']['apriori']['avg_mem'] if r['results']['apriori'] else 0 for r in dataset_results]
        opt_mem = [r['results']['optimized']['avg_mem'] if r['results']['optimized'] else 0 for r in dataset_results]
        huim_mem = [r['results']['huim']['avg_mem'] if r['results']['huim'] else 0 for r in dataset_results]
        
        plt.bar(x - width, ap_mem, width, label='Classical Apriori', color='gray', alpha=0.8)
        plt.bar(x, opt_mem, width, label='Optimized (Vertical)', color='blue', alpha=0.8)
        plt.bar(x + width, huim_mem, width, label='HUIM (2022+)', color='green', alpha=0.8)
        
        plt.xlabel('Minimum Support (%)')
        plt.ylabel('Memory Delta (MB)')
        plt.title(f'Memory Usage Comparison - {dataset}')
        plt.xticks(x, labels)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{dataset.split(' ')[0].lower()}_memory.png"))
        plt.close()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_file = os.path.join(base_dir, "results", "benchmark_results.json")
    output_dir = os.path.join(base_dir, "results", "plots")
    
    if os.path.exists(results_file):
        print(f"Generating plots from {results_file}...")
        plot_results(results_file, output_dir)
        print(f"Plots saved to {output_dir}")
    else:
        print(f"Results file not found: {results_file}")
