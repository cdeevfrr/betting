import generic
from generateEvaluator import generateEvaluator
import random




algorithmSettings = {
    'mutationNerfConstant': 5,
    'populationSize': 20,
    'numTopPerformersToKeep': 5,
    'numIterations': 200,
    'timeBetweenPrints': 1
}

def initializer(algorithmSettings):
    return [0.5 for i in range(5)]

def mutator(algorithmSettings, parent):
    return [\
        i + (random.random() - .5) \
        / \
        algorithmSettings['mutationNerfConstant'] \
    for i in parent]

scorer = generateEvaluator('')

generic.runGeneticAlgorithm(
    initializer,
    mutator,
    scorer,
    algorithmSettings)
