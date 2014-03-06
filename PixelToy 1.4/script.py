import math

buttonUp = loadImage('res/buttonUp.png')
buttonDown = loadImage('res/buttonDown.png')

G =  6.67428*math.pow(10,-11) #gravitational constant, unit: N(m/kg)^2 
time = 0
pause = False
maxdistance = 0
mindistance = 1000000000000000000000000
cameraX = _screenWidth/2
cameraY = _screenHeight/2

distanceScaleFactor = 1/280000000.0
#time unit: seconds
#mass unit: kilograms
#distance unit: meters

def drawImageRect(image,rect):
		drawImage(image,rect.x1+rect.width/2,rect.y1+rect.height/2,rect.width,rect.height)

def scaleMetersToPixels(distance):
	return distance*distanceScaleFactor

def gravity(body1Mass,body1Position,body2Mass,body2Position):
	global maxdistance, mindistance
	distance = Vector2D(body2Position.x-body1Position.x,body2Position.y-body1Position.y) # distance from self to body2
	if distance.power > maxdistance:
		maxdistance = distance.power
		print "MAX",maxdistance, bodies[0].position.x, bodies[0].position.y
	if distance.power < mindistance:
		mindistance = distance.power
		print "MIN",mindistance, bodies[0].position.x, bodies[0].position.y

	force = G*(body1Mass*body2Mass) / math.pow(distance.power,2) # indirectional force acting on both bodies
	force1 = Vector2D(distance.x/distance.power * force, distance.y/distance.power * force) # directional force acting on body1
	force2 = Vector2D(distance.x/distance.power *-force, distance.y/distance.power *-force) # directional force acting on body2 (opposite direction of force1)
	return force1,force2

def printScales():
	global time
	if distanceScaleFactor == 0:
		Dscale = str(0)
	else:
		Dscale = str(1/distanceScaleFactor)
	height = 17
	text0 = "scales:"
	text1 = "1 pixel = "+Dscale+" meters"
	text2 = "time(days): "+str(time)
	text3 = "Size is not to scale!!"
	useColour(0,0,0,255)
	drawString(_screenWidth-len(text1)*6-42,_screenHeight-height-6,text0)
	drawString(_screenWidth-len(text1)*12,_screenHeight-height*2-10,text1)
	drawString(_screenWidth-len(text1)*12,_screenHeight-height*3-10,text2)
	drawString(_screenWidth-len(text3)*12,_screenHeight-height*4-10,text3)

class Rect:
	def __init__(self,x,y,w,h):
		self.x1 = x
		self.y1 = y
		self.x2 = x+w
		self.y2 = y+h
		self.width = w
		self.height = h
	def rectCollide(self,rect2):
		if rect2.x1>self.x1 and rect2.x1<self.x2 and rect2.y1>self.y1 and rect2.y1<self.y2:
			return True
		if rect2.x2>self.x1 and rect2.x2<self.x2 and rect2.y1>self.y1 and rect2.y1<self.y2:
			return True
		if rect2.x1>self.x1 and rect2.x1<self.x2 and rect2.y2>self.y1 and rect2.y2<self.y2:
			return True
		if rect2.x2>self.x1 and rect2.x2<self.x2 and rect2.y2>self.y1 and rect2.y2<self.y2:
			return True
				
		if self.x1>rect2.x1 and self.x1<rect2.x2 and self.y1>rect2.y1 and self.y1<rect2.y2:
			return True
		if self.x2>rect2.x1 and self.x2<rect2.x2 and self.y1>rect2.y1 and self.y1<rect2.y2:
			return True
		if self.x1>rect2.x1 and self.x1<rect2.x2 and self.y2>rect2.y1 and self.y2<rect2.y2:
			return True
		if self.x2>rect2.x1 and self.x2<rect2.x2 and self.y2>rect2.y1 and self.y2<rect2.y2:
			return True
		return False

class Button:
	def __init__(self,x,y,width,text,returnValue):
		self.rect = Rect(x,y,width,35)
		self.text = text
		self.returnValue = returnValue
	def isUnderMouse(self):
		return self.rect.rectCollide(Rect(_mouseX,_mouseY,0,0)) #checking if mouse is over button
	def draw(self):
		useColour(0,0,0,255)
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
		self.acceleration = Vector2D(0.0,0.0)
		self.force = Vector2D(0.0,0.0)
		self.radius = radius
		self.trace = []
	def handleForce(self,force):
		self.force.x += force.x
		self.force.y += force.y
	def move(self): 		
		self.acceleration.x += self.force.x/self.mass
		self.acceleration.y += self.force.y/self.mass	
		self.velocity.x += self.acceleration.x*86400
		self.velocity.y += self.acceleration.y*86400
		self.position.x += self.velocity.x*86400
		self.position.y += self.velocity.y*86400
		self.acceleration = Vector2D(0.0,0.0)
		self.force = Vector2D(0.0,0.0)
	def draw(self):
		self.trace.append((self.position.x,self.position.y))
		if self.name == "Sun":
			useColour(255,0,0,255)
		else:
			useColour(0,0,255,255)
		drawCircle(scaleMetersToPixels(self.position.x)+cameraX,scaleMetersToPixels(self.position.y)+cameraY,scaleMetersToPixels(self.radius))
		drawString(scaleMetersToPixels(self.position.x)-len(self.name)*5+cameraX,scaleMetersToPixels(self.position.y)-scaleMetersToPixels(self.radius)-17+cameraY,self.name)
		for point in self.trace:
			drawPoint(scaleMetersToPixels(point[0])+cameraX,scaleMetersToPixels(point[1])+cameraY)
print math.sqrt(G*1.9891*math.pow(10,30)*(2.0/30550000000.0-1.0/30550000000.0)
bodies = [Body("Vega",0.0,30550000000,1.9891*math.pow(10,30),math.sqrt(G*1.9891*math.pow(10,30)*(2/30550000000-1/30550000000)),0.0,6955000000.0),Body("Capricorn",0.0,-30550000000,1.9891*math.pow(10,30),math.sqrt(G*1.9891*math.pow(10,30)*(2/30550000000-1/30550000000)),0.0,6955000000.0)]
# Body("Planet X",152098232000.0,0.0,5.97219*math.pow(10,24),0,40340,63781000.0),
#-math.sqrt(G*1.9891*math.pow(10,30)*(2/30550000000-1/28550000000))


for body in bodies:
	print body.name, body.position.x, body.position.y

while True:
	PREVIOUSscreenWidth = _screenWidth
	PREVIOUSscreenHeight = _screenHeight
	PREVIOUSisLeftMouseDown = isLeftMouseDown()
	newFrame()
	scroll = getMouseWheelDelta()
	if scroll >= 120:
		distanceScaleFactor *= 1.25
	if scroll <= -120:
		distanceScaleFactor *= 0.8

	if PREVIOUSscreenHeight != _screenHeight or PREVIOUSscreenWidth != _screenWidth:
		cameraX = _screenWidth/2
		cameraY = _screenHeight/2
		if pause:
			buttons = [Button(0,_screenHeight-35,150,'play','play')]
		else:
			buttons = [Button(0,_screenHeight-35,150,'pause','pause')]

	isCenterButton = 'not'
	isZoomButton = 'not'
	for i in range(len(buttons),0,-1):
		j = i-1
		if not isLeftMouseDown() and PREVIOUSisLeftMouseDown and buttons[j].isUnderMouse():
			if buttons[j].returnValue == 'center':
				cameraX = _screenWidth/2
				cameraY = _screenHeight/2
			if buttons[j].returnValue == 'unzoom':
				 distanceScaleFactor = 1/280000000.0
			if buttons[j].returnValue == 'pause':
				pause = True
				buttons.pop(j)
				buttons.append(Button(0,_screenHeight-35,150,'play','play'))
			elif buttons[j].returnValue == 'play':
				pause = False
				buttons.pop(j)
				buttons.append(Button(0,_screenHeight-35,150,'pause','pause'))
			
		if buttons[j].text == 'center':
			isCenterButton = j
		if buttons[j].text == 'reset zoom':
			isZoomButton = j		
		buttons[j].draw()

	if isCenterButton == 'not':
		if cameraX != _screenWidth/2 or cameraY != _screenHeight/2:
			buttons.append(Button(0,_screenHeight-35*(len(buttons)+1),150,'center','center'))
	elif cameraX == _screenWidth/2 and cameraY == _screenHeight/2:
		buttons.pop(isCenterButton)

	if isZoomButton == 'not':
		if distanceScaleFactor != 1/280000000.0:
			buttons.append(Button(0,_screenHeight-35*(len(buttons)+1),150,'reset zoom','unzoom'))
	elif distanceScaleFactor == 1/280000000.0:
		buttons.pop(isZoomButton)

	if not pause:
		time += 1
		i = 0
		for body1 in bodies[:-1]:
			i += 1
			for body2 in bodies[i:]:
				force1,force2 = gravity(body1.mass,body1.position,body2.mass,body2.position)
		
				body1.handleForce(force1)
				body2.handleForce(force2)
				if time % 50 == 0:
					print body1.name, body1.force.x, force1.x, body1.force.x + force1.x
					print body2.name, body2.force.x, force1.x, body2.force.x + force2.x
	
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
