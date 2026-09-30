import random

classes = [
    ("Math", "F3", "G1"),
    ("Physics", "F2", "G2"),
    ("DSA", "F1", "G3"),
    ("DBMS", "F3", "G1"),
    ("OS", "F2", "G3"),
    ("AI", "F3", "G2"),
    ("COA", "F3", "G1"),
    ("web","F2", "G2"),
    ("OOP", "F2", "G1")
]

rooms = ["R1", "R2"]
slots = ["S1", "S2", "S3", "S4","S5"]

POP_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.05


def create_chromosome():
    return [(random.choice(slots), random.choice(rooms))
            for _ in classes]


def fitness(chromosome):
    clashes = 0

    for i in range(len(classes)):
        _, faculty1, group1 = classes[i]
        slot1, room1 = chromosome[i]

        for j in range(i + 1, len(classes)):
            _, faculty2, group2 = classes[j]
            slot2, room2 = chromosome[j]

            if slot1 == slot2:
                if faculty1 == faculty2:
                    clashes += 1
                if room1 == room2:
                    clashes += 1
                if group1 == group2:
                    clashes += 1

    return 1 / (1 + clashes)


def selection(population):
    a = random.choice(population)
    b = random.choice(population)
    return a if fitness(a) > fitness(b) else b


def crossover(p1, p2):
    point = random.randint(1, len(classes) - 1)
    return p1[:point] + p2[point:]


def mutation(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] = (
                random.choice(slots),
                random.choice(rooms)
            )
    return chromosome


population = [create_chromosome() for _ in range(POP_SIZE)]

for generation in range(GENERATIONS):

    new_population = []

    best = max(population, key=fitness)
    new_population.append(best)

    while len(new_population) < POP_SIZE:
        p1 = selection(population)
        p2 = selection(population)

        child = crossover(p1, p2)
        child = mutation(child)

        new_population.append(child)

    population = new_population

    best = max(population, key=fitness)

    if fitness(best) == 1:
        break


best = max(population, key=fitness)

print("CLASS TIMETABLE")
print("=" * 55)

for i, (subject, faculty, group) in enumerate(classes):
    slot, room = best[i]

    print(
        f"{subject:8} | Faculty: {faculty} | "
        f"Group: {group} | Slot: {slot} | Room: {room}"
    )

print("=" * 55)
print("Clashes :", int(1 / fitness(best) - 1))
print("Fitness :", fitness(best))
print("Generation:", generation + 1)
