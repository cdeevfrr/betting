import evaluator
import numpy

# See main.py for the shape of betInformationArray
def generateEvaluator(betInformationArray):
    return repeatUntilWithinTolerance(evaluator.evaluateBettingStrategy(betInformationArray))



def repeatUntilWithinTolerance(betEvaluator):
    def newEvaluator(betArray):
        results = []
        while(not certainWithinTolerance(results, 0.2)):
            results.append(betEvaluator(betArray))
        # This can be helpful if you're running into speed problems.
        # print("Evaluated to be close with " + str(len(results)) + " steps")
        return sum(results) / len(results)
    return newEvaluator

def certainWithinTolerance(results, tolerance):
    if(len(results) < 3):
        return False
    ## Standard error of mean = stdDeviation / sqrt(sampleSize)
    return numpy.std(results) / (len(results) ** .5) < tolerance
    
    


