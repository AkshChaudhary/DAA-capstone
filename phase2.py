import csv
from pathlib import Path


# ==========================================
# MINI COURIER PLANNER
# PHASE 2: PACKAGE PRIORITIZATION
# AND VEHICLE LOADING
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

VEHICLE_CAPACITY = 15

PRIORITY_RANK = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}


# ==========================================
# 1. LOAD LOCATIONS
# ==========================================

def load_locations():

    locations = {}

    file_path = DATA_DIR / "locations.csv"

    with open(file_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            locations[int(row["id"])] = row["name"]

    return locations


# ==========================================
# 2. LOAD PACKAGES
# ==========================================

def load_packages(locations):

    packages = []

    file_path = DATA_DIR / "packages.csv"

    with open(file_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            package = {
                "id": row["package_id"],
                "destination": int(row["destination_id"]),
                "weight": int(row["weight_kg"]),
                "priority": row["priority"].strip(),
                "deadline": row["deadline"].strip(),
                "benefit": int(row["benefit"])
            }

            if package["destination"] not in locations:
                raise ValueError("Invalid package destination.")

            if package["weight"] <= 0:
                raise ValueError("Package weight must be positive.")

            if package["priority"] not in PRIORITY_RANK:
                raise ValueError("Invalid package priority.")

            if package["benefit"] <= 0:
                raise ValueError("Benefit must be positive.")

            if len(package["deadline"]) != 5 or package["deadline"][2] != ":":
                raise ValueError("Deadline must use HH:MM format.")

            packages.append(package)

    if len({p["id"] for p in packages}) != len(packages):
        raise ValueError("Duplicate package ID found.")

    if not packages:
        raise ValueError("No packages found.")

    return packages


# ==========================================
# 3. MERGE SORT BY DEADLINE
# ==========================================

def merge_sort_deadline(packages):

    if len(packages) <= 1:
        return packages[:]

    mid = len(packages) // 2

    left = merge_sort_deadline(packages[:mid])
    right = merge_sort_deadline(packages[mid:])

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["deadline"] <= right[j]["deadline"]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ==========================================
# 4. INSERTION SORT BY PRIORITY
# ==========================================

def insertion_sort_priority(packages):

    result = packages[:]

    for i in range(1, len(result)):

        key = result[i]
        j = i - 1

        while j >= 0:

            current_rank = PRIORITY_RANK[result[j]["priority"]]
            key_rank = PRIORITY_RANK[key["priority"]]

            should_shift = (
                current_rank < key_rank
                or (
                    current_rank == key_rank
                    and result[j]["deadline"] > key["deadline"]
                )
            )

            if not should_shift:
                break

            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


# ==========================================
# 5. 0/1 KNAPSACK USING DYNAMIC PROGRAMMING
# ==========================================

def knapsack_dp(packages, capacity):

    n = len(packages)

    dp = [
        [0 for _ in range(capacity + 1)]
        for _ in range(n + 1)
    ]

    # Build DP table
    for i in range(1, n + 1):

        weight = packages[i - 1]["weight"]
        benefit = packages[i - 1]["benefit"]

        for w in range(capacity + 1):

            # Exclude current package
            dp[i][w] = dp[i - 1][w]

            # Include current package if possible
            if weight <= w:

                include_value = (
                    benefit + dp[i - 1][w - weight]
                )

                if include_value > dp[i][w]:
                    dp[i][w] = include_value

    # Backtracking to find selected packages
    selected = []

    remaining_capacity = capacity

    for i in range(n, 0, -1):

        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:

            package = packages[i - 1]

            selected.append(package)

            remaining_capacity -= package["weight"]

    selected.reverse()

    return dp, selected


# ==========================================
# 6. GENERATE PHASE 2 REPORT
# ==========================================

def generate_phase2_report():

    locations = load_locations()

    packages = load_packages(locations)

    result = []

    result.append("=" * 65)
    result.append("       MINI COURIER PLANNER")
    result.append("       PHASE 2: PACKAGE PRIORITIZATION")
    result.append("       AND VEHICLE LOADING")
    result.append("=" * 65)

    result.append("\n1. PACKAGE DATASET SUMMARY")

    result.append(f"Total Packages: {len(packages)}")
    result.append(f"Vehicle Capacity: {VEHICLE_CAPACITY} kg")

    result.append("\n2. MERGE SORT - DEADLINE PRIORITIZATION")

    deadline_sorted = merge_sort_deadline(packages)

    result.append(
        "Packages sorted in ascending order of delivery deadline:"
    )

    for p in deadline_sorted:

        result.append(
            f'{p["id"]} | Deadline: {p["deadline"]} | '
            f'Weight: {p["weight"]} kg | Priority: {p["priority"]}'
        )

    result.append("\n3. INSERTION SORT - PRIORITY BASED SORTING")

    priority_sorted = insertion_sort_priority(packages)

    result.append(
        "Packages sorted by High, Medium and Low priority:"
    )

    for p in priority_sorted:

        result.append(
            f'{p["id"]} | Priority: {p["priority"]} | '
            f'Deadline: {p["deadline"]} | Weight: {p["weight"]} kg'
        )

    result.append("\n4. DYNAMIC PROGRAMMING - 0/1 KNAPSACK")

    result.append(f"Maximum Vehicle Capacity: {VEHICLE_CAPACITY} kg")

    result.append("Objective: Maximize total package benefit.")

    dp, selected = knapsack_dp(
        packages,
        VEHICLE_CAPACITY
    )

    result.append("\n5. DP TABLE")

    header = "Packages | " + " ".join(
        f"{w:3}" for w in range(VEHICLE_CAPACITY + 1)
    )

    result.append(header)

    for i in range(len(dp)):

        if i == 0:
            label = "None"
        else:
            label = packages[i - 1]["id"]

        values = " ".join(
            f"{value:3}" for value in dp[i]
        )

        result.append(f"{label:8} | {values}")

    # Calculate final selection
    total_weight = sum(p["weight"] for p in selected)
    total_benefit = sum(p["benefit"] for p in selected)

    result.append("\n6. OPTIMAL SELECTED PACKAGE LIST")

    for p in selected:

        destination_name = locations[p["destination"]]

        result.append(
            f'{p["id"]} | Destination: {destination_name} | '
            f'Weight: {p["weight"]} kg | '
            f'Priority: {p["priority"]} | '
            f'Benefit: {p["benefit"]}'
        )

    result.append("\n7. FINAL VEHICLE LOADING PLAN")

    result.append(f"Vehicle Capacity: {VEHICLE_CAPACITY} kg")
    result.append(f"Total Loaded Weight: {total_weight} kg")
    result.append(f"Remaining Capacity: {VEHICLE_CAPACITY - total_weight} kg")
    result.append(f"Total Benefit: {total_benefit}")

    result.append(f"Selected Packages: {len(selected)}")
    result.append(f"Rejected Packages: {len(packages) - len(selected)}")

    result.append("\n8. ALGORITHM COMPLEXITY")

    result.append("Merge Sort: O(n log n)")
    result.append("Insertion Sort: O(n^2)")
    result.append("0/1 Knapsack DP: O(n x W)")

    result.append("\n9. OBSERVATION")

    result.append(
        "Merge Sort efficiently arranges packages by delivery deadline."
    )

    result.append(
        "Insertion Sort prioritizes High, Medium and Low priority packages."
    )

    result.append(
        "Dynamic Programming selects the package combination "
        "with maximum total benefit within vehicle capacity."
    )

    result.append("\n" + "=" * 65)
    result.append("PHASE 2 COMPLETED SUCCESSFULLY")
    result.append("=" * 65)

    return "\n".join(result)


# ==========================================
# 7. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    try:

        report = generate_phase2_report()

        print(report)

        OUTPUT_DIR.mkdir(exist_ok=True)

        report_path = OUTPUT_DIR / "phase2_report.txt"

        with open(report_path, "w", encoding="utf-8") as file:
            file.write(report)

        print("\nPhase 2 report saved successfully!")
        print(f"File: {report_path}")

    except (FileNotFoundError, ValueError, KeyError) as error:

        print("\nERROR:", error)