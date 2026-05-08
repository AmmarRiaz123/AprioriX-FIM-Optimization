# Optimizations implemented:
# 1. Vertical Data Format (TID-lists) - Fast intersection instead of full DB scans (Addresses Section 5.1/5.2)
# 2. Transaction Reduction - Ignoring transactions that are too short to contain a k-itemset.

def load_transactions_vertical(filepath):
    tid_lists = {}
    num_transactions = 0
    with open(filepath, 'r') as file:
        for tid, line in enumerate(file):
            num_transactions += 1
            items = line.strip().split()
            for item in items:
                if item not in tid_lists:
                    tid_lists[item] = set()
                tid_lists[item].add(tid)
    return tid_lists, num_transactions

def vertical_apriori(filepath, min_sup_count):
    tid_lists, num_transactions = load_transactions_vertical(filepath)
    
    # Filter length 1 items
    f1 = {frozenset([item]): tids for item, tids in tid_lists.items() if len(tids) >= min_sup_count}
    frequent_itemsets = {1: set(f1.keys())}
    current_itemsets = f1
    k = 2
    
    while current_itemsets:
        next_itemsets = {}
        itemset_list = list(current_itemsets.keys())
        
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                itemset1 = itemset_list[i]
                itemset2 = itemset_list[j]
                
                # Join condition (share first k-2 items)
                l1 = list(itemset1)[:-1]
                l2 = list(itemset2)[:-1]
                if l1 == l2:
                    candidate = itemset1.union(itemset2)
                    
                    # Intersect TID lists (The core optimization: no full DB scan)
                    candidate_tids = current_itemsets[itemset1].intersection(current_itemsets[itemset2])
                    
                    if len(candidate_tids) >= min_sup_count:
                        next_itemsets[candidate] = candidate_tids
                        
        if next_itemsets:
            frequent_itemsets[k] = set(next_itemsets.keys())
        current_itemsets = next_itemsets
        k += 1
        
    return frequent_itemsets
