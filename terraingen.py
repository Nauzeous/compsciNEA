import numpy as np, random, time, asyncio
from numba import jit
from noise import pnoise2

@jit
def detail(x):
		return x * random.uniform(0.92,1)

async def add_colour(world):
	t1 = time.perf_counter()
	shape = world.shape

	   
	BLUE = np.array([0, 0, 255],dtype=np.uint8) 
	YELLOW = np.array([255, 210, 0],dtype=np.uint8)
	GREEN = np.array([0, 200, 0],dtype=np.uint8)
	GREY = np.array([128, 128, 128],dtype=np.uint8)
	WHITE = np.array([255, 255, 255],dtype=np.uint8)

		# output array
	colour_world = np.zeros(shape+(3,), dtype=np.uint8)

		# masks are used for each condition
	colour_world[world >= 0.8] = WHITE
	colour_world[(world >= 0.3) & (world < 0.8)] = GREY
	colour_world[(world >= -0.03) & (world < 0.3)] = GREEN
	colour_world[(world >= -0.04) & (world < -0.03)] = YELLOW
	colour_world[world<-0.04] = BLUE
	
	noisify = np.vectorize(detail)
	colour_world = noisify(colour_world)

	return colour_world


class World:
	def __init__(self):
		self.world = np.zeros((2500,2500,3),dtype=np.uint8)
		self.centre = [1250,1250]
		self.seed = random.randint(1,10_000)
		self.chunksize=100
		asyncio.run(self.spawnbasechunks()) # start with 10x10 chunks




		
        

	


	async def chunk(self,x,y) -> None:
		# x and y are the top left corner of the chunk, or the closest multiple of 100 below current x or y

		noise = np.zeros((self.chunksize,self.chunksize),dtype = float)
		#convert from signed space to unsigned space
		uint_x = x + self.centre[0]
		uint_y = y + self.centre[1]

		for i in range(self.chunksize):
			for j in range(self.chunksize):
				noise[i,j]=pnoise2((i+x)/1000,(j+y)/1000,octaves=6,
						persistence=0.5,lacunarity=2,base=self.seed)
		chunk = await add_colour(noise)
		self.world[uint_x:uint_x+self.chunksize,uint_y:uint_y+self.chunksize]=chunk
		
	
	async def spawnbasechunks(self):
		t1 = time.perf_counter()
		for i in range(-5,5):
			for j in range(-5,5):
				await self.chunk(i*100,j*100)
		t2 = time.perf_counter()
		print(round(t2-t1,2),"seconds to generate chunks")


