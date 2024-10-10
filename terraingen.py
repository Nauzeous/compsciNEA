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
		self.centre = [25,25]
		self.chunksize = 50
		self.chunks = np.zeros((9,9,self.chunksize,self.chunksize,3),dtype = np.uint8) # chunkX, chunkY, chunksizeX
		self.seed = 8_002
		self.chunktasks = []
		asyncio.run(self.spawnbasechunks()) # start with 10x10 chunks




		
        

	def world_to_chunk_conv(world_x,world_y):
		return int(world_x/self.chunksize),int(world_y/self.chunksize)

	def chunk_to_chunkgrid_conv(chunk_x,chunk_y):
		return chunk_x

	def new_chunk(self,x,y) -> None:

		# x and y are the top left corner of the chunk, or the closest multiple of 100 below current x or y

		noise_grid = np.zeros((self.chunksize,self.chunksize),dtype = float)
		#convert from signed space to unsigned space
		uint_x = (x+self.centre[0])*self.chunksize
		uint_y = (y+self.centre[1])*self.chunksize

		for i in range(self.chunksize):
			for j in range(self.chunksize):
				noise_grid[i,j]=pnoise2((i+uint_x)/2000,(j+uint_y)/2000,	
					octaves=6,
						persistence=0.5,lacunarity=2,base=self.seed)
		
		chunk = add_colour(noise_grid)
		self.chunks[x+self.centre[0],y+self.centre[1]]=chunk

		
	async def create_chunk(self,x,y):
		chunk = await asyncio.to_thread(self.new_chunk,x,y)
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

		curr_chunk_coord = (int(position.x/self.chunksize)+self.centre[0],int(position.y/self.chunksize)+self.centre[1])

		for i in range(-2,3):
			for j in range(-2,3):
				#realx+i*self.chunksize,y+j*self.chunksize]
				if self.chunks[curr_chunk_coord[0],curr_chunk_coord[1],0,0] == [0,0,0]:
					chunkX = int(coord[0]/100)
					chunkY = int(coord[1]/100)
					self.chunktasks.append(self.create_chunk(chunkX,chunkY))

	def get_world_grid(self,position:tuple,render_dist:int): # convert from world space into chunk space, then chunk space into chunkgrid space
		
		# convert from world space to chunk space

		dimXY = (render_dist*2) * self.chunksize

		grid = np.zeros((dimXY,dimXY,3))

		player_chunk_x,player_chunk_y = int(position[0]/self.chunksize)+self.centre[0], int(position[1]/self.chunksize)+self.centre[1]

		print(position)

		for i in range(-render_dist,render_dist):
			for j in range(-render_dist,render_dist):
				gridX = (i + render_dist)*self.chunksize+position[0] % self.chunksize
				gridY = (j + render_dist)*self.chunksize+position[1] % self.chunksize
				rendered_chunk = self.chunks[player_chunk_x+i,player_chunk_y+j]
				print(gridX,gridY)
				grid[gridX:gridX+self.chunksize,gridY:gridY+self.chunksize]=rendered_chunk

		return grid