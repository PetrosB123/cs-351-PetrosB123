import time
import random
import numpy as np
import matplotlib.pyplot as plt
import math

def generate_test_data(n):
    """Generate n distinct random integers"""
    # Create a set to ensure distinct values
    data = set()
    while len(data) < n:
        # Generate random integers in range [-n*10, n*10]
        val = random.randint(-n*10, n*10)
        data.add(val)
    return list(data)

def time_two_sum(n):
    """Time the two_sum function for input size n"""
    data = generate_test_data(n)
    
    start_time = time.perf_counter()
    count = two_sum(data)
    end_time = time.perf_counter()
    
    elapsed_time = end_time - start_time
    return elapsed_time


def two_sum(arr):
    """
    Count pairs that sum to exactly 0
    """
    count = 0
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == 0:
                count += 1
    
    return count


def run_experiments():
    """Run experiments for different input sizes"""
    sizes = [1000, 2000, 4000, 8000, 16000]
    times = []
    
    print(f"{'N':>10}{'Time (seconds)':>20}")
    print("-" * 30)
    
    for n in sizes:
        # Run multiple trials and take average
        trial_times = []
        for _ in range(3):  # 3 trials per size
            trial_time = time_two_sum(n)
            trial_times.append(trial_time)
        
        avg_time = sum(trial_times) / len(trial_times)
        times.append(avg_time)
        print(f"{n:10}{avg_time:20.4f}")
    
    return sizes, times

# Run the experiments
sizes, times = run_experiments()



# Create standard plot
fig, ax1 = plt.subplots(figsize=(10, 10))

# Standard scale plot
ax1.plot(sizes, times, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Input Size (N)', fontsize=12)
ax1.set_ylabel('Time (seconds)', fontsize=12)
ax1.set_title('2Sum Algorithm Performance', fontsize=14)
ax1.grid(True, alpha=0.3)

# Add annotations
for i, (x, y) in enumerate(zip(sizes, times)):
    ax1.annotate(f'({x}, {y:.2f})', 
                xy=(x, y), 
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9)

# Log-log plot
fig, ax2 = plt.subplots(figsize=(6, 4))

ax2.loglog(sizes, times, 'ro-', linewidth=2, markersize=8, label='Empirical')
ax2.set_xlabel('Input Size (N) - log scale', fontsize=12)
ax2.set_ylabel('Time (seconds) - log scale', fontsize=12)
ax2.set_title('2Sum Log-Log Plot', fontsize=14)
ax2.grid(True, which="both", ls="-", alpha=0.2)
ax2.legend()

plt.tight_layout()

# Use linear regression for more accurate slope
log_N = np.log10(sizes)
log_T = np.log10(times)

# Perform linear regression
slope, intercept = np.polyfit(log_N, log_T, 1)
print(f"Linear regression slope: {slope:.4f}")
print(f"Linear regression intercept: {intercept:.4f}")

# Calculate the scaling constant a
a = 10**intercept
print(f"Scaling constant a = {a:.6f}")


# Calculate slope using two points
N1, T1 = 4000, 0.6734
N2, T2 = 8000, 2.6951

b = (math.log10(T2) - math.log10(T1)) / (math.log10(N2) - math.log10(N1))
print(f"Calculated slope b = {b:.4f}")

# Alternative: Using natural logarithm
b_ln = (math.log(T2) - math.log(T1)) / (math.log(N2) - math.log(N1))
print(f"Slope using ln: b = {b_ln:.4f}")



def project_time(N, a, b):
    """Project time using power law T(N) = a * N^b"""
    return a * (N ** b)

# Use our calculated values
a = a  # scaling constant
b = b    # exponent

# Generate projections
test_sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 100000]
projected_times = [project_time(n, a, b) for n in test_sizes]

print(f"{'N':>10}{'Empirical':>15}{'Projected':>15}{'Error (%)':>15}")
print("-" * 55)

for i, n in enumerate(sizes):
    emp_time = times[i]
    proj_time = project_time(n, a, b)
    error = abs(emp_time - proj_time) / emp_time * 100
    print(f"{n:10}{emp_time:15.4f}{proj_time:15.4f}{error:15.2f}")

# Add future projections
for n in [32000, 64000, 100000]:
    proj_time = project_time(n, a, b)
    print(f"{n:10}{'--':>15}{proj_time:15.4f}{'--':>15}")



# Create comprehensive visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Standard scale with projections
ax = axes[0, 0]
ax.plot(sizes, times, 'bo-', label='Empirical', markersize=8)
extended_sizes = sizes + [32000, 64000]
extended_projected = [project_time(n, a, b) for n in extended_sizes]
ax.plot(extended_sizes, extended_projected, 'r--', label='Projected', linewidth=2)
ax.set_xlabel('Input Size (N)')
ax.set_ylabel('Time (seconds)')
ax.set_title('2Sum: Empirical vs Projected')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Log-log with regression line
ax = axes[0, 1]
ax.loglog(sizes, times, 'bo', label='Empirical Data', markersize=8)
# Add regression line
N_range = np.logspace(np.log10(min(sizes)), np.log10(max(sizes)*2), 100)
T_fitted = a * N_range**b
ax.loglog(N_range, T_fitted, 'r-', label=f'Fitted: T = {a:.2e} * N^{b:.3f}', linewidth=2)
ax.set_xlabel('Input Size (N)')
ax.set_ylabel('Time (seconds)')
ax.set_title('2Sum Log-Log Plot with Power Law Fit')
ax.legend()
ax.grid(True, which="both", ls="-", alpha=0.2)

# Plot 3: Residuals
ax = axes[1, 0]
residuals = [times[i] - project_time(n, a, b) for i, n in enumerate(sizes)]
ax.bar(range(len(sizes)), residuals, color='g', alpha=0.7)
ax.set_xticks(range(len(sizes)))
ax.set_xticklabels(sizes)
ax.set_xlabel('Input Size (N)')
ax.set_ylabel('Residual (Empirical - Projected)')
ax.set_title('Residuals Analysis')
ax.axhline(y=0, color='r', linestyle='--')
ax.grid(True, alpha=0.3)

# Plot 4: Growth rate comparison
ax = axes[1, 1]
growth_rates = [times[i]/times[i-1] if i > 0 else 0 for i in range(len(times))]
theoretical_growth = [4.0] * len(sizes)  # N^2 growth means 4x when doubling
ax.plot(sizes[1:], growth_rates[1:], 'bo-', label='Empirical Growth Rate', markersize=8)
ax.axhline(y=4.0, color='r', linestyle='--', label='Theoretical (4x for N^2)')
ax.set_xlabel('Input Size (N)')
ax.set_ylabel('Time Ratio (T(N) / T(N/2))')
ax.set_title('Growth Rate Analysis')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()