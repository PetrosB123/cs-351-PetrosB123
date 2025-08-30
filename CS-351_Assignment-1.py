import time
import random

def time_algorithm(algo, arr):
    start = time.time()
    algo(arr.copy())
    return time.time() - start

# Starter code
def selection_sort(arr):
    new_arr = []
    while len(arr) > 0:
        lowest_num = arr[0]
        for num in arr:
            if num < lowest_num:
                lowest_num = num
        new_arr.append(lowest_num)
        arr.remove(lowest_num)
    return new_arr

def merge_sort(arr):
    if len(arr) <= 2:
        return arr
    split_arr = []
    split_arr.append(arr[:len(arr)//2])
    split_arr.append(arr[len(arr)//2:])

    left_arr = merge_sort(split_arr[0])
    right_arr = merge_sort(split_arr[1])
    
    return merge(left_arr, right_arr)

def merge(C, D):
    i = j = 0
    B = []
    
    while i < len(C) and j < len(D):
        if C[i] < D[j]:
            B.append(C[i])
            i += 1
        else:
            B.append(D[j])
            j += 1
    
    # Add remaining elements
    B.extend(C[i:])
    B.extend(D[j:])
    return B


random.seed(3609218026)
n = 1000
arr = random.sample(range(1, n+1), n)
selection_sort(arr)
merge_sort(arr)
print(f"Selection sort time - {time_algorithm(selection_sort, arr)}")
print(f"Merge sort time - {time_algorithm(merge_sort, arr)}")