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
#            'totalConsidered'
#            
# Then, you can run parameterize(seconds to run) on those inputs, and it will spit out
#    a good population size, num to keep, mutator, and initializer to use to optimize for algorithms
#    run in that number of seconds.



import generic
from generateEvaluator import generateEvaluator
import random

def create_meta_initializer(extraSettings):
    def meta_initializer(meta_algorithmSettings):
        # To make a new parameter set, ignore the meta_algorithm settings and
        # just make a new standard parameter set plus all the extra settings.
        result = extraSettings.copy()
        result.update({
        'populationSize': 20,
        'numTopPerformersToKeep': 5,
        'maxIterations': 2000, # we want to take advantage of as many iterations as we can in our allowed time.
        })
        return result
    return meta_initializer

def meta_mutator(meta_algorithmSettings, parent):
    # To make a new parameter set, ignore the meta_algorithmSettings
    # and just mess with the solution.
    # We don't want to let it optimize by increasing timeoutSeconds or maxIterations.
    print(parent)

    result = {}
    for key in parent:
        if (key not in ('timeoutSeconds','maxIterations')):
            result[key] = max(round(parent[key] * random.random() * 2), 1)
        else:
            result[key] = parent[key]
    print("Created parameter set %s" % result)
    return result

def reEvaluate(pop, scorer, algorithmSettings, times):
    for i in range(times):
        for member in pop:
            member.addEvaluation(scorer(algorithmSettings, member.solution))

def create_meta_scorer(object_initializer, object_mutator, object_scorer, secondsToRun):
    # Make a function that scores parameter sets.
    def scoringFunction(meta_algorithmSettings, solution):
        # solution is an instance of object-level algorithmSettings.

        # Add the timeout to the solution
        newSettings = solution.copy()
        newSettings['timeoutSeconds'] = secondsToRun
        try:
            object_result = generic.runGeneticAlgorithm(
                object_initializer,
                object_mutator,
                object_scorer,
                newSettings,
                False # print status
                )
        except Exception as error:
            print("Issues running parameters %s" % solution)
            raise error

        # Re-evaluate the winning population to get a better sense of the
        # performance of this algorithm on the true underlying objective
        # function. This means that parameter sets will get higher scores
        # for having truly good solutions somewhere in the output population,
        # rather than for just having lucky solutions (or large pop sizes)
        reEvaluate(
            pop=object_result,
            scorer=object_scorer,
            algorithmSettings=newSettings,
            times=3)
        object_result = sorted(
            object_result,
            key= lambda member:
                member.score,
            reverse=True # high scores are better.
        ) 
        
        print("Scored one parameter set: %.5f" % object_result[0].score)
        return object_result[0].score
    return scoringFunction

def parameterize(
        initializer,
        mutator,
        scorer,
        secondsToRunSolutions,
        secondsToOptimize,
        extraSettings):
    
    return generic.runGeneticAlgorithm(
        create_meta_initializer(extraSettings),
        meta_mutator,
        create_meta_scorer(initializer, mutator, scorer, secondsToRunSolutions),
        {
            'populationSize':5,
            'numTopPerformersToKeep':2,
            'timeoutSeconds': secondsToOptimize
        },
        True # print status
    )

