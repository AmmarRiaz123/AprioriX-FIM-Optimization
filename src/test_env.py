
import os
import sys
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
try:
    import psutil
    print("psutil imported")
except ImportError:
    print("psutil NOT found")
try:
    from apriori import load_transactions
    print("apriori imported")
except Exception as e:
    print(f"apriori import FAILED: {e}")
