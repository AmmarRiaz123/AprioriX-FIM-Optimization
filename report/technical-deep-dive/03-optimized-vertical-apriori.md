# 3. Optimized vertical Apriori (`src/optimized_apriori.py`)

## 3.1 Purpose in the project

This module is the project’s **primary optimization story**: replace **repeated horizontal scans** with **vertical tidset operations**, implemented as **Python integers used as bitsets**. Support for an itemset becomes the **population count** (number of 1 bits) of the intersection of the itemsets’ tidsets.

Conceptually, this is in the family of **vertical Apriori / Eclat**: store, for each frequent itemset, the set of transaction IDs where it appears; extend itemsets by **intersecting** tidsets instead of scanning the full database.

## 3.2 Loading: `load_transactions_bitsets`

```8:18:src/optimized_apriori.py
def load_transactions_bitsets(filepath):
    bitsets = {}
    num_transactions = 0
    with open(filepath, 'r') as file:
        for tid, line in enumerate(file):
            items = line.strip().split()
            for item in items:
                if item not in bitsets:
                    bitsets[item] = 0
                bitsets[item] |= (1 << tid)
            num_transactions += 1
    return bitsets, num_transactions
```

**Mechanics:**

- Transaction index **`tid`** runs `0 .. n-1` in file order.
- For each item, accumulate a **big integer** whose *tid*-th bit is 1 if the item appears in that transaction.
- **`|=` OR with `1 << tid`**: idempotent for duplicate items in a line only if duplicates existed—they would set the same bit twice (still 1). FIMI data is usually duplicate-free per line; retail conversion uses sets to dedupe.

**Why this is faster than horizontal counting (empirically):**

- Counting a candidate no longer iterates all transactions; it is **one bitwise AND** plus a bit count on the intersection bitset.
- Join step still enumerates pairs of frequent itemsets, but the **per-candidate** work shifts from O(|D|) subset tests to O(1) machine-word-friendly operations **in principle**—though Python’s big integers and `bin(x).count('1')` are not as fast as SIMD popcount on fixed-width arrays (see limitations doc).

## 3.3 Mining loop: `vertical_apriori`

```21:69:src/optimized_apriori.py
def vertical_apriori(filepath, min_sup_count):
    bitsets, num_transactions = load_transactions_bitsets(filepath)
    
    # Filter frequent 1-itemsets
    f1_bitsets = {}
    for item, bitset in bitsets.items():
        support = bin(bitset).count('1')
        if support >= min_sup_count:
            f1_bitsets[frozenset([item])] = bitset
            
    frequent_itemsets = {1: set(f1_bitsets.keys())}
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
                
                # Join condition (same prefix)
                l1 = sorted(list(itemset1))[:-1]
                l2 = sorted(list(itemset2))[:-1]
                
                if l1 == l2:
                    candidate = itemset1.union(itemset2)
                    candidates_generated += 1
                    
                    # Optimization: Bitwise AND intersection (Fast)
                    candidate_bitset = current_itemsets_bitsets[itemset1] & current_itemsets_bitsets[itemset2]
                    
                    # Count support using bitset population count
                    support = bin(candidate_bitset).count('1')
                    
                    if support >= min_sup_count:
                        next_itemsets_bitsets[candidate] = candidate_bitset
                        
        if next_itemsets_bitsets:
            frequent_itemsets[k] = set(next_itemsets_bitsets.keys())
            current_itemsets_bitsets = next_itemsets_bitsets
        else:
            break
        k += 1
        
    return frequent_itemsets, candidates_generated
```

### 3.3.1 Frequent 1-itemsets

Single-item support = popcount of its item bitset. Frequent singletons seed **`current_itemsets_bitsets`**: a map from **`frozenset` itemset** → **intersection bitset** representing its tidset.

### 3.3.2 Join condition

For two itemsets *A*, *B* of size *k−1*, sort items and compare **`sorted[:-1]`** (all but last). This is the usual **Apriori-style prefix join** adapted to arbitrary item labels (strings).

### 3.3.3 Implicit pruning vs classical `apriori_gen`

This loop **does not** explicitly run the “all *(k−1)* subsets must be frequent” test. Instead:

- It only joins **already frequent** *(k−1)*-itemsets from the **current** level.
- Any *(k−1)* subset of the joined candidate that misses one item is not directly verified here.

**Important nuance:** In a strict Apriori implementation, you must ensure subset closure. This code relies on the property that if you only extend from the known frequent level and your join is correct, candidates that survive intersection are **sound**, but **completeness** normally requires the same subset pruning as classical Apriori. In practice, for typical implementations starting from all frequent singletons and using prefix joins on the **current** frontier, this pattern often matches the classical output when the join strategy matches—**the team’s empirical benchmarks** are the operational check. For a formal proof in a course setting, you would align this join/prune with the textbook variant explicitly.

### 3.3.4 Support test

`candidate_bitset = bitset(A) & bitset(B)` is the tidset of **A ∪ B** when `bitset(X)` already stores transactions containing all items in *X*—because tidset of union = **intersection** of tidsets.

### 3.3.5 Return shape

- **`frequent_itemsets`**: dict keyed by **itemset size** (1, 2, …) mapping to `set` of `frozenset`s (no bitsets in the value sets—only keys in the internal dict carry bitsets).
- **`candidates_generated`**: incremented for **every join attempt** that passes prefix equality, regardless of eventual frequency.

This differs slightly from `apriori.py`’s candidate accounting (which counts `len(candidates)` after `apriori_gen`), but both are **monotonic indicators** of search breadth.

## 3.4 Interface contrast with baseline

| | `apriori.apriori` | `optimized_apriori.vertical_apriori` |
|--|-------------------|--------------------------------------|
| Input | In-memory `list[set]` | File path (reads again internally) |
| Threshold | `min_sup_count` | `min_sup_count` |
| Output levels | Keys `k-1` style | Keys `1,2,3,...` by size |

`evaluate.py` intentionally passes **`dataset_path`** to the vertical miner so it can build bitsets from disk without duplicating the horizontal structure.

## 3.5 Engineering takeaway

The module demonstrates **algorithm + data structure co-design**: the same Apriori **breadth-first** idea, but counting becomes **set intersection** instead of **subset scanning**. That is the **4×+** style speedup reported on Chess-like workloads in the README—modulo Python-specific constant factors and the popcount implementation choice.
