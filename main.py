
##
# Currently supported bet information array:
# [
#   {
#       betWinChance: number
#       maxBetSize: number
#   }
# ]
#

#Population Member type:
# {
#    betStrategy: Array<number> the fraction to bet at each iteration
#    score: 'unknown' | number  the score that this bet strategy gets. Stored to reduce computation time.
# }
#
import random
from generateEvaluator import generateEvaluator
import time
import math

populationSize = 20
numTopPerformersToKeep = 5
numIterations = 200
totalConsidered = 0
mutationNerfConstant = 5

def findBettingStrategy(betInformationArray):
    global totalConsidered
    objectiveFunction = generateEvaluator(betInformationArray)
    population = [] # Array<PopulationMember>
    totalConsidered = 0
    for i in range(populationSize):
        totalConsidered += 1
        population.append(makePopulationMember(newBettingStrategy(betInformationArray)))
    # print(population)

    result = evolve (population, objectiveFunction)
    print ("Considered " + str(totalConsidered) + " betting strategies")
    return result[0:numTopPerformersToKeep]

def evolve(initialPopulation, objectiveFunction):
    population = initialPopulation
    timer = time.time()
    for j in range(numIterations):
        population = runIteration(population, objectiveFunction)
        currentTime = time.time()
        if currentTime - timer > 1:
            print("Iteration " + str(j) + " Current best: "+ str(population[0]))
            timer = currentTime
    return population
        
def runIteration(population, objectiveFunction):
    for i in population:
        ## This only re-computes scores for things that don't have scores yet.
        evaluatePopulationMember(i,objectiveFunction)
    sortedPop = sorted(\
        population, \
        key= lambda result: \
            result['score'],\
        reverse=True)
    # These can show you the progress as you mutate the population.
    # print(sortedPop)
    newPop = [sortedPop[i] for i in range(numTopPerformersToKeep)]
    return refillPop(newPop)

def refillPop(smallPopulation):
    global totalConsidered
    while (len(smallPopulation) < populationSize):
        totalConsidered += 1
        winner = random.choice(smallPopulation)
        smallPopulation.append(makePopulationMember(mutate(winner['betStrategy'])))
    return smallPopulation

def mutate(bettingStrategy):
    return [i + (random.random() - .5) / mutationNerfConstant for i in bettingStrategy]

def makePopulationMember(bettingArray):
    return {'betStrategy': bettingArray, 'score': 'unknown'}

# Statefully modifies the 'score' attribute of the population member.
# This can help keep us from re-evaluating already evaluated bet strategies.
def evaluatePopulationMember(popMember, objectiveFunction):
    if(popMember['score'] == 'unknown'):
        popMember['score'] = objectiveFunction(popMember['betStrategy'])
        popMember['evalCount'] = 1
    else:
        # Rescore the result, and add that to the running average
        popMember['score'] = \
                           (\
                               popMember['score'] * popMember['evalCount'] \
                               + objectiveFunction(popMember['betStrategy']) \
                            ) / (popMember['evalCount'] + 1)
        popMember['evalCount'] += 1
                           


def newBettingStrategy(betInformationArray):
    return [.5 for i in range(10)]
