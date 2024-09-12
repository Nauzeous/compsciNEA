import random
class Gene:
    def __init__(self):
        self.genelength = 5
        self.genomelength = 12
        self.mutationrate = 0.1

    def create_gene(self):
        newgene = ""
        for i in range(self.genelength):
            newhex = str(hex(random.randint(0,15)))[2:4]
            newgene += newhex
        return newgene
    
    def create_genome(self):
        newgenome = []
        for i in range(self.genomelength):
            newgenome.append(self.create_gene())
        return newgenome
