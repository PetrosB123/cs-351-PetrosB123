import random
import time
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
import math


def three_sum_brute_force(arr: List[int]) -> Tuple[int, int]:
    """
    Count triplets that sum to exactly 0 using brute force
    
    Args:
        arr: List of integers
        
    Returns:
        Tuple of (count of zero-sum triplets, number of comparisons made)
        
    Time Complexity: O(n^3)
    Space Complexity: O(1)
    """

    # Make sure input is an array
    if not isinstance(arr, list):
        raise TypeError(f"Input '{arr}' not of type 'Array'")

    count = 0
    n = len(arr)
    comparisons = 0

    # Make sure array is long enought to compare at least once
    if n < 3:
        raise IndexError("Array size smaller than 3")
    
    # Triple for loop comparison
    for i in range(n-2):
        for j in range(i + 1, n-1):
            for e in range(j + 1, n):
                comparisons += 1
                if arr[i] + arr[j] + arr[e] == 0:
                    count += 1
    
    return count, comparisons

# Seed input (defaults to '54321')
inp_seed = input("Input a seed (or don't - Default Seed = 54321)")
try: 
    random.seed(int(inp_seed))
except:
    random.seed(54321)

arr_lengths = [50, 100, 200, 400, 800]
three_sum_brute_force([1,2,3])

full_test = input("Run full test?")

if full_test.lower() in ["no", "n"]:
    run_times = 1
else:
    run_times = 10

results = [[] for i in range(len(arr_lengths))]
for j in range(run_times):
    for i in range(len(arr_lengths)):
        start = time.perf_counter()
        count, comparisons = three_sum_brute_force([random.randint(-100, 100) for i in range(arr_lengths[i])])
        total_time = time.perf_counter() - start
        results[i].append([total_time, comparisons])

print("Array Size | Runtime | Operations Count")
times = []
ops = []
for i in range(len(results)):
    total_time = 0
    for j in range(len(results[i])):
        total_time += results[i][j][0]
        if j == len(results[i]) - 1:
            avg_time = total_time/len(results[i])
            print(f"{arr_lengths[i]} | {avg_time} | {results[i][j][1]}")
            times.append(avg_time)
            ops.append(results[i][j][1])


# Input Size/Seconds
# Create standard plot
fig, ax1 = plt.subplots(figsize=(10, 10))

# Standard scale plot
ax1.plot(arr_lengths, times, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Input Size (N)', fontsize=12)
ax1.set_ylabel('Time (seconds)', fontsize=12)
ax1.set_title('3Sum Brute Force Performance', fontsize=14)
ax1.grid(True, alpha=0.3)

# Add annotations
for i, (x, y) in enumerate(zip(arr_lengths, times)):
    ax1.annotate(f'({x}, {y:.2f})', 
                xy=(x, y), 
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9)
    
# Input Size/Operations
# Create standard plot
fig, ax2 = plt.subplots(figsize=(10, 10))

# Standard scale plot
ax2.plot(arr_lengths, ops, 'bo-', linewidth=2, markersize=8)
ax2.set_xlabel('Input Size (N)', fontsize=12)
ax2.set_ylabel('Operations', fontsize=12)
ax2.set_title('3Sum Brute Force Performance', fontsize=14)
ax2.grid(True, alpha=0.3)

# Add annotations
for i, (x, y) in enumerate(zip(arr_lengths, ops)):
    ax2.annotate(f'({x}, {y:.2f})', 
                xy=(x, y), 
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9)

# Use linear regression for more accurate slope
log_N = np.log10(arr_lengths)
log_T = np.log10(times)

# Perform linear regression
slope, intercept = np.polyfit(log_N, log_T, 1)
print(f"Linear regression slope: {slope:.4f}")
print(f"Linear regression intercept: {intercept:.4f}")

# Calculate the scaling constant a
a = 10**intercept
print(f"Scaling constant a = {a:.6f}")


# Calculate slope using two points
N1, T1 = arr_lengths[0], times[0]
N2, T2 = arr_lengths[1], times[1]

b = (math.log10(T2) - math.log10(T1)) / (math.log10(N2) - math.log10(N1))
print(f"Calculated slope b = {b:.4f}")
    
def project_time(N, a, b):
    """Project time using power law T(N) = a * N^b"""
    return a * (N ** b)


fig, ax3 = plt.subplots(figsize=(10, 10))
# Standard scale with projections
ax3.plot(arr_lengths, times, 'bo-', label='Empirical', markersize=8)
theoretical_projected = [project_time(n, a, b) for n in arr_lengths]
ax3.plot(arr_lengths, theoretical_projected, 'r--', label='Projected', linewidth=2)
ax3.set_xlabel('Input Size (N)')
ax3.set_ylabel('Time (seconds)')
ax3.set_title('3Sum: Empirical vs Projected')
ax3.legend()
ax3.grid(True, alpha=0.3)
    
plt.show()