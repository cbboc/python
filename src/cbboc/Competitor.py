class Competitor(object):
    def __init__(self, trainingCategory):
        self.trainingCategory = trainingCategory
    
    def getTrainingCategory(self): return self.trainingCategory
    
    def train(self, trainingSet, maxTimeInMilliseconds):
        ''' trainingSet is a list of ObjectiveFns '''
        raise NotImplementedError("You must implement the train function")
    
    def test(self, testCase, maxTimeInMilliseconds):
        ''' testCase is an ObjectiveFn '''
        raise NotImplementedError("You must implement the testfunction")