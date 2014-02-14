G =  

time = 0
class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def pointAdd(self,point2):
		self.x += point2.x
		self.y += point2.y
class Object:
	def __init__(self,x,y,mass,vX,vY,radius):
		self.position = Point(x,y)
		self.mass = mass
		self.velocity = Point(vX,vY)
		self.acceleration = Point(0,0)
		self.radius = radius
	def handleForce(self,force):
		self.acceleration.pointAdd(Point(force.x/self.mass,force.y/self.mass))
	def gravitySelfAndObject(self,objectMass,objectPosition):
		
	def move(self):
		self.velocity.pointAdd(self.acceleration)
		self.position.pointAdd(self.velocity)
		self.acceleration.x = 0
		self.acceleration.y = 0
	def draw(self):
		drawCircle(self.position.x,self.position.y,self.radius)


while True:
	newFrame()


