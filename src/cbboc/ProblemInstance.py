class ProblemInstance(object):
    def __init__(self, file_obj):
        # Get the first line and extract integer values
        self.numGenes, self.maxEvalsPerInstance, self._K, self._M = list(map(int, file_obj.readline().split()))
        self._data = []
        for _ in range(self._M):
            pieces = file_obj.readline().split()
            epistasis = list(map(int, pieces[:self._K]))
            fitness = list(map(float, pieces[self._K:]))
            self._data.append((epistasis, fitness))
        assert self.invariant()
    
    # Accessors to make API identical to other languages
    def getNumGenes(self): return self.numGenes
    
    def getMaxEvalsPerInstance(self): return self.maxEvalsPerInstance
    
    def value(self, candidate):
        if len(candidate) != self.numGenes:
            raise ValueError("Candidate of length %{0} expected, \
                              found %{1}".format(self.numGenes, len(candidate)))
        total = 0
        for epistasis, fitness in self._data:
            fnTableIndex = 0
            for index in epistasis:
                fnTableIndex <<= 1
                fnTableIndex |= candidate[index]
            total += fitness[fnTableIndex]
        return total
    
    def __str__(self):
        result = "ProblemInstance(numGenes={0},maxEvalsPerInstance={1},numFunctions={2})"
        return result.format(self.numGenes, self.maxEvalsPerInstance, len(self._data))
    
    def _allValidSize(self):
        tableSize = 1 << self._K
        for epistasis, fitness in self._data:
            if len(epistasis) != self._K or len(fitness) != tableSize:
                return False
        return True
    
    def invariant(self):
        return (self.getNumGenes() > 0 and
                self.getMaxEvalsPerInstance() > 0 and
                self._K > 0 and
                len(self._data) == self._M and
                self._allValidSize())
    
if __name__ == "__main__":
    from os import path
    filename = path.join(path.pardir, "resources", "toy1.txt")
    with open(filename, "r") as f:
        prob = ProblemInstance(f)
    candidate = [True] * prob.getNumGenes()
    print(prob.value(candidate))
    print(prob)

    filename = path.join(path.pardir, "resources", "toy2.txt")
    with open(filename, "r") as f:
        prob = ProblemInstance(f)
    candidate = [True] * prob.getNumGenes()
    print(prob.value(candidate))
    print(prob)
