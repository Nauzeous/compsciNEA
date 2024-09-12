from genes import Gene
from grid import Grid
class Cell:
    def __init__(self,ID,row,column):
        self.ID = ID



class Creature(Cell):
    def __init__ (self, ID,row,column):
        super().__init__(ID,row,column)
        self.dna = Gene()
        self.genome = self.dna.create_genome()
        
    def print_genome(self):

        print(self.genome)

