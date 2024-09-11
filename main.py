import time, numpy as np, pygame, sys,random
from player import Player
from terraingen import World

class Game:
    def __init__(self,wlength,wheight):
        pygame.init()
        self.world = World()
        self.window_length = wlength
        self.window_height = wheight
        self.screen = pygame.display.set_mode((wlength,wheight))
        self.worldseed = random.randint(1,20000)

        self.centre = [1000,1000] 
        self.player = Player()
        self.clock = pygame.time.Clock()
        self.pmodel = pygame.image.load("battler.png").convert_alpha()
        self.speed = 5
        self.view_diameter = 100
        
        self.view = pygame.Surface((self.view_diameter+2,self.view_diameter+2))
        

    def main(self):
        
        action = [0,0,0,0] # left right up down
        while True:
            for ev in pygame.event.get():    
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN:
                    k = ev.key
                    if k == pygame.K_a:
                        action[0] = 1
                    elif k == pygame.K_d:
                        action[1] = 1
                    elif k == pygame.K_w:
                        action[2] = 1
                    elif k == pygame.K_s:
                        action[3] = 1
                elif ev.type == pygame.KEYUP:
                    k = ev.key
                    if k == pygame.K_a:
                        action[0] = 0
                    elif k == pygame.K_d:
                        action[1] = 0
                    elif k == pygame.K_w:
                        action[2] = 0
                    elif k == pygame.K_s:
                        action[3] = 0
            accel = (action[1]-action[0],action[3]-action[2])

            self.player.pos.move(accel,self.speed, 1/60)

            self.screen.fill((0,0,0))
            t1=time.perf_counter()
            self.render()
            self.screen.blit(self.pmodel,(480,480))
            t2=time.perf_counter()
            pygame.display.update()
            self.clock.tick(60)



    def render(self):

        view_radius = self.view_diameter//2 + 1

        fracX,intX = np.modf(self.player.pos.x)
        fracY,intY = np.modf(self.player.pos.y)

        # initialise range of values viewable by player
        minX = int(intX-view_radius + self.world.centre[0])
        maxX = int(intX+view_radius + self.world.centre[0])
        minY = int(intY-view_radius + self.world.centre[1])
        maxY = int(intY+view_radius + self.world.centre[1])

        # take slice of array inside these boundaries
        visible_map = self.world.world[minX:maxX, minY:maxY]
        pygame.surfarray.blit_array(self.view,visible_map)
        scaled_view = pygame.transform.scale(self.view,(1050,1050)) # 5 pixels of padding on each side



        # use fractional part of number to produce an offset
        offsetX = -int(fracX*self.window_length/self.view_diameter)
        offsetY = -int(fracY*self.window_height/self.view_diameter)
        print(offsetX)

        self.screen.blit(scaled_view,(offsetX,offsetY))


game = Game(1000,1000)

if __name__ == "__main__":
    game.main()

            



