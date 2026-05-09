def load_transactions(filepath):
    transactions = []
    with open(filepath, 'r') as file:
        for line in file:
            transactions.append(set(line.strip().split()))
    return transactions

def get_frequent_1_itemsets(transactions, min_sup_count):
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1
            
    f1 = []
    for item, count in item_counts.items():
        if count >= min_sup_count:
            f1.append(frozenset([item]))
    return f1

def apriori_gen(fk_minus_1, k):
    candidates = set()
    fk_list = sorted([sorted(list(itemset)) for itemset in fk_minus_1])
    
    # Group by prefix (first k-2 items)
    for i in range(len(fk_list)):
        for j in range(i + 1, len(fk_list)):
            l1 = fk_list[i][:k-2]
            l2 = fk_list[j][:k-2]
            
            if l1 == l2:
                # Potential candidate
                c1 = frozenset(fk_list[i])
                c2 = frozenset(fk_list[j])
                candidate = c1.union(c2)
                
                # Pruning step (Apriori property)
                is_valid = True
                for item in candidate:
                    subset = candidate - frozenset([item])
                    if subset not in fk_minus_1:
                        is_valid = False
                        break
                if is_valid:
                    candidates.add(candidate)
            else:
                # Since fk_list is sorted, if prefixes don't match, 
                # we can break the inner loop early if we want, 
                # but simple prefix check is already much faster than before.
                break 
    return candidates

def apriori(transactions, min_sup_count):
    frequent_itemsets = {}
    f1 = get_frequent_1_itemsets(transactions, min_sup_count)
    fk = set(f1)
    k = 2
    
    total_candidates_generated = 0
    
    while fk:
        frequent_itemsets[k-1] = fk
        candidates = apriori_gen(fk, k)
        total_candidates_generated += len(candidates)
        
        item_counts = {c: 0 for c in candidates}
        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    item_counts[candidate] += 1
                    
        fk = set(c for c, count in item_counts.items() if count >= min_sup_count)
        k += 1
        
    return frequent_itemsets, total_candidates_generated
