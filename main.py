
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
numIterations = 5
totalConsidered = 0

def findBettingStrategy(betInformationArray):
    global totalConsidered
    objectiveFunction = generateEvaluator(betInformationArray)
    population = []
    totalConsidered = 0
    for i in range(populationSize):
        totalConsidered += 1
        population.append(newBettingStrategy(betInformationArray))

    result = evolve (population, objectiveFunction)
    print ("Considered " + str(totalConsidered) + " betting strategies")
    return result

def evolve(initialPopulation, objectiveFunction):
    population = initialPopulation
    for j in range(numIterations):
        population = runIteration(population, objectiveFunction)
    return population[0]
        
def runIteration(population, objectiveFunction):
    scoredResults = [ {'betStrategy': i, 'score': objectiveFunction(i)} for i in population]
    sortedPop = sorted(scoredResults, key=lambda result: result['score'], reverse=True)
    # These can show you the progress as you mutate the population.
    # print(sortedPop)
    print("Current best: "+ str(sortedPop[0]))
    newPop = [sortedPop[i]['betStrategy'] for i in range(numTopPerformersToKeep)]
    return refillPop(newPop)

def refillPop(smallPopulation):
    global totalConsidered
    while (len(smallPopulation) < populationSize):
        totalConsidered += 1
        winner = random.choice(smallPopulation)
        smallPopulation.append(mutate(winner))
    return smallPopulation

def mutate(bettingStrategy, nerfConstant = 5):
    return [i + (random.random() - .5) / nerfConstant for i in bettingStrategy]

def newBettingStrategy(betInformationArray):
    return [.5 for i in range(10)]



