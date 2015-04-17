from ObjectiveFn import ObjectiveFN, TRAINING, TESTING
from ProblemInstance import ProblemInstance
import TrainingCategory
from os import path
from glob import glob
import TrainingCategory

class SharedPrimitive(object):
    ''' Wraps an immutable type to allow for shared read/write '''
    def __init__(self, value):
        self.value = value

def readInstances(file_obj):
    numInstances = int(file_obj.readline().strip())
    return [file_obj.readline().strip() for _ in range(numInstances)]

class ProblemClass(object):
    def __init__(self, base_path, trainingCategory):
        self.trainingCategory = trainingCategory
        with open(path.join(base_path, "trainingFiles.txt"), "r") as f:
            trainingFiles = readInstances(f)

        trainingInstances = []
        for filename in trainingFiles:
            with open(path.join(base_path, filename), "r") as f:
                trainingInstances.append(ProblemInstance(f))
        if trainingCategory is TrainingCategory.NONE:
            self.training = []
        else:
            totalTraining = sum(instance.getMaxEvalsPerInstance()
                                for instance in trainingInstances)
            sharedTrainingEvaluations = SharedPrimitive(totalTraining * trainingCategory)
            self.training = [ObjectiveFN(p, TRAINING, sharedTrainingEvaluations)
                             for p in trainingInstances]

        with open(path.join(base_path, "testingFiles.txt"), "r") as f:
            testingFiles = readInstances(f)
        self.testing = []
        for filename in testingFiles:
            with open(path.join(base_path, filename), "r") as f:
                p = ProblemInstance(f)
            separateTestingEvaluations = SharedPrimitive(p.getMaxEvalsPerInstance())
            self.testing.append(ObjectiveFN(p, TESTING, separateTestingEvaluations))
    
    # Accessors to match other language APIs
    def getTrainingCategory(self): return self.trainingCategory
    def getTrainingInstances(self): return self.training
    def getTestingInstances(self): return self.testing

if __name__ == "__main__":
    base_name = path.join("resources", "test", "toy")
    pc = ProblemClass(base_name, TrainingCategory.LONG)
    print len(pc.getTrainingInstances()), len(pc.getTestingInstances())