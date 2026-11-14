# MINI COURIER PLANNER
## Phase 4: Performance Testing and Optimization

### 1. Introduction

Phase 4 evaluates the performance of the
algorithms implemented in the courier planner.

Small and larger datasets are used to measure
execution time.

### 2. Testing Methodology

Python time.perf_counter() is used to measure
algorithm execution time.

Each test is repeated three times.

The median execution time is recorded.

### 3. Algorithms Tested

1. Dijkstra
2. Bellman-Ford
3. Merge Sort
4. Insertion Sort
5. 0/1 Knapsack
6. Nearest Neighbor

### 4. Dataset Sizes

Graph algorithms:
- 30 vertices
- 80 vertices

Sorting algorithms:
- 500 packages
- 2000 packages

Knapsack:
- 25 packages, capacity 100
- 50 packages, capacity 200

### 5. Complexity Analysis

Dijkstra: O(V^2 + E)

Bellman-Ford: O(V * E)

Merge Sort: O(n log n)

Insertion Sort: O(n^2)

0/1 Knapsack: O(n * W)

Nearest Neighbor:
O(V * (V^2 + E))

### 6. Optimization Suggestions

1. Use a Min Heap for Dijkstra.
2. Use adjacency lists for sparse graphs.
3. Prefer Merge Sort for large datasets.
4. Use one-dimensional DP to reduce Knapsack memory.
5. Cache repeated shortest path calculations.
6. Test using larger real-world datasets.

### 7. Validation

The system checks:
- Shortest path connectivity.
- Negative cycle status.
- Sorting correctness.
- Vehicle capacity.
- Delivery route start and end points.

### 8. Conclusion

Phase 4 measures the execution time of major
algorithms and identifies optimization
opportunities.

The testing helps evaluate the scalability
and efficiency of the Mini Courier Planner.