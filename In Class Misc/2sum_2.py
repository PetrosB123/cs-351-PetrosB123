import time
import random
from typing import List, Tuple, Dict

def twosum_brute_force(nums, target):
    """
    Brute force approach: Check all pairs
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    n = len(nums)
    comparisons = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            comparisons += 1
            if nums[i] + nums[j] == target:
                return [i, j], comparisons
    
    return None, comparisons


def twosum_hash_table(nums, target):
    """
    Hash table approach: One-pass solution
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = {}  # Hash table to store value -> index mapping
    lookups = 0
    
    for i, num in enumerate(nums):
        complement = target - num
        lookups += 1
        
        if complement in seen:
            return [seen[complement], i], lookups
        
        seen[num] = i
    
    return None, lookups


nums = [2, 7, 11, 15]
target = 9

# Test the brute force solution
result, comps = twosum_brute_force(nums, target)
print(f"Result: {result}")
print(f"Comparisons made: {comps}")

# Test the hash table solution
result, lookups = twosum_hash_table(nums, target)
print(f"Result: {result}")
print(f"Hash lookups made: {lookups}")



def two_sum_brute_force(arr: List[int]) -> Tuple[int, int]:
    """
    Count pairs that sum to exactly 0 using brute force
    
    Args:
        arr: List of integers
        
    Returns:
        Tuple of (count of zero-sum pairs, number of comparisons made)
        
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    count = 0
    n = len(arr)
    comparisons = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            comparisons += 1
            if arr[i] + arr[j] == 0:
                count += 1
    
    return count, comparisons

# Test the brute force solution
test_arrays = [
    [1, -1, 2, -2, 3],
    [0, 0, 0],
    [5, -5, 10, -10, 5, -5],
    [1, 2, 3, 4, 5]
]

for arr in test_arrays:
    result, comps = two_sum_brute_force(arr)
    print(f"Array: {arr}")
    print(f"  Zero-sum pairs: {result}")
    print(f"  Comparisons made: {comps}")
    print()


def two_sum_hash_table(arr: List[int]) -> Tuple[int, int]:
    """
    Count pairs that sum to exactly 0 using hash table
    
    Args:
        arr: List of integers
        
    Returns:
        Tuple of (count of zero-sum pairs, number of lookups made)
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    frequency: Dict[int, int] = {}
    lookups = 0
    
    # First pass: count frequencies
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
        lookups += 1
    
    count = 0
    processed: set = set()
    
    # Second pass: count pairs
    for num in frequency:
        lookups += 1
        
        if num in processed:
            continue
            
        if num == 0:
            # Special case: pairs of zeros
            # Choose 2 from frequency[0] zeros: C(n,2) = n*(n-1)/2
            zeros = frequency[0]
            count += (zeros * (zeros - 1)) // 2
        elif -num in frequency:
            # Regular case: positive-negative pairs
            # Each positive can pair with each negative
            count += frequency[num] * frequency[-num]
            processed.add(num)
            processed.add(-num)
    
    return count, lookups

# Test the hash table solution
test_arrays = [
    [1, -1, 2, -2, 3],
    [0, 0, 0],
    [5, -5, 10, -10, 5, -5],
    [1, 2, 3, 4, 5]
]

print("Hash Table Approach Results:")
print("-" * 50)
for arr in test_arrays:
    result, lookups = two_sum_hash_table(arr)
    print(f"Array: {arr}")
    print(f"  Zero-sum pairs: {result}")
    print(f"  Hash operations: {lookups}")
    print()