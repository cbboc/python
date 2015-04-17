import time
import ProblemInstance

TRAINING, TESTING = 0, 1

trainingEndTime = -1
testingEndTime = -1

class EvaluationsExceededException(Exception):
    pass

class TimeExceededException(Exception):
    pass

class ObjectiveFN(object):
    def __init__(self, instance, timingMode, remainingEvaluations):
        self.instance = instance
        self.timingMode = timingMode
        self.remainingEvaluations = remainingEvaluations
        self.remainingEvaluationsAtBestValue = None
    
    def value(self, candidate):
        timeNow = time.time() * 1000
        if self.timingMode == TRAINING:
            if timeNow > trainingEndTime:
                raise TimeExceededException()
        elif self.timingMode == TESTING:
            if timeNow > testingEndTime:
                raise TimeExceededException()
        else:
            raise ValueError("Not in training or testing, but trying to get value.")
        if self.remainingEvaluations.value <= 0:
            raise EvaluationsExceededException()
        value = self.instance.value(candidate)
        self.remainingEvaluations.value -= 1

        if self.remainingEvaluationsAtBestValue is None or value > self.remainingEvaluationsAtBestValue[1]:
            self.remainingEvaluationsAtBestValue = (self.remainingEvaluations.value, value)
        
        return value
    
    # Accessors to match other languages
    def getRemainingEvaluationsAtBestValue(self):
        if self.remainingEvaluationsAtBestValue is None:
            return (-1, -1)
        else:
            return self.remainingEvaluationsAtBestValue
    def getNumGenes(self): return self.instance.getNumGenes()
    def getRemainingEvaluations(self): return self.remainingEvaluations.value
    def getMaxEvalsPerInstance(self): return self.instance.getMaxEvalsPerInstance()
    
    def __str__(self):
        result = "ObjectiveFn(numGenes:{0},remainingEvaluations:{1}"
        result += ",remainingEvaluationsAtBestValue:{2},bestValue{3},timingMode:{4})"
        evals, best = self.getRemainingEvaluationsAtBestValue()
        result.format(self.getNumGenes(), self.remainingEvaluations, evals, best, self.timingMode)
