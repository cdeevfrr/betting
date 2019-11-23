##
# The meta algorithm operates on 'population members'.
# To use the meta algorithm, define :
#    your own type of population member,
#    a function for scoring population members:
#        This can be a heuristic, nondeterministic score. It will be averaged over time.
#    a set of functions which can be used to create a population member from scratch,
#    a set of n-ary functions on population members to mutate population member(s)
#    a settings object of type {[key: string other than default setting] : number between -1 and 1}
#        This should be the first arg of each of the above functions.
#        If you want an integer setting or similar, please do your own converting
#            to and from the range -1 to 1. To determine settings for you, we need a
#            simple solution space.
#        DO NOT WRITE TO these settings within your functions:
#            'populationSize'
#            'numTopPerformersToKeep'
#            'maxIterations'
#            'timeoutSeconds'
#            'timeBetweenPrints'
#            'mutator'
#            
# Then, you can run parameterize(seconds to run) on those inputs, and it will spit out
#    a good population size, num to keep, mutator, and initializer to use to optimize for algorithms
#    run in that number of seconds.



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
