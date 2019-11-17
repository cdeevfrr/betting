
##
# Currently supported bet information array:
# [
#   {
#       betWinChance: number
#       maxBetSize: number
#   }
# ]
#
import random
from generateEvaluator import generateEvaluator

populationSize = 20
numTopPerformersToKeep = 5
numIterations = 30

def findBettingStrategy(betInformationArray):
    objectiveFunction = generateEvaluator(betInformationArray)
    population = []
    for i in range(populationSize):
        population.append(newBettingStrategy(betInformationArray))
    
    for j in range(numIterations):
        runIteration(population, objectiveFunction)
    return population[0]

        
def runIteration(population, objectiveFunction):
    scoredResults = [ {'betStrategy': i, 'score': objectiveFunction(i)} for i in population]
    sortedPop = sorted(scoredResults, key=lambda result: result['score'])
    print(sortedPop)
    newPop = [scoredResults[i]['betStrategy'] for i in range(numTopPerformersToKeep)]
    return refillPop(newPop)

def refillPop(smallPopulation):
    while (smallPopulation.length < populationSize):
        winner = pickRandomMember(smallPopulation)
        smallPopulation.append(mutate(winner))
    return smallPopulation

def mutate(bettingStrategy, nerfConstant = 5):
    return [i + random.random() / nerfConstant for i in bettingStrategy]

def newBettingStrategy(betInformationArray):
    return [1 for i in betInfromationArray]
