import random,pygame
from position import Position

class Player:
	def __init__(self):
		self.upgrade_tree = [0,0,0,0,0,0]
		self.pos = Position(50,50,50) 
		self.upgrade_points = 0
		self.xp = 0


