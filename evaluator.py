import numpy

def evaluateBettingStrategy(betFractionArray):
    return sameBetEverywhere([2,1], rewardPercentages=[.5,-.5])


# winOdds: [number]
#    ex: [1:5:4] could mean you have a 10% chance of scenario1,
#    50% chance of scenario 2, and 40% chance of scenario 3.
# rewardPercentages: [number]
#    your total bet is multiplied by this and returned to you.
#    Must be the same length as winOdds.
#    [1, -.1, -.5] could be reward percentages for 10% chance of doubling,
#    50% chance of loosing 10%, and 40% chance of loosing 50%.
# 
def sameBetEverywhere(winOdds, rewardPercentages):
    def result(betArray):
        totalReward = 1
        for betPercentage in betArray:
            betPercentage = max(min(betPercentage, 1),0) ##restrict bets to be between 0 and 1
            totalReward += totalReward * betPercentage * numpy.random.choice(rewardPercentages, p=normalize(winOdds))
        return totalReward
    return result


def normalize(odds):
    x = sum(odds)
    return [i / x for i in odds]



                            
        
