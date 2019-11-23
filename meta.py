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

def meta_initializer(meta_algorithmSettings):
    return {
    'populationSize': 20,
    'numTopPerformersToKeep': 5,
    'maxIterations': 2000,
    }
}

def meta_mutator(meta_algorithmSettings, parent):
    return [\
        key: round(parent[key] * random() * 2)
    for i in parent]

def meta_scorer(object_initialzier, object_mutator, object_scorer, secondsToRun):
    def scoringFunction(meta_algorithmSettings, solution):
        # solution is an instance of object-level algorithmSettings.

        # Add the timeout to the solution
        newSettings = solution.clone()
        newSettings.update('timeoutSeconds': secondsToRun)
        object_result = generic.runGeneticAlgorithm(
            object_initializer,
            object_mutator,
            object_scorer,
            newSettings
            )
        # Should we instead average the top 3 members of the object population,
        # to lessen the impact of randomness?
        return object_result[0].score
    return scoringFunction

def parameterize(
        secondsToRun,
        mutator,
        initializer,
        scorer):
    return generic.runGeneticAlgorithm(
        meta_initializer,
        meta_mutator,
        meta_scorer(mutator, initializer, scorer, secondsToRun),
        {} # Use default meta_algorithmSettings
        )

