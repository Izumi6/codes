# STEP 1: Accept size of bucket
n = int(input("Enter size of bucket: "))
bucket = [-1] * n
complexity = [-1] * n

# STEP 2: Hash function (Division Method)
def hashDiv(telephone):
    return int(telephone) % n

# STEP 3: Accept telephone numbers <= size of bucket
def acceptKeys():
    while True:
        num_keys = int(input("Enter number of telephone numbers to insert (<= bucket size): "))
        if num_keys <= n:
            break
        print("Number of keys must not exceed bucket size.")
    
    keys = []
    for i in range(num_keys):
        tel = input(f"Enter telephone number {i + 1}: ")
        keys.append(tel)
    return keys

# STEP 4: Insert keys and handle collisions
keys = acceptKeys()
bucket = [-1] * n
complexity = [-1] * n
collisions = []

for key in keys:
    idx = hashDiv(key)
    if bucket[idx] == -1:
        bucket[idx] = key
        complexity[idx] = 'O(1)'
    else:
        print(f"Collision at index {idx} for telephone number {key}")
        collisions.append(key)

# Display current status
print("\nInitial Bucket Contents:", bucket)
print("Insertion Complexity:", complexity)
density = (n - bucket.count(-1)) / n * 100
print(f"Density of the bucket: {density:.2f}%")
print("Collisions:", collisions)

# Check if position is free
def isCollision(index):
    return bucket[index] != -1

# Linear Probing
def linear_probing(coll, bucket, complexity):
    for key in coll:
        original_idx = hashDiv(key)
        idx = original_idx
        offset = 1
        while isCollision(idx):
            idx = (original_idx + offset) % n
            offset += 1
        bucket[idx] = key
        complexity[idx] = f'O({offset})'
        print(f"Key {key} inserted successfully at index: {idx}")

# Quadratic Probing
def quadratic_probing(coll, bucket, complexity):
    for key in coll:
        original_idx = hashDiv(key)
        offset = 1
        idx = original_idx
        while isCollision(idx):
            idx = (original_idx + offset ** 2) % n
            offset += 1
            if offset > n:
                print(f"Cannot insert {key}, quadratic probing failed.")
                break
        else:
            bucket[idx] = key
            complexity[idx] = f'O({offset})'
            print(f"Key {key} inserted successfully at index: {idx}")

# STEP 5: Choose collision resolution method
while True:
    print("\nChoose collision resolution technique:")
    print("1. Linear Probing")
    print("2. Quadratic Probing")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        linear_probing(collisions, bucket, complexity)
        print("-" * 10, "Linear Probing Complete", "-" * 10)
        break
    elif choice == 2:
        quadratic_probing(collisions, bucket, complexity)
        print("-" * 10, "Quadratic Probing Complete", "-" * 10)
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")

# Final Output
print("\nFinal Bucket:", bucket)
print("Final Complexity:", complexity)
