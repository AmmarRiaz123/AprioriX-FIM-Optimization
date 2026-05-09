"""
High-Utility Itemset Mining (HUIM) Algorithm
Optimized with Vertical Data Format (TID-lists) for 2022+ Performance.
"""

def load_transactions_with_utility(filepath):
    transactions = []
    tid_lists = {}
    with open(filepath, 'r') as file:
        for tid, line in enumerate(file):
            transaction = {}
            items = line.strip().split()
            for item_spec in items:
                if ',' in item_spec:
                    item, utility = item_spec.split(',')
                    transaction[item] = float(utility)
                else:
                    item = item_spec
                    transaction[item] = 1.0
                
                if item not in tid_lists:
                    tid_lists[item] = set()
                tid_lists[item].add(tid)
                
            if transaction:
                transactions.append(transaction)
    return transactions, tid_lists

def huim_mining_optimized(filepath, min_utility_threshold):
    transactions, tid_lists = load_transactions_with_utility(filepath)
    
    # Step 1: Calculate item utilities
    item_utils = {}
    for tid, transaction in enumerate(transactions):
        for item, utility in transaction.items():
            item_utils[item] = item_utils.get(item, 0) + utility
            
    # Filter 1-itemsets
    f1_tids = {frozenset([item]): tid_lists[item] for item, util in item_utils.items() if util >= min_utility_threshold}
    f1_utils = {frozenset([item]): item_utils[item] for item, util in item_utils.items() if util >= min_utility_threshold}
    
    high_utility_itemsets = {1: set(f1_tids.keys())}
    current_itemsets_tids = f1_tids
    k = 2
    candidates_generated = 0
    
    while current_itemsets_tids:
        next_itemsets_tids = {}
        itemset_list = list(current_itemsets_tids.keys())
        
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                itemset1 = itemset_list[i]
                itemset2 = itemset_list[j]
                
                l1 = sorted(list(itemset1))[:-1]
                l2 = sorted(list(itemset2))[:-1]
                
                if l1 == l2:
                    candidate = itemset1.union(itemset2)
                    candidates_generated += 1
                    
                    # Optimization: Intersect TID lists first
                    candidate_tids = current_itemsets_tids[itemset1].intersection(current_itemsets_tids[itemset2])
                    
                    if not candidate_tids:
                        continue
                        
                    # Calculate utility only for transactions in candidate_tids
                    candidate_utility = 0.0
                    for tid in candidate_tids:
                        transaction = transactions[tid]
                        # In HUIM, utility of itemset in transaction is usually sum of utilities
                        # of its items in that transaction (standard model)
                        util = sum(transaction[item] for item in candidate)
                        candidate_utility += util
                    
                    if candidate_utility >= min_utility_threshold:
                        next_itemsets_tids[candidate] = candidate_tids
                        
        if next_itemsets_tids:
            high_utility_itemsets[k] = set(next_itemsets_tids.keys())
            current_itemsets_tids = next_itemsets_tids
        else:
            break
        k += 1
        
    return high_utility_itemsets, candidates_generated
