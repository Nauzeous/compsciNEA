import random
from cells import Cell,Creature
import pygame
class Grid:
    def __init__(self, pgridsize, ppopulation,pixellength,pixelheight):
        self.gridsize = pgridsize
        self.population = ppopulation
        self.length = pixellength
        self.height = pixelheight
        self.cell_size = self.height/self.gridsize
        self.cells = []

    
    def gridclear(self):
        self.grid = [[0 for i in range(self.gridsize)]for j in range(self.gridsize)]
    
    def printgrid(self):
        for i in range(self.gridsize):
            print(self.grid[i])

    def moveright(self,row,column):
        if self.validposition(row,column+1):
            self.grid[row][column+1] = self.grid[row][column]
            self.grid[row][column] = 0
    
    def moveleft(self,row,column):
        if self.validposition(row,column-1):
            self.grid[row][column-1] = self.grid[row][column]
            self.grid[row][column] = 0
    
    def moveup(self,row,column):
        if self.validposition(row-1,column):
            self.grid[row-1][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def movedown(self,row,column):
        if self.validposition(row+1,column):
            self.grid[row+1][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def gridmoveup(self,row,column):
        if self.validposition(row-1,column):
            self.grid[row-1][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def gridmoveleft(self,row,column):
        if self.validposition(row,column-1):
            self.grid[row][column-1] = self.grid[row][column]
            self.grid[row][column] = 0
    

    def gridmoveright(self,row,column):
        if self.validposition(row,column+1):
            self.grid[row][column+1] = self.grid[row][column]
            self.grid[row][column] = 0
    


    def validposition(self, x, y):
        if self.grid[x][y] == 0:
            return True
        return False
        

    def generate(self):
        remainingcells = self.population*2
        while remainingcells != 0:
            newrandomrow = random.randint(0,self.gridsize-1)
            newrandomcol = random.randint(0,self.gridsize-1)
            if self.validposition(newrandomrow,newrandomcol) == True:
                if remainingcells >= self.population:
                    cell = Creature((self.population-remainingcells),newrandomrow,newrandomcol)
                    self.cells.append(cell)
                else:
                    cell = Cell(remainingcells,newrandomrow,newrandomcol)
                self.grid[newrandomrow][newrandomcol] = cell

                remainingcells = remainingcells -1




                



    def getcreature(self):
        for row in range(self.gridsize):
            for column in range(self.gridsize):
                if isinstance(self.grid[row][column],Creature):
                    return (row,column)
                
    def addcreature(self,column,row):
        newcell = Creature(200,column,row)
        self.grid[row][column] = newcell
        


    def draw(self, screen):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if isinstance(self.grid[i][j],Cell) == True:
                    cell_value = (self.grid[i][j]).ID
                else:
                    cell_value = 0
                colour1 = (100,100,100)
                if cell_value > self.population:
                    colour1 = (255,50,50)
                elif cell_value >=1:
                    colour1 = (50,255,50)
            
                cell_rect = pygame.Rect(j*self.cell_size+((self.length - self.height)/2), i*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, colour1 , cell_rect)

            
        

