import random
from cells import Cell,Creature
import pygame
class Grid:
    def __init__(self, pgridsize, ppopulation,pixellength,pixelheight,pvisionradius):
        self.gridsize = pgridsize
        self.population = ppopulation
        self.length = pixellength
        self.height = pixelheight
        self.cell_size = self.height/self.gridsize
        self.cells = []
        self.foodcells = []
        self.offset = (self.length - self.height)/2
        self.visionradius = pvisionradius
 
    def gridclear(self):
        self.grid = [[0 for i in range(self.gridsize)]for j in range(self.gridsize)]
        self.cells = []
        self.foodcells = []
    

    def getinputs(self, cell):
        inputs = []
        for i in range(-self.visionradius,self.visionradius + 1):
            for j in range(-self.visionradius,self.visionradius + 1):
                newrow = []
                row = cell.row
                col = cell.column
                if i == j and i == 0:
                    continue
                if self.inrange(row + i, col + j):
                        if self.grid[row + i][col + j] in self.foodcells:
                            newrow.append(1)
                        else:
                            newrow.append(0)
                else:
                    newrow.append(0)
                inputs.append(newrow)
        return inputs




    def moveright(self,cellID):
        row = self.cells[cellID].row
        column = self.cells[cellID].column
        if self.inrange(row,column+1) and isinstance(self.grid[row][column+1],Creature) == False:
            if self.grid[row][column+1] != 0:
                self.cells[cellID].foodcount += 1
                self.foodcells.remove(self.grid[row][column+1])      
            self.grid[row][column+1] = self.grid[row][column]
            self.grid[row][column] = 0
            self.cells[cellID].cell_move(0,1)


    def moveleft(self, cellID):
        row = self.cells[cellID].row
        column = self.cells[cellID].column
        if self.inrange(row,column-1) and isinstance(self.grid[row][column-1],Creature) == False:
            if self.grid[row][column-1] != 0:
                self.cells[cellID].foodcount += 1
                self.foodcells.remove(self.grid[row][column-1])
            self.grid[row][column-1] = self.grid[row][column]
            self.grid[row][column] = 0
            self.cells[cellID].cell_move(0,-1)


    def moveup(self,cellID):
        row = self.cells[cellID].row
        column = self.cells[cellID].column
        if self.inrange(row-1,column) and isinstance(self.grid[row-1][column],Creature) == False:
            if self.grid[row-1][column] != 0:
                self.cells[cellID].foodcount += 1
                self.foodcells.remove(self.grid[row-1][column])          
            self.grid[row-1][column] = self.grid[row][column]
            self.grid[row][column] = 0
            self.cells[cellID].cell_move(-1,0)


    def movedown(self,cellID):
        row = self.cells[cellID].row
        column = self.cells[cellID].column
        if self.inrange(row+1,column) and isinstance(self.grid[row+1][column],Creature) == False:
            if self.grid[row+1][column] != 0:
                self.cells[cellID].foodcount += 1
                self.foodcells.remove(self.grid[row+1][column])
            self.grid[row+1][column] = self.grid[row][column]
            self.grid[row][column] = 0
            self.cells[cellID].cell_move(1,0)

    def moverandom(self, cellID):
        rando = random.randint(1,4)
        
        if rando == 1:
            self.moveright(cellID)
        elif rando == 2:
            self.moveleft(cellID)
        elif rando == 3:
            self.moveup(cellID)
        else:
            self.movedown(cellID)


    def validposition(self, row, column):
        try:
            if self.grid[row][column] == 0 and row >= 0 and row <= self.gridsize and column >= 0 and column <= self.gridsize:
                return True
            return False
        except:
            return False

    def inrange(self, row, column):
        if row >= 0 and row <= self.gridsize-1 and column >= 0 and column <= self.gridsize-1:
            return True
        return False

    def generate(self, setgenomes):
        remainingcells = self.population*2
        while remainingcells != 0:
            newrandomrow = random.randint(0,self.gridsize-1)
            newrandomcol = random.randint(0,self.gridsize-1)
            if self.validposition(newrandomrow,newrandomcol) == True:
                if remainingcells >= self.population:
                    if len(setgenomes) != 0:
                        cell = Creature(remainingcells,newrandomrow,newrandomcol, setgenomes[0], self.visionradius)
                        setgenomes.pop(0)
                    else:
                        cell = Creature(remainingcells,newrandomrow,newrandomcol, 0, self.visionradius)
                    self.cells.append(cell)
                else:
                    cell = Cell(remainingcells,newrandomrow,newrandomcol)
                    self.foodcells.append(cell)
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
        

    def draw_with_signal_grid(self, screen):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if isinstance(self.grid[i][j],Creature):
                    colour = (255,0,0)
                elif isinstance(self.grid[i][j],Cell):
                    colour = (0,255,0)
                else:
                    if self.signalgrid[i][j][0] > 3:
                        self.signalgrid[i][j][0] = 3
                    if self.signalgrid[i][j][1] > 3:
                        self.signalgrid[i][j][1] = 3
                    colour = (100+(25*self.signalgrid[i][j][0]),100+(25*self.signalgrid[i][j][1]),100)
                cell_rect = pygame.Rect(j*self.cell_size+((self.length - self.height)/2), i*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, colour , cell_rect)
        pygame.display.update()


    def draw(self, screen):
        screen.fill((100,100,100))
        for cell in self.cells:
            pygame.draw.circle(screen,(255,0,0), (cell.column*self.cell_size+self.cell_size/2+self.offset,cell.row*self.cell_size+self.cell_size/2),self.cell_size/2)
        for foodcell in self.foodcells:
            cell_rect = pygame.Rect(foodcell.column*self.cell_size+self.offset, foodcell.row*self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen,(0,255,0), cell_rect)