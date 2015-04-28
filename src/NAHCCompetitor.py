from cbboc import CBBOC2015
from cbboc.Competitor import Competitor
from cbboc import TrainingCategory
import random


def make_improvement(solution, previous_fitness, objectiveFn):
    '''
    Given a solution and its fitness, test each 1 bit flip
    in a random order until an improvement is found. Returns
    the fitness of the new solution, or the original if no
    improvement was found
    '''
    options = list(range(len(solution)))
    random.shuffle(options)
    for index in options:
        # flip bit
        solution[index] = not solution[index]
        fitness = objectiveFn.value(solution)
        if fitness > previous_fitness:
            # exit when improvement found
            return fitness
        solution[index] = not solution[index]
    # no improvement found
    return fitness

def randomBitString(length):
    '''
    Generate and return a random list of bools.
    '''
    generated = bin(random.getrandbits(length))[2:]  # String of bits
    leadingZeros = '0' * (length - len(generated)) + generated
    return [x == '1' for x in leadingZeros]


class NAHCCompetitor(Competitor):
    '''
    Implements the competition interface for performing training and testing
    '''
    def __init__(self):
        super(NAHCCompetitor, self).__init__(TrainingCategory.NONE)
        # Set up algorithm specific member variables here
    
    def train(self, trainingSet, maxTimeInMilliseconds):
        '''
        This is where training would be performed.
        '''
        raise NotImplementedError("Hill Climbers don't need training")
    
    def test(self, objectiveFn, maxTimeInMilliseconds):
        '''
        Apply your algorithm to the testing set of instances.
        '''
        while True:
            solution = randomBitString(objectiveFn.getNumGenes())
            new_fitness = objectiveFn.value(solution)
            # used to pass the first loop requirement
            fitness = new_fitness - 1
            while fitness < new_fitness:
                fitness = new_fitness
                new_fitness = make_improvement(solution, fitness, objectiveFn)


if __name__ == "__main__":
    # Create your competitor, and call "run"
    competitor = NAHCCompetitor()
    try:
        CBBOC2015.run(competitor)
    except IOError as e:
        print(e)
        print("Make sure you are calling this from the src directory")
