import meta
from generateEvaluator import generateEvaluator
import random





### Copied from meta_test.py, the level 0 layer.
algorithmSettings = {
    'populationSize': 20,
    'numTopPerformersToKeep': 5,
    'numIterations': 200,
    'timeBetweenPrints': 1
}

def initializer(algorithmSettings):
    return [0.8 for i in range(5)]

def mutator(algorithmSettings, parent):
    return [\
        i + (random.random() - .5) \
        / \
        algorithmSettings['mutationNerfConstant'] \
    for i in parent]

solutionScorer = generateEvaluator('')
scorer = lambda settings, solution: solutionScorer(solution)


# This runs the level 1 layer.
meta.parameterize(
    initializer,
    mutator,
    scorer,
    1, # how long to run each genetic algorithm
    60 , # how long to run the meta algorithm,
    metaAlgorithmSettings = {
        'populationSize':5,
        'numTopPerformersToKeep':2
        },
    extraSettings = {'mutationNerfConstant': 5}
)

# The level 2 layer should run the level 1 layer multiple times.


