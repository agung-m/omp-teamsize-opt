
import random
import array

import numpy

from deap import base
from deap import benchmarks
from deap import creator
from deap import tools
import trial

# Problem definition:
# Each individual consists of sizes of teams, whose the number of teams as the problem dimension.
# Objective function: execution time
# Use differential evolution (DE) to optimize the execution time using black-box approach.

# Problem dimension: number of teams
NDIM = trial.NUM_TEAMS

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

#toolbox.register("attr_float", random.uniform, -3, 3)
toolbox.register("attr_nthreads", random.randint, trial.NTHREADS_MIN, trial.NTHREADS_MAX)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_nthreads, NDIM)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("select", tools.selRandom, k=3)
toolbox.register("evaluate", trial.run)

# Consider constraints by applying penalties
toolbox.decorate("evaluate", tools.DeltaPenalty(trial.feasible, trial.INVALID_NTHREADS_PENALTY))

def main():
    # Differential evolution parameters
    # Crossover probability
    CR = 0.25
    # Differential weight
    F = 1
    # The number of individuals to select for the next generation
    MU = 300
    # The number of generation
    NGEN = 200

    pop = toolbox.population(n=MU);
    print(pop)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(pop), **record)
    print(logbook.stream)

    for g in range(1, NGEN):
        for k, agent in enumerate(pop):
            a, b, c = toolbox.select(pop)
            y = toolbox.clone(agent)
            index = random.randrange(NDIM)
            for i, value in enumerate(agent):
                if i == index or random.random() < CR:
                    y[i] = a[i] + F * (b[i] - c[i])

            #print("- Evaluate {}".format(y))
            y.fitness.values = toolbox.evaluate(y)
            if y.fitness > agent.fitness:
                pop[k] = y
        hof.update(pop)
        record = stats.compile(pop)
        logbook.record(gen=g, evals=len(pop), **record)
        print(logbook.stream)

    print("Best individual (params) is ", hof[0], hof[0].fitness.values[0])


if __name__ == "__main__":
    main()