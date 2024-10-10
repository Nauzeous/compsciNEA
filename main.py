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

        self.player = Player()
        self.clock = pygame.time.Clock()
        self.pmodel = pygame.image.load("battler.png").convert_alpha()
        self.speed = 5
        self.render_dist = 2
        self.view = pygame.Surface((self.render_dist*self.world.chunksize*2,self.render_dist*self.world.chunksize*2))
        

    def main(self):
        
        left, right, up, down = 0,0,0,0 # left right up down
        while True:
            for ev in pygame.event.get():    
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_a:
                        left = 1
                    elif ev.key == pygame.K_d: 
                        right = 1
                    elif ev.key == pygame.K_w:
                        up = 1
                    elif ev.key == pygame.K_s:
                        down = 1
                elif ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_a:
                        left = 0
                    elif ev.key == pygame.K_d:
                        right = 0
                    elif ev.key == pygame.K_w:
                        up = 0
                    elif ev.key == pygame.K_s:
                        down = 0

            accel = (right-left,down-up)

            self.player.pos.move(accel,self.speed, 1/60) 

            self.screen.fill((0,0,0))
            t1=time.perf_counter()
            self.render()
            #self.screen.blit(self.pmodel,(480,480))
            self.world.check_for_new_chunks(self.player.pos)
            t2=time.perf_counter()
            pygame.display.update()
            self.clock.tick(60)



    def render(self):

        intX = int(self.player.pos.x)
        intY = int(self.player.pos.y)

        fracX =self.player.pos.x-intX
        fracY = self.player.pos.y-intY

        # take slice of array inside these boundaries
        visible_map = self.world.get_world_grid((intX,intY),self.render_dist)
        pygame.surfarray.blit_array(self.view,visible_map)
        scaled_view = pygame.transform.scale(self.view,(1040,1040)) # 20 pixels of padding on each side

        view_diameter = 500 # pixels on screen



        # use fractional part of number to produce an offset
        offsetX = -20-int(fracX*self.window_length/view_diameter)
        offsetY = -20-int(fracY*self.window_height/view_diameter)
        self.screen.blit(scaled_view,(offsetX,offsetY))


game = Game(1000,1000)

if __name__ == "__main__":
    game.main()

            



