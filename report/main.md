# IEEE Conference Report Draft

## Title: Comparison of Apriori Algorithm for Frequent Itemset Mining with State-of-the-Art Algorithms and Optimization Strategies for Improved Performance

### Abstract
Frequent Itemset Mining (FIM) is a foundational task in data mining heavily utilized for generating actionable association rules. This study evaluates the classical Apriori algorithm against modern optimizations and state-of-the-art implementations. We propose two primary optimizations: **Transaction Reduction using Vertical Data Formats (TID-sets)** and **Bitset Intersection**, drastically resolving the I/O bottleneck of the classical approach.

### 1. Introduction
Discuss FIM, its real-world impact, and the computational complexity it entails. Note the problem constraints with classical Apriori such as exponential candidate generation and repeated database scans.

### 2. Literature Review
Mention the original paper by Agrawal & Srikant (1994) and review a recent algorithm (e.g., modern Eclat variants or diffset architectures >= 2022). Discuss the gaps.

### 3. Algorithms: Description and Analysis
- **Classical Apriori:** Generate-and-test, level-wise search, horizontal data formatting. $O(2^d)$ complexity in worst-case candidate generation.
- **State-of-the-Art / Optimizations:** Vertical data formats eliminate repeat database scans substituting them with set intersections.

### 4. Proposed Optimization Strategies
- **Optimization 1 (Vertical Tid-Sets):** Replacing raw database scans with tid-list intersections (Eclat inspiration).
- **Optimization 2 (Transaction Pruning):** Avoid looping through non-viable candidates early.

### 5. Experimental Setup and Results
Testing against FIMI benchmark datasets (Connect, Chess, Accident).
Include tables depicting Memory usage (MB) and Runtime (ms).

### 6. Discussion & 7. Conclusion
Analyse how the classical algorithm choked on dense datasets like `Connect`, forcing the optimization strategies to handle the sparsity constraints natively via set operations.

### References
[1] R. Agrawal and R. Srikant, "Fast algorithms for mining association rules", Proc. 20th Int. Conf. Very Large Data Bases, VLDB, pp. 487-499, 1994.
[2] [Insert selected 2022+ paper here, e.g. on High-Utility or Diffset FIM]
