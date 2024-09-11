import numpy as np, random, time
from numba import jit,cuda
from noise import pnoise2

@jit
def detail(x):
		return x * random.uniform(0.92,1)

def add_colour(world):
	t1 = time.perf_counter()
	shape = world.shape
	   
	blue = np.array([0, 0, 255]) 
	yellow = np.array([255, 210, 0])
	green = np.array([0, 200, 0])
	grey = np.array([128, 128, 128])
	white = np.array([255, 255, 255])

		# output array
	colour_world = np.zeros(shape+(3,), dtype=np.uint8)
	print(colour_world.shape)

		# masks are used for each condition
	colour_world[world >= 0.8] = white
	colour_world[(world >= 0.3) & (world < 0.8)] = grey
	colour_world[(world >= -0.03) & (world < 0.3)] = green
	colour_world[(world >= -0.04) & (world < -0.03)] = yellow
	colour_world[world<-0.04] = blue
	
	noisify = np.vectorize(detail)

	colour_world = noisify(colour_world)
	t2=time.perf_counter()
	print(round(t2-t1,2),"seconds to colour map")

	return colour_world
        

class World:
	def __init__(self):
		self.world = np.zeros((2500,2500,3),dtype=np.uint8)
		self.centre = [1250,1250]
		self.seed = random.randint(1,10_000)
		self.map(-1000,1000,-1000,1000)



	def map(self,minX,maxX,minY,maxY):
		scale = 1000
		octaves = 6
		persistence = 0.5
		lacunarity = 2.0
		noise = np.zeros((maxX-minX,maxY-minY),dtype = float)

		t1 = time.perf_counter()
		for i in range(minX,maxX):
			for j in range(minY,maxY):
				if self.world[i+self.centre[0],j+self.centre[1],0]==0:
					noise[i,j]=pnoise2(i/scale,j/scale,octaves=octaves,
									persistence=persistence,lacunarity=lacunarity,base=self.seed)

		

		t2 = time.perf_counter()
		print(round(t2-t1,2), "seconds to generate map")
		self.world[minX+self.centre[0]:maxX+self.centre[0],
		minY+self.centre[1]:maxY+self.centre[1]]=add_colour(noise)


	

