# MINI COURIER PLANNER
## Phase 2: Package Prioritization and Route Filling

### 1. Introduction

Phase 2 focuses on package prioritization and
optimal vehicle loading.

The system sorts packages using delivery deadlines
and priority levels.

Dynamic Programming is used to select packages
within the vehicle's maximum weight capacity.

### 2. Dataset

The packages dataset contains:

- Package ID
- Destination ID
- Weight
- Priority
- Delivery Deadline
- Benefit Score

Total Packages: 8

Vehicle Capacity: 15 kg

### 3. Sorting Algorithms

#### A. Merge Sort

Merge Sort arranges packages in ascending order
of delivery deadlines.

Time Complexity: O(n log n)

#### B. Insertion Sort

Insertion Sort arranges packages according to
priority:

High > Medium > Low

For equal priority, earlier deadlines are preferred.

Time Complexity: O(n^2)

### 4. Dynamic Programming

Algorithm: 0/1 Knapsack

Objective: Maximize total package benefit while
keeping total package weight within vehicle capacity.

DP Recurrence:

DP[i][w] = max(
    DP[i-1][w],
    benefit[i] + DP[i-1][w-weight[i]]
)

The second option is considered only when the
package weight does not exceed available capacity.

Time Complexity: O(n * W)

Space Complexity: O(n * W)

### 5. Optimal Package Selection

Selected Packages:

P101, P102, P105, P107

Total Loaded Weight: 14 kg

Vehicle Capacity: 15 kg

Remaining Capacity: 1 kg

Total Benefit: 370

### 6. Results

The system successfully:

1. Sorted packages by delivery deadline.
2. Sorted packages by priority.
3. Generated the Dynamic Programming table.
4. Selected an optimal package combination.
5. Ensured that vehicle capacity was not exceeded.

### 7. Conclusion

Phase 2 successfully implements two sorting
algorithms and a Dynamic Programming based
vehicle loading system.

The system maximizes total package benefit
while satisfying the vehicle capacity constraint.