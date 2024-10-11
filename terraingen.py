import numpy as np, random, time, asyncio, multiprocessing
from numba import jit
from noise import pnoise2

@jit
def detail(x):
		return x * random.uniform(0.92,1)

def add_colour(world):
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
		self.chunksize = 50
		loading_range = 30
		self.offset = [loading_range // 2,loading_range // 2]
		self.loaded_chunks = np.array((loading_range*self.chunksize,loading_range*self.chunksize,3),dtype = np.uint8)
		self.seed = 8_002
		self.chunktasks = []
		asyncio.run(self.spawnbasechunks()) # start with 10x10 chunks


	def new_chunk(self,x,y) -> None:

		# x and y are the top left corner of the chunk, or the closest multiple of 100 below current x or y

		noise_grid = np.zeros((self.chunksize,self.chunksize),dtype = float)

		x_lcs = (x+self.centre[0])
		y_lcs = (y+self.centre[1])

		for i in range(self.chunksize):
			for j in range(self.chunksize):
				noise_grid[i,j]=pnoise2((i+x)/2000,(j+y)/2000,	
					octaves=6,
						persistence=0.5,lacunarity=2,base=self.seed)
		
		chunk = add_colour(noise_grid)
		self.loaded_chunks[x_lcs:x_lcs+self.chunksize,y_lcs:y_lcs+self.chunksize]=chunk

		
	async def create_chunk(self,x_cs,y_cs):
		chunk = await asyncio.to_thread(self.new_chunk,x_cs,y_cs)
		return chunk
	
	async def spawnbasechunks(self):
	    self.seed += 1
	    t1 = time.perf_counter()
	    for i in range(-5, 5):
	        for j in range(-5, 5):
	            self.chunktasks.append(self.create_chunk(i, j))
	    await asyncio.gather(*self.chunktasks)  # Use gather to run all tasks concurrently
	    t2 = time.perf_counter()
	    print(round(t2-t1, 2), "seconds to generate chunks")


	def check_for_new_chunks(self,position): # generate chunks in a 5x5 chunk range around the player if not generated

		curr_chunk_coord = (int(position.x/self.chunksize),int(position.y/self.chunksize))

		for i in range(-2,3):
			for j in range(-2,3):
				#realx+i*self.chunksize,y+j*self.chunksize]
				if self.chunks[curr_chunk_coord[0],curr_chunk_coord[1],0,0] == [0,0,0]:
					chunkX = int(coord[0]/100)
					chunkY = int(coord[1]/100)
					self.chunktasks.append(self.create_chunk(chunkX,chunkY))



	def get_world_grid(self,position:tuple,render_dist:int): # convert from world space into loaded world space
		
		lwsp = (int(position[0]+self.centre[0]),int(position[1]+self.centre[1]))

		visible_area = self.loaded_chunks[lwsp[0]-render_dist:lwsp[0]+render_dist,lwsp[1]-render_dist:lwsp[1]+render_dist]

		return visible_area