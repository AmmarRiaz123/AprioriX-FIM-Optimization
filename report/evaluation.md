## Evaluation Details & Code Map

### Implemented Requirements:
1. **Classical Apriori (`src/apriori.py`)**: 
   - Uses Breadth-First-Search and generate-and-test candidate processing.
   - Exhaustive horizontal parsing of the dataset per level.
2. **State-of-the-art Optimization (`src/optimized_apriori.py`)**: 
   - Based on Vertical Data Framing (TID sets) commonly cited in recent High-Utility & Diffset approaches. It substitutes memory-expensive scans in favor of intersection sets (equivalent to bitwise operations proxy).
3. **Benchmarking Framework (`src/benchmark.py`)**:
   - Collects peak RAM usage in MB using `psutil`.
   - Records execution wall-clock time in ms.
   - Calculates total distinct frequent itemsets resulting from both approaches sequentially dynamically based on `min_sup`.
4. **IEEE Report Shell (`report/main.md`)**:
   - Laid out exactly conforming to sections 8.1 through 8.9 of your instructions (Abstract, Lit Review, Algo Analysis, Results, Conclusions, etc).

### Next Steps (For the Student Group)
- Run `benchmark.py` on all 3 datasets via the terminal to collect the precise values for your tables.
- Render the `main.md` file using an IEEE LaTeX conference template (or Word format).
- Complete Section 8.3 & References by looking up standard FIM algorithms released from 2022+ (e.g., modern FP-Growth variants in IoT contexts).
