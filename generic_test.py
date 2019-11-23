import generic
from generateEvaluator import generateEvaluator
import random




algorithmSettings = {
    'mutationNerfConstant': 1,
    'populationSize': 150,
    'numTopPerformersToKeep': 1,
    'numIterations': 2000,
    'timeBetweenPrints': 1,
    'timeoutSeconds': 1
}

def initializer(algorithmSettings):
    return [0.1 for i in range(5)]

def mutator(algorithmSettings, parent):
    return [\
        i + (random.random() - .5) \
        / \
        algorithmSettings['mutationNerfConstant'] \
    for i in parent]

solutionScorer = generateEvaluator('')
scorer = lambda settings, solution: solutionScorer(solution)

generic.runGeneticAlgorithm(
    initializer,
    mutator,
    scorer,
    algorithmSettings,
    True)

print("\n\n\n Finished first test, moving on....")
# TEST: Does not throw errors with minimal sizes
algorithmSettings.update({'populationSize': 2, 'numTopPerformersToKeep': 1})
generic.runGeneticAlgorithm(
    initializer,
    mutator,
    scorer,
    algorithmSettings,
    True)

algorithmSettings.update({'populationSize': 1})
generic.runGeneticAlgorithm(
    initializer,
    mutator,
    scorer,
    algorithmSettings,
    True)

# TEST: Does not throw errors with strange settings
algorithmSettings.update({'populationSize': 1, 'numTopPerformersToKeep': 3})
generic.runGeneticAlgorithm(
    initializer,
    mutator,
    scorer,
    algorithmSettings,
    True)

