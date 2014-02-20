import math
G =  6.67428*math.pow(10,-11) #gravitational constant, unit: N(m/kg)^2 
time = 0

distanceScaleFactor = 1/300000000.0
#time unit: seconds
#mass unit: kilograms
#distance unit: meters
print G*((1.9891*math.pow(10,30)*5.97219 * math.pow(10,24))/ math.pow(149600000000,2))

def absoluteValue(number):
	if number<0:
		number *= -1
	return number

def scaleMetersToPixels(distance):
	return distance*distanceScaleFactor

def gravity(body1Mass,body1Position,body2Mass,body2Position):
	distance = Vector2D(body2Position.x-body1Position.x,body2Position.y-body1Position.y) # distance from self to body2
	force = G*(body1Mass*body2Mass) / math.pow(distance.power,2) # indirectional force acting on both bodies
	force1 = Vector2D(distance.x/distance.power * force, distance.y/distance.power * force) # directional force acting on body1
	force2 = Vector2D(distance.x/distance.power *-force, distance.y/distance.power *-force) # directional force acting on body2 (opposite direction of force1)
	return force1,force2

def printScales():

	height = 17
	text0 = "scales:"
	text1 = "1 pixel = "+str(1/distanceScaleFactor)+" meters"
	text2 = "1 second = 60 days"
	text3 = "Size is not to scale!!"
	useColour(0,0,0,255)
	drawString(_screenWidth-len(text1)*6-42,_screenHeight-height-6,text0)
	drawString(_screenWidth-len(text1)*12,_screenHeight-height*2-10,text1)
	drawString(_screenWidth-len(text1)*12,_screenHeight-height*3-10,text2)
	drawString(_screenWidth-len(text3)*12,_screenHeight-height*4-10,text3)

class Button:

	def __init__(self,x,y,width,text,returnValue):
		self.rect = Rect(x,y,width,35)
		self.text = text
		self.returnValue = returnValue
	def isUnderMouse(self):
		return self.rect.rectCollide(Rect(_mouseX,_mouseY,0,0)) #checking if mouse is over button
	def draw(self):
		useColourList(BLACK)
		if isLeftMouseDown() and self.isUnderMouse():						
			drawImageRect(buttonDown,self.rect)
			drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+11,self.text)
		else:
			drawImageRect(buttonUp,self.rect)
			drawString(self.rect.x1+self.rect.width/2-len(self.text)*6,self.rect.y1+13,self.text)

class Vector2D:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.power = math.hypot(x,y)
	def vectorAdd(self,vector2):
		self.x += vector2.x
		self.y += vector2.y
class Body:
	def __init__(self,name,x,y,mass,vX,vY,radius):
		self.name = name
		self.position = Vector2D(x,y)
		self.mass = mass
		self.velocity = Vector2D(vX,vY)
		self.acceleration = Vector2D(0,0)
		self.radius = radius
		self.trace = []
	def handleForce(self,force):
		self.acceleration.x += force.x/self.mass
		self.acceleration.y += force.y/self.mass	
	def move(self): 			
		self.velocity.x += self.acceleration.x
		self.velocity.y += self.acceleration.y
		self.position.x += self.velocity.x
		self.position.y += self.velocity.y		
	def draw(self):
		self.trace.append((scaleMetersToPixels(self.position.x),scaleMetersToPixels(self.position.y)))
		if self.name == "Sun":
			useColour(255,0,0,255)
		else:
			useColour(0,0,255,255)
		drawCircle(scaleMetersToPixels(self.position.x)+cameraX,scaleMetersToPixels(self.position.y)+cameraY,scaleMetersToPixels(self.radius))
		drawString(scaleMetersToPixels(self.position.x)-len(self.name)*5+cameraX,scaleMetersToPixels(self.position.y)-scaleMetersToPixels(self.radius)-17+cameraY,self.name)
		self.acceleration.x = 0
		self.acceleration.y = 0
		for point in self.trace:
			drawPoint(point[0]+cameraX,point[1]+cameraY)
		

bodies = [Body("Earth",149600000000,0,5.97219*math.pow(10,24),0,29951.7,63781000),Body("Sun",0,0,1.9891*math.pow(10,30),0,0,6955000000)]

for body in bodies:
	print body.name, body.position.x, body.position.y
while True:
	newFrame()
	cameraX = _screenWidth/2
	cameraY = _screenHeight/2
	
	i = 0
	for body1 in bodies[:-1]:
		i += 1
		for body2 in bodies[i:]:
			force1,force2 = gravity(body1.mass,body1.position,body2.mass,body2.position)
		
			body1.handleForce(force1)
			body2.handleForce(force2)

	for i in range(86400):
		for body in bodies:
			body.move()

	for body in bodies:
		body.draw()
	
	printScales()

	if isKeyDown('UP'):
		cameraY -= 10
	if isKeyDown('DOWN'):
		cameraY += 10
	if isKeyDown('LEFT'):
		cameraX += 10
	if isKeyDown('RIGHT'):
		cameraX -= 10
