import math
class Position:
	def __init__(self,x,y, speedcap):
		self.x = x
		self.y = y
		self.Xvel = 0
		self.Yvel = 0
		self.speedcap = speedcap
		self.friction = 0.95

	def move(self,accel,speedcap, dt):
		xaccel, yaccel = accel
		self.Xvel += xaccel
		self.Yvel += yaccel

		curr_speed = math.sqrt(self.Xvel ** 2 + self.Yvel ** 2)
		if curr_speed > self.speedcap: 
			speed_modifier = self.speedcap / curr_speed # normalizes size of velocity vectors
			self.Xvel *= speed_modifier
			self.Yvel *= speed_modifier
		

		self.Xvel *= self.friction
		self.Yvel *= self.friction

		# multiply by change in time to ensure movement is framerate independent
		self.x += self.Xvel * dt
		self.y += self.Yvel * dt

