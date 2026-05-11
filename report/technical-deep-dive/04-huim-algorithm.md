# 4. HUIM-style mining (`src/huim_algorithm.py`)

## 4.1 Purpose in the project

The course brief asked for a **modern (2022+)** perspective beyond pure frequency. **High-Utility Itemset Mining (HUIM)** fits that slot: itemsets are ranked by **utility** contributed across transactions, enabling scenarios like **profit-weighted** market baskets.

This repository’s `huim_algorithm.py` implements a **vertical bitset join pipeline** analogous to `optimized_apriori.py`, but the **acceptance criterion** is **minimum utility** rather than minimum support count. The docstring frames it as optimized with **bitset parallelism** and a **fast path** when data is **binary** (all utilities 1).

## 4.2 Loading: `load_transactions_bitsets` (HUIM variant)

```7:30:src/huim_algorithm.py
def load_transactions_bitsets(filepath):
    transactions = []
    bitsets = {}
    num_transactions = 0
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
                
                if item not in bitsets:
                    bitsets[item] = 0
                bitsets[item] |= (1 << tid)
                
            if transaction:
                transactions.append(transaction)
                num_transactions += 1
    return transactions, bitsets, num_transactions
```

**Dual representation:**

1. **`transactions`**: list of `dict[item → utility]` for **per-transaction utility sums** when weights are not all 1.
2. **`bitsets`**: same per-item tid bitset as optimized Apriori, used to find **where** a candidate appears.

**Token grammar:**

- `item` → utility 1.0 (compatible with standard FIM `.dat`).
- `item,utility` → explicit float utility (as produced by `convert_dataset.py` for retail prices).

## 4.3 Mining: `huim_mining_optimized`

```32:101:src/huim_algorithm.py
def huim_mining_optimized(filepath, min_utility_threshold):
    transactions, bitsets, num_transactions = load_transactions_bitsets(filepath)
    
    # Step 1: Calculate item utilities
    item_utils = {}
    is_binary = True
    for tid, transaction in enumerate(transactions):
        for item, utility in transaction.items():
            item_utils[item] = item_utils.get(item, 0) + utility
            if utility != 1.0:
                is_binary = False
            
    # Filter 1-itemsets
    f1_bitsets = {frozenset([item]): bitsets[item] for item, util in item_utils.items() if util >= min_utility_threshold}
    
    high_utility_itemsets = {1: set(f1_bitsets.keys())}
    current_itemsets_bitsets = f1_bitsets
    k = 2
    candidates_generated = 0
    
    while current_itemsets_bitsets:
        next_itemsets_bitsets = {}
        itemset_list = list(current_itemsets_bitsets.keys())
        
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                itemset1 = itemset_list[i]
                itemset2 = itemset_list[j]
                
                l1 = sorted(list(itemset1))[:-1]
                l2 = sorted(list(itemset2))[:-1]
                
                if l1 == l2:
                    candidate = itemset1.union(itemset2)
                    candidates_generated += 1
                    
                    # Optimization: Bitwise AND intersection
                    candidate_bitset = current_itemsets_bitsets[itemset1] & current_itemsets_bitsets[itemset2]
                    
                    if candidate_bitset == 0:
                        continue
                        
                    # Fast Path for Binary Data (Standard FIM)
                    if is_binary:
                        # Count set bits (support)
                        support = bin(candidate_bitset).count('1')
                        candidate_utility = float(len(candidate) * support)
                    else:
                        # Full Utility Calculation for Weighted Data
                        candidate_utility = 0.0
                        temp_bitset = candidate_bitset
                        tid = 0
                        while temp_bitset > 0:
                            if temp_bitset & 1:
                                transaction = transactions[tid]
                                candidate_utility += sum(transaction[item] for item in candidate)
                            temp_bitset >>= 1
                            tid += 1
                    
                    if candidate_utility >= min_utility_threshold:
                        next_itemsets_bitsets[candidate] = candidate_bitset
                        
        if next_itemsets_bitsets:
            high_utility_itemsets[k] = set(next_itemsets_bitsets.keys())
            current_itemsets_bitsets = next_itemsets_bitsets
        else:
            break
        k += 1
        
    return high_utility_itemsets, candidates_generated
```

### 4.3.1 Level-1 filtering

`item_utils[item]` sums utilities **over all transactions** where the item appears (global item utility). The code keeps singletons with **global utility ≥ threshold**.

**Relation to textbook HUIM:** Classical HUIM definitions often use **transaction-weighted utility** (TWU) and **remaining utility** upper bounds for pruning. This implementation uses a **simpler** global item filter at *k=1* and then relies on **vertical joins** at higher *k*. That is easier to code and sufficient for a **controlled** course comparison, but it is **not** a faithful reimplementation of HUI-Miner/FHM-style pruning—see [09-design-tradeoffs-and-limitations.md](09-design-tradeoffs-and-limitations.md).

### 4.3.2 Binary fast path

If **every** parsed utility is exactly `1.0`, `is_binary` stays true. Then for candidate *X*:

\[
\text{utility}(X) \;=\; |X| \times \text{support}(X)
\]

because each contributing transaction adds \(\sum_{i \in X} 1 = |X|\).

**Consequence:** On standard FIM files, HUIM’s metric becomes a **monotone transform** of support with an extra **|X|** factor. It is **not** the same decision boundary as Apriori unless thresholds are chosen consistently—`evaluate.py` maps `min_utility_threshold = min_sup_count * 1.0` as an **engineering approximation** for apples-to-apples runtime experiments, not a claim of equivalent output sets.

### 4.3.3 Weighted (non-binary) path

For each TID bit set in `candidate_bitset`, sum **actual utilities** of all items in the candidate **for that transaction**. This matches the intuitive definition “utility of itemset X in transaction t = sum of utilities of items of X in t,” aggregated over all transactions containing all items of X.

**Complexity:** O(number of 1 bits × |candidate|) per candidate—more expensive than popcount; reflects real weighted mining cost.

### 4.3.4 Early skip

If `candidate_bitset == 0`, no transaction contains the full candidate; utility is 0; skip.

## 4.4 How HUIM is positioned in reports

- **Qualitative:** HUIM is the hook for **utility-aware** analytics and weighted retail data (`online_retail_utility.dat`).
- **Quantitative:** On binary benchmarks, HUIM may run **slower** than optimized Apriori while doing **similar bitwise work** plus branching and (for non-binary) extra scans—README already notes slower wall time in one configuration.

## 4.5 Summary

`huim_algorithm.py` is best understood as:

1. **Demonstration** of extending the vertical/bitset machinery to a **different objective function** (utility).
2. A **bridge** to the retail conversion pipeline (item,price tokens).
3. A **conversation starter** about what “2022+ SOTA” really means—**full** modern HUIM algorithms are more complex than this file, but the **project’s narrative** (utility matters; weighted data paths exist) remains valid.
