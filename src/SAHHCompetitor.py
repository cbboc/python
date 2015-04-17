'''
 Implementation of Simulated Annealing as descriped in this paper:
 @inproceedings{white:1984,
   address = {Port Chester, NY},
   author = {White, S. R.},
   booktitle = {Proceeedings of the IEEE International Conference on Computer Design (ICCD) '84},
   pages = {646--651},
   title = {Concepts of Scale in Simulated Annealing},
   year = {1984}
 }
'''
from cbboc import CBBOC2015
from cbboc.Competitor import Competitor
from cbboc import TrainingCategory
import random
import sys
import math

def randomBitString(length):
    '''
    Generate and return a random list of bools.
    '''
    generated = bin(random.getrandbits(length))[2:]  # String of bits
    leadingZeros = '0' * (length - len(generated)) + generated
    return [x == '1' for x in leadingZeros]


def WhiteTemperatureRangeForSA(fitnessTrajectory):
    minDifference = min(abs(lead-follow) for lead, follow in
                        zip(fitnessTrajectory[1:], fitnessTrajectory))
    mean = sum(fitnessTrajectory) / len(fitnessTrajectory)
    variance = sum((mean - element) ** 2 for element in fitnessTrajectory)
    variance /= float(len(fitnessTrajectory) - 1)
    return minDifference, math.sqrt(variance)

def fitnessTrajectoryOfRandomWalk(objectiveFn, numSteps):
    incumbent = randomBitString(objectiveFn.getNumGenes())
    result = []
    for _ in range(numSteps):
        flipping = random.randrange(len(incumbent))
        incumbent[flipping] = not incumbent[flipping]
        result.append(objectiveFn.value(incumbent))
    return result

def SAAccept(lastValue, currentValue, temperature):
    if (currentValue > lastValue):
        return True
    elif temperature == 0:
        return currentValue > lastValue
    else:
        diffDivT = (currentValue - lastValue) / temperature
        p = math.exp(diffDivT)
        return random.random() < p

class SAHHCompetitor(Competitor):
    def __init__(self):
        super(SAHHCompetitor, self).__init__(TrainingCategory.SHORT)
        self.saScheduleLowerBound = 0
        self.saScheduleUpperBound = sys.float_info.max
    
    def train(self, trainingSet, maxTimeInMilliseconds):
        evalsPerCase = trainingSet[0].getRemainingEvaluations() / len(trainingSet)
        tempuratures = []
        for instance in trainingSet:
            fitnessTrajectory = fitnessTrajectoryOfRandomWalk(instance, evalsPerCase)
            tempuratures.append(WhiteTemperatureRangeForSA(fitnessTrajectory))
        lower, upper = zip(*tempuratures)
        self.saScheduleLowerBound = sum(lower) / len(lower)
        self.saScheduleUpperBound = sum(upper) / len(upper)
    
    def test(self, testCase, maxTimeInMilliseconds):
        length = testCase.getNumGenes()
        incumbent = randomBitString(length)
        lastValue = testCase.value(incumbent)
        numEvaluations = testCase.getRemainingEvaluations()
        span = (self.saScheduleUpperBound - self.saScheduleLowerBound)
        for i in range(numEvaluations):
            flipping = random.randrange(length)
            incumbent[flipping] = not incumbent[flipping]
            value = testCase.value(incumbent)
            fraction_cooled = (1 - (i / float(numEvaluations-1)))
            temperature = fraction_cooled * span + self.saScheduleLowerBound
            if not SAAccept(lastValue, value, temperature):
                # revert the change
                incumbent[flipping] = not incumbent[flipping]
            else:
                lastValue = value


if __name__ == "__main__":
    # Create your competitor, and call "run"
    competitor = SAHHCompetitor()
    try:
        CBBOC2015.run(competitor)
    except IOError as e:
        print e
        print "Make sure you are calling this from the top level directory"
    
    