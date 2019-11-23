
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



import random
import time
import math
from inspect import signature


class PopulationMember:
    # The type of solution will be given by the user.
    def __init__(self, solution):
        self.score = 'unknown'
        self.evalCount = 0
        self.solution = solution
        
    def addEvalution(self, newScore):
        if (self.score) == 'unknown':
            global totalConsidered
            totalConsidered += 1
            self.score = newScore
            self.evalCount = 1
        else:
            # Average your score with the previous score
            self.score = (self.score * evalCount + newScore) / (self.evalCount + 1)
            self.evalCount += 1

defaultAlgorithmSettings = {
    'populationSize': 20,
    'numTopPerformersToKeep': 5,
    'maxIterations': 200,
    'timeoutSeconds': 60*2, 
    'timeBetweenPrints': 5
    }

def runGeneticAlgorithm(initializer,# type (algoSettings) => solution
                        mutator, # type (algoSettings, solution, solution...) => solution
                        scorer, #type: (algoSettings, solution) => number
                        algorithmSettings={}# If meta-optimizing, all allowed keys should be in this dict
                        ):
    # Keep track of how many solutions have been checked.
    global totalConsidered
    totalConsidered = 0

    # Make the settings that will be used throughout
    defaultAlgorithmSettings.update(algorithmSettings)
    settings = defaultAlgorithmSettings.copy()
    # Stick mutator into algorithmSettings so we don't have to pass it through all these functions explicitly.
    settings['mutator'] = mutator

    startTime = time.time()
    population = [] # Array<PopulationMember>
    for i in range(populationSize):
        initialSolution = initializer(settings)
        population.append(PopulationMember(initialSolution))
    endInitTime = time.time()
    print("Initialized population of %d members in %.5f seconds" % (len(population), endInitTime - startTime))

    result = evolve (population, scorer, algorithmSettings, startTime)
    endEvolveTime = time.time()
    print ("Finished run; Considered %d total solutions in #.5f seconds. Best member has score %d and was evaluated %d times."\
           % (totalConsidered, endEvolveTime - startTime, result[0].score, result[0].evalCount ))
    return result[0:settings['numTopPerformersToKeep']]

def evolve(
        initialPopulation,
        scorer,
        algorithmSettings,
        startTime # May stop the algorithm depending on what's in algorithmSettings
        ):
    population = initialPopulation

    printTimer = time.time()
    for j in range(algorithmSettings['maxIterations']):
        if (time.time() - startTime > algorithmSettings['timeoutSeconds']):
            break
        population = runIteration(population, scorer, algorithmSettings)
        currentTime = time.time()
        if currentTime - printTimer > algorithmSettings['timeBetweenPrints']:
            print("Iteration #d, Current best: {score: %.4f evalCount: %d" %\
                  (j, population[0].score, population[0].evalCount))
            printTimer = currentTime
    return population
        
def runIteration(population, scorer, algorithmSettings):
    # Right now, I'm choosing to prune-then-mutate.
    # You could mutate-then-prune.
    # If you mess with the pop. size and numToKeep, these two choices can be made identical.
    
    for i in population:
        # there is room here to optimize - you might not need to re-evaluate things that have already been evaluated a lot.
        # However, this currently saves you from sticking to a bad solution that got a lucky break from the scorer.
        i.addEvaluation(scorer(i.solution))
        
    sortedPop = sorted(
        population,
        key= lambda member:
            member.score,
        reverse=True # high scores are better.
        )
    newPop = [sortedPop[i] for i in range(algorithmSettings['numTopPerformersToKeep'])]
    return refillPop(newPop, algorithmSettings)

def refillPop(smallPopulation, algorithmSettings):
    mutator = algorithmSettings['mutator']
    neededNewMembers = algorithmSettings['populationSize'] - len(smallPopulation)
    newMembers = [makeChild(smallPopulation, mutator) for i in range(neededNewMembers)]
    return smallPopulation + newMembers

def makeChild(population, mutator):
    parents = [random.choice(population) for i in range(len(signature(mutator).parameters) - 1)]
    return PopulationMember(mutator(algorithmSettings, *parents))
