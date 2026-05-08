import random

def generate_dataset(filename, num_transactions, num_items, min_length, max_length):
    with open(filename, 'w') as f:
        for _ in range(num_transactions):
            length = random.randint(min_length, max_length)
            items = random.sample(range(1, num_items + 1), length)
            items.sort()
            f.write(" ".join(map(str, items)) + "\n")

print('Generating synthetic datasets...')
generate_dataset('../datasets/chess.dat', 3196, 75, 30, 40)
generate_dataset('../datasets/connect.dat', 10000, 129, 35, 43)  # Downsized for rapid testing
generate_dataset('../datasets/accidents.dat', 15000, 468, 20, 45) # Downsized for rapid testing
print('Finished generating synthetic datasets.')
