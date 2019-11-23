import random
import time
import math
import json
from inspect import signature


class PopulationMember:
    # The type of solution will be given by the user.
    def __init__(self, solution):
        self.score = -2 ** 20 # We still want to be able to sort populations
        # with some unkonwn scores, mostly in cases where we timed out
        # evaluating things in the pop.
        self.evalCount = 0
        self.solution = solution

    # Returns true if this is the first score, false otherwise.
    def addEvaluation(self, newScore):
        if (self.evalCount) == 0:
            self.score = newScore
            self.evalCount = 1
            return True
        else:
            # Average your score with the previous score
            self.score = (self.score * self.evalCount + newScore) / (self.evalCount + 1)
            self.evalCount += 1
            return False

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
                        algorithmSettings={}, # If meta-optimizing, all allowed keys should be in this dict
                        printStatus=False
                        ):
     # Make the settings that will be used throughout
    settings = defaultAlgorithmSettings.copy()
    settings.update(algorithmSettings)
    # Stick mutator and totalConsidered into algorithmSettings
    # so we don't have to pass them through all these functions explicitly.
    settings['mutator'] = mutator
    settings['totalConsidered'] = 0

    startTime = time.time()
    population = [] # Array<PopulationMember>
    for i in range(settings['populationSize']):
        initialSolution = initializer(settings)
        population.append(PopulationMember(initialSolution))
    endInitTime = time.time()
    if(printStatus):
        print("Initialized population of %d members in %.5f seconds" % (len(population), endInitTime - startTime))

    result = evolve (population, scorer, settings, startTime, printStatus)
    endEvolveTime = time.time()
    
    if(printStatus):
        print(\
            "\n\nFinished run; Considered %d total solutions in %.5f seconds. Best member has score %.5f and was evaluated %d times."\
            % (settings['totalConsidered'], endEvolveTime - startTime, result[0].score, result[0].evalCount ))
        print("Best result: %s" % result[0].solution)
    
    return result[0:settings['numTopPerformersToKeep']]

def evolve(
        initialPopulation,
        scorer,
        algorithmSettings,
        startTime, # May stop the algorithm depending on what's in algorithmSettings
        printStatus=False
        ):
    population = initialPopulation

    printTimer = time.time()
    for j in range(algorithmSettings['maxIterations']):
        # Check if we've timed out.
        if (time.time() - startTime > algorithmSettings['timeoutSeconds']):
            break
        population = runIteration(population, scorer, algorithmSettings, startTime)
        currentTime = time.time()
        if currentTime - printTimer > algorithmSettings['timeBetweenPrints']:
            if(printStatus):
                print("Iteration %d, Current best: {score: %.5f, evalCount: %d, solution: %s}" %\
                   (j, population[0].score,population[0].evalCount,population[0].solution ))
            printTimer = currentTime
    return population
        
def runIteration(population, scorer, algorithmSettings, startTime):
    # Right now, I'm choosing to prune-then-mutate.
    # You could mutate-then-prune.
    # If you mess with the pop. size and numToKeep, these two choices can be made identical.
    
    for i in population:
        # there is room here to optimize - you might not need to re-evaluate things that have already been evaluated a lot.
        # However, this currently saves you from sticking to a bad solution that got a lucky break from the scorer.
        isNew = i.addEvaluation(scorer(algorithmSettings, i.solution))
        if (isNew):
            algorithmSettings['totalConsidered'] += 1
        # stop if we've timed out.
        # This keeps you from passing a timeout just because the population is large.
        if (time.time() - startTime > algorithmSettings['timeoutSeconds']):
            break
        
    sortedPop = sorted(
        population,
        key= lambda member:
            member.score,
        reverse=True # high scores are better.
        )
    newPop = [sortedPop[i] \
              for i in range(\
                  min(\
                      algorithmSettings['numTopPerformersToKeep'],\
                      algorithmSettings['populationSize']\
                  )\
              )\
    ]
    return refillPop(newPop, algorithmSettings)

def refillPop(smallPopulation, algorithmSettings):
    mutator = algorithmSettings['mutator']
    neededNewMembers = algorithmSettings['populationSize'] - len(smallPopulation)
    newMembers = [makeChild(smallPopulation, mutator, algorithmSettings) \
                  for i in range(neededNewMembers)]
    return smallPopulation + newMembers

def makeChild(population, mutator, algorithmSettings):
    parentPopulationMembers = [random.choice(population) for i in range(len(signature(mutator).parameters) - 1)]
    parentSolutions = map(lambda s: s.solution, parentPopulationMembers)
    return PopulationMember(mutator(algorithmSettings, *parentSolutions))
