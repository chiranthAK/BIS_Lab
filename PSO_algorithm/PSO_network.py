import random
import networkx as nx
import matplotlib.pyplot as plt

edges = [
    ("A", "B", 2),
    ("A", "C", 4),
    ("B", "C", 1),
    ("B", "D", 3),
    ("B", "E", 7),
    ("C", "D", 6),
    ("C", "E", 5),
    ("D", "E", 2)
]

source = "A"
destination = "E"

graph = nx.Graph()

for u, v, cost in edges:
    graph.add_edge(u, v, cost=cost)

def fitness(path):
    if path[0] != source or path[-1] != destination:
        return float("inf")

    total = 0

    for i in range(len(path) - 1):
        total += graph[path[i]][path[i + 1]]["cost"]

    return total

def random_route():
    path = [source]
    visited = {source}

    while path[-1] != destination:

        neighbors = [
            node for node in graph.neighbors(path[-1])
            if node not in visited
        ]

        if not neighbors:
            return nx.shortest_path(
                graph, source, destination
            )

        next_node = random.choice(neighbors)

        path.append(next_node)
        visited.add(next_node)

    return path

num_particles = 20
iterations = 50

c1 = 1.5 
c2 = 1.5 
mutation_rate = 0.25

particles = [
    random_route()
    for _ in range(num_particles)
]

pbest = [path[:] for path in particles]
pbest_cost = [fitness(path) for path in pbest]

best_index = pbest_cost.index(min(pbest_cost))

gbest = pbest[best_index][:]
gbest_cost = pbest_cost[best_index]

for iteration in range(iterations):

    for i in range(num_particles):

        current = particles[i]

        candidates = [
            current,
            pbest[i],
            gbest,
            random_route()
        ]

        scores = []

        for route in candidates:

            cost = fitness(route)

            cognitive = 0
            if route == pbest[i]:
                cognitive = c1 * random.random()

            social = 0
            if route == gbest:
                social = c2 * random.random()

            score = cost - cognitive - social

            scores.append((score, route))

        scores.sort(key=lambda x: x[0])

        particles[i] = scores[0][1][:]

        current_cost = fitness(particles[i])

        if current_cost < pbest_cost[i]:
            pbest[i] = particles[i][:]
            pbest_cost[i] = current_cost

        if current_cost < gbest_cost:
            gbest = particles[i][:]
            gbest_cost = current_cost

    if (iteration + 1) % 10 == 0:
        print(
            f"Iteration {iteration + 1}: "
            f"{' -> '.join(gbest)}, Cost = {gbest_cost}"
        )

print("\nFinal Result")
print("----------------")
print("Source :", source)
print("Destination :", destination)
print("Best Route :", " -> ".join(gbest))
print("Total Cost :", gbest_cost)

pos = {
    "A": (0, 1),
    "B": (1, 2),
    "C": (1, 0),
    "D": (2, 2),
    "E": (3, 1)
}

plt.figure(figsize=(9, 6))

nx.draw_networkx_nodes(
    graph,
    pos,
    node_color="lightblue",
    node_size=1000
)

nx.draw_networkx_labels(
    graph,
    pos,
    font_weight="bold"
)

nx.draw_networkx_edges(
    graph,
    pos,
    edge_color="gray",
    width=1.5
)

edge_labels = {
    (u, v): data["cost"]
    for u, v, data in graph.edges(data=True)
}

nx.draw_networkx_edge_labels(
    graph,
    pos,
    edge_labels=edge_labels
)

best_edges = [
    (gbest[i], gbest[i + 1])
    for i in range(len(gbest) - 1)
]

nx.draw_networkx_edges(
    graph,
    pos,
    edgelist=best_edges,
    edge_color="red",
    width=4
)

plt.title(
    f"PSO Network Routing\n"
    f"Best Route: {' -> '.join(gbest)} | Cost: {gbest_cost}"
)

plt.axis("off")
plt.show()