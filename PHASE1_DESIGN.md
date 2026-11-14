# MINI COURIER PLANNER
## Phase 1: Courier Problem Design and Planning

### 1. Problem Definition

The Mini Courier Planner is a route planning and
decision optimization system designed to improve
courier delivery operations.

The system represents delivery locations as graph
vertices and roads as weighted edges.

The weight of each edge represents the distance
between two locations in kilometers.

The main objective is to identify efficient delivery
routes and optimize package distribution.

### 2. Project Objectives

1. Represent delivery locations using graphs.
2. Store road distances using weighted edges.
3. Implement Adjacency Matrix and Adjacency List.
4. Select suitable algorithms for courier operations.
5. Find shortest paths between locations.
6. Prioritize packages based on deadlines and priority.
7. Optimize vehicle loading based on capacity.
8. Analyze algorithm performance.

### 3. Graph Design

Graph Type: Undirected Weighted Graph

Vertices: Delivery locations.

Edges: Roads connecting two locations.

Edge Weight: Distance in kilometers.

Sample Locations:

1. Courier Hub
2. North Zone
3. East Zone
4. South Zone
5. West Zone
6. Central Zone

### 4. Dataset Design

Two CSV datasets are used.

locations.csv:
- id
- name

roads.csv:
- from
- to
- distance_km

All sample road distances are positive.

### 5. Algorithm Selection

| Algorithm | Application |
|---|---|
| Adjacency Matrix | Graph representation |
| Adjacency List | Graph representation |
| Merge Sort | Package sorting |
| Greedy | Delivery decisions |
| 0/1 Knapsack | Vehicle loading |
| Dijkstra | Shortest path |
| Bellman-Ford | Negative cycle detection |
| Nearest Neighbor | Approximate delivery tour |

### 6. Algorithm Suitability

Adjacency Matrix provides fast edge lookup but
requires O(V^2) space.

Adjacency List is suitable for sparse graphs and
requires O(V + E) space.

Merge Sort provides O(n log n) sorting.

Greedy algorithms make locally optimal choices.

0/1 Knapsack uses Dynamic Programming to optimize
package selection under vehicle capacity.

Dijkstra calculates shortest paths for non-negative
road distances.

Bellman-Ford supports negative weights and detects
reachable negative weight cycles.

Nearest Neighbor provides an approximate solution
for visiting multiple delivery locations.

### 7. System Assumptions

1. Every location has a unique ID.
2. Roads are undirected.
3. Road distances are positive.
4. Duplicate roads are not allowed.
5. Sample distances are demonstration values.
6. Real-time traffic is not included in Phase 1.

### 8. Conclusion

Phase 1 establishes the problem definition,
graph structure, sample dataset and algorithm
selection for the Mini Courier Planner.

The designed foundation will be used in the
following phases to implement package
prioritization, vehicle loading, route optimization
and performance testing.