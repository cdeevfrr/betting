
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

    return evolve (population, objectiveFunction)

def evolve(initialPopulation, objectiveFunction):
    population = initialPopulation
    for j in range(numIterations):
        population = runIteration(population, objectiveFunction)
    return population[0]
        
def runIteration(population, objectiveFunction):
    scoredResults = [ {'betStrategy': i, 'score': objectiveFunction(i)} for i in population]
    sortedPop = sorted(scoredResults, key=lambda result: result['score'], reverse=True)
    print("Current best: " + str(sortedPop[0]))
    newPop = [sortedPop[i]['betStrategy'] for i in range(numTopPerformersToKeep)]
    return refillPop(newPop)

def refillPop(smallPopulation):
    while (len(smallPopulation) < populationSize):
        winner = random.choice(smallPopulation)
        smallPopulation.append(mutate(winner))
    return smallPopulation

def mutate(bettingStrategy, nerfConstant = 5):
    return [i + (random.random() - .5) / nerfConstant for i in bettingStrategy]


