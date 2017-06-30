#!/usr/bin/python

import sys
import copy
import numpy
import random

BEST_FITNESS = 28
MUTATION_PROBABILITY = 0.01
CROSSOVER_PROBABILITY = 0.3

class Individual:
    def __init__(self, chromosome_len):
        self.fitness = None
        self.chromosome_len = chromosome_len
        self.chromosome = numpy.arange(self.chromosome_len)
        numpy.random.shuffle(self.chromosome)

    def __str__(self):
        result = "\nsolution found!\nfitness: " + str(self.evaluate()) + '\n'
        for j in range(self.chromosome_len):
            for i in range(self.chromosome_len):
                if i == self.chromosome[j]:
                    result += "[Q]"
                else:
                    result += "[-]"
            result += '\n'
        return result

    def mutate(self):
        for i in range(self.chromosome_len):
            if random.random() < MUTATION_PROBABILITY:
                self.chromosome[i] = random.randint(0, self.chromosome_len)
        return self

    def evaluate(self):
        if not self.fitness:
            fitness = 0
            for i in range(0, self.chromosome_len - 1):
                for j in range(i + 1, self.chromosome_len):
                    if self.chromosome[i] == self.chromosome[j]:
                        fitness += 1
                    if abs(j - i) == abs(self.chromosome[j] - self.chromosome[i]):
                        fitness += 1
            self.fitness = BEST_FITNESS - fitness
        return self.fitness
    
def selection(population):
    result = []
    for i in range(2):
        leader = random.choice(population)
        for j in range(len(population)):
            challenger = random.choice(population)
            if leader.evaluate() < challenger.evaluate():
                leader = challenger
        result.append(leader);
    return result

def crossover(parents):
    result = copy.deepcopy(parents)
    if random.random() < CROSSOVER_PROBABILITY:
        i = random.randint(0, result[0].chromosome_len)
        j = random.randint(i, result[0].chromosome_len)
        for k in range(i, j):
            result[0].chromosome[k] = parents[1].chromosome[k]
            result[1].chromosome[k] = parents[0].chromosome[k]
    return result
        
def evolve(population):
    result = []
    while len(result) < len(population):
        parents = selection(population)
        children = crossover(parents)
        for child in children:
            result.append(child.mutate())
            if len(result) == len(population):
                break
    return result

if __name__ == '__main__':
    generations = 100
    chromosome_len = 8
    population_size = 1000
    population = [Individual(chromosome_len) for i in range(population_size)]
    for g in range(generations):
        population = evolve(population)
        solution = next((i for i in population if i.evaluate() == BEST_FITNESS), None)
        if solution != None:
            print(solution)
            sys.exit(1)

