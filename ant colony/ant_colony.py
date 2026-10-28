import numpy as np

D = np.array([
    [0,  2,  9, 10],
    [2,  0,  6,  4],
    [9,  6,  0,  3],
    [10, 4,  3,  0]
], dtype=float)

n = len(D)
alpha, beta = 1, 2
rho, Q = 0.5, 100
ants, iterations = 10, 50

np.random.seed(42)

tau = np.ones((n, n))
eta = np.zeros_like(D)
eta[D > 0] = 1 / D[D > 0]

best_route = None
best_distance = float("inf")

for iteration in range(iterations):
    for _ in range(ants):
        route = [0]
        unvisited = set(range(1, n))

        while unvisited:
            current = route[-1]
            nodes = sorted(unvisited)

            weights = np.array([
                tau[current, j]**alpha * eta[current, j]**beta
                for j in nodes
            ])

            probabilities = weights / weights.sum()
            next_node = int(np.random.choice(
                nodes, p=probabilities
            ))

            route.append(next_node)
            unvisited.remove(next_node)

        route.append(0)

        distance = sum(
            D[route[i], route[i + 1]]
            for i in range(len(route) - 1)
        )

        if distance < best_distance:
            best_distance = distance
            best_route = route.copy()

    tau *= (1 - rho)

    for i in range(len(best_route) - 1):
        a, b = best_route[i], best_route[i + 1]
        tau[a, b] += Q / best_distance
        tau[b, a] += Q / best_distance

print("WAREHOUSE ROUTE OPTIMIZATION")
print("-" * 35)
print("Starting point: Warehouse (0)")
print("Best route:", " -> ".join(map(str, best_route)))
print(f"Minimum distance: {best_distance:.2f} units")
print("Locations visited:", n)
print("Iterations:", iterations)