import pygame
import sys

pygame.init()


# Game Constants
SCREENX = 500
SCREENY = 500
SCREEN = pygame.display.set_mode((SCREENX, SCREENY))
pygame.display.set_caption('Breadth-First-Search Path-Finding Algorithm')

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

CLOCK = pygame.time.Clock()
FPS = 30
DELAY = 300

# Refers to the number of boxes on screen gridx x gridy e.g 5x5 = 25
GRIDX = 10
GRIDY = 10

obstacleObjects = {} # Store the obstacle objects (Blocks on the path) from Obstacle class
gridObjects = {}  # Store grid-box objects from Grid Class
gridObstacle = {} # Store the grid:obstacle pair stuck together ^_*
boxObjects = {}   # Store box objects from Box class :> filled boxes :> Actually start & goal Nodes
boxes = 1
obstacles = 1

# BFS Variables
startNode = 0
goalNode = 0
graph = dict()
pathFound = [] # Store the path in a list :> box index to draw on later


class BFS:
	''' This is the main class in this program. Finds a suitable path from point A to point B
		using Breadth-First-Search Algorithm'''
	def __init__(self, graph, start, goal):
		self.graph = graph
		self.start = start
		self.goal = goal

	def solve(self):
		print('Abracadara!\n\n')
		print(self.graph)
		print('\n\n')
		# keep track of explored nodes
		explored = []

		# keep track of all paths to be checked
		queue = [[self.start]]

		# return path if start is goal
		if self.start == self.goal:
			return 'That was easy. Start == Goal'

		# keep looping until all possible paths are explored
		while queue:
			# pop the first path from the queue
			path = queue.pop(0)
			# get the last node from the path
			node = path[-1]

			if node not in explored:
				neighbors = self.graph[node]
				# go through all neighbor nodes
				# push it into the queue
				for neighbor in neighbors:
					new_path = list(path)
					new_path.append(neighbor)
					queue.append(new_path)

					if neighbor == self.goal:
						return new_path

				# mark node as explored
				explored.append(node)

		# in case there is no path
		return "path not accessible"


class Grid(object):
	''' This class draws the grid on the screen by rendering equally sized boxes on the screen'''
	def __init__(self,x,y,sx,sy):
		self.x = x
		self.y = y
		self.sx = sx
		self.sy = sy
		self.width = 2

	def draw(self):
		pygame.draw.rect(SCREEN,BLACK,(self.x, self.y,self.sx, self.sy),self.width)


class Box(object):
	''' This class is used in filling up the grid-boxes rendered on-screen!
		Explicitly used on the Start and Goal nodes! :> Coz they are not obstacles! '''
	def __init__(self,x,y,sx,sy,color):
		self.x = x
		self.y = y
		self.sx = sx
		self.sy = sy
		self.color = color

	def draw(self):
		pygame.draw.rect(SCREEN, self.color, pygame.Rect(self.x, self.y, self.sx, self.sy))


class Obstacle(object):
	''' This class fills in the grid box with a black color indicating an Obstacle'''
	def __init__(self, mouseObj):
		self.mseX = mouseObj[0]
		self.mseY = mouseObj[1]

		for grid in gridObjects:
			g = getGridBoxes(grid)
			self.x = g.x
			self.y = g.y
			self.sx = g.sx
			self.sy = g.sy
			if self.mseX > self.x and self.mseX < self.x + self.sx:
				if self.mseY > self.y and self.mseY < self.y + self.sy:
					self.posX = self.x
					self.posY = self.y
					self.gridBox = grid

	def draw(self):
		pygame.draw.rect(SCREEN, BLACK, pygame.Rect(self.posX, self.posY, self.sx, self.sy))


def getGridBoxes(grid_box):
	return gridObjects[grid_box]

def drawGrid(sizex,sizey):
	''' Given the number of boxes X and Y, draw equally-sized grid boxes guided by SCREEN Dimensions'''
	spaceX = SCREENX // sizex
	spaceY = SCREENY // sizey
	width = 2

	# Instantiate Grid objects and store them in a dict object
	counter = 1
	for i in range(sizex):
		for j in range(sizey):
			g = Grid(i*spaceX,j*spaceY,spaceX, spaceY)
			gridObjects[counter] = g # Store the grid-box object in a Dictionary
			counter += 1

def generateGraph(row,col):
	''' This function generates a graph based on the gridObjects instantiated! '''
	# sample_graph = {'A':['B','C','E'],
	# 		 'B':['A','D','E'],
	# 		 'C':['A','F','G'],
	# 		 'D':['B'],
	# 		 'E':['A','B','D'],
	# 		 'F':['C'],
	# 		 'G':['C']
	# }

	miniG = {}
	for grid in range(len(gridObjects)):
		grid += 1 # Synchronize the index!
		mod = grid % col # Used to check the Top and Bottom Grid Boxes! :> Ingenious Idea!!! ^_^
		gN = grid - 1
		gS = grid + 1
		gE = grid + col		
		gW = grid - col

		# CHECK THE NEIGHBORS TO THE GRID-BOXES, ACCOUNTING FOR THE EXTREME GRID-BOXES(BORDERS)
		if mod == 0: # 5,10,15,20,25 :> You can't go south from here ! (Bottom Boxes)
			if grid > col: # Away from the Left Border of the Screen
				if grid > (col*row)-col: # You are on the Right Border of the screen :> You can't go East!
					miniG[grid] = [gN, gW]
				else: # Away from the Right Border of the Screen :> To the East you Go!
					miniG[grid] = [gN, gE, gW]
			else: # You are on the Left Edge of the screen :> You can't go West!
				miniG[grid] = [gN, gE]

		elif mod == 1: # 6,11,16,21 :> You can't go North from here ! (Top Boxes)
			if grid > col: # Away from the Left Border of the Screen
				if grid > (col*row)-col: # You are on the Right Border of the screen :> You can't go East!
					miniG[grid] = [gS, gW]
				else: # Away from the Right Border of the Screen :> To the East you Go!
					miniG[grid] = [gS, gE, gW]
			else: # You are on the Left Edge of the screen :> You can't go West!
				miniG[grid] = [gS, gE]

		else: # All the rest (Not Top or Bottom Boxes) :> You can go North or South
			if grid > col: # Away from the Left Border of the Screen
				if grid > (col*row)-col: # You are on the Right Border of the screen :> You can't go East!
					miniG[grid] = [gN, gS, gW]
				else: # Away from the Right Border of the Screen :> To the East you Go!
					miniG[grid] = [gN, gS, gE, gW]
			else: # You are on the Left Edge of the screen :> You can't go West!
				miniG[grid] = [gN, gS, gE]


	# FILTER OUT OBSTACLES FROM THE GRAPH!
	miniG2 = {}
	for grid in range(len(gridObjects)):
		grid += 1
		if grid not in gridObstacle:
			# gridObjects.remove(grid) # Dict object has no attribute : 'remove'
			# HACK :> I couldn't figure out a way to remove elements(keys) directly from a dictionary 
			miniG2[grid] = miniG[grid] # Created a new dictionary that stored the values required
			# IN-DEPTH FILTER :> Filter out obstacles from the neighbors-list
			for neigbor in miniG2[grid]:
				if neigbor in gridObstacle:
					miniG2[grid].remove(neigbor)

	# Filtering again as the first Filter block didn't clear out everything
	# Filtering through the neighbors
	for grid in miniG2:
		for item in miniG2[grid]:
			if item in gridObstacle:
				miniG2[grid].remove(item)


	return miniG2

def drawGraph(pathF):
	''' Draws the path given the path-list'''
	print(pathF)
	for grid in pathF:
		g = gridObjects[grid] # Get the grid-box object mentioned in the path
		x = g.x
		y = g.y
		sx = g.sx
		sy = g.sy
		pygame.draw.rect(SCREEN, GREEN, pygame.Rect(x,y,sx,sy))

def UIHandler(mouseObj):
	''' Handles the drawing of objects on the screens'''
	drawGrid(GRIDX, GRIDY)

	# Render the Grid objects (grid-boxes)
	for grid in gridObjects:
		gridObjects[grid].draw()

	# Render the Box Objects (Filled Boxes :> Obstacles, start & goal nodes)
	for bx in boxObjects:
		boxObjects[bx].draw()

	# Render the Obstacle Objects (Black Filled Boxes )
	for obs in obstacleObjects:
		obstacleObjects[obs].draw()

	if pathFound:
		drawGraph(pathFound)

def eventHandler(kbdObj,mouseObj):
	''' Handles events such as Keypresses and mouse movements'''
	global boxes
	global obstacles
	global startNode
	global goalNode
	global pathFound

	# If Key_s is pressed, set Start Node
	if kbdObj[pygame.K_s]:
		gBox = getGridBoxes(1)
		x = gBox.x
		y = gBox.y
		sx = gBox.sx
		sy = gBox.sy
		bo = Box(x,y,sx,sy,RED)
		boxObjects[boxes] = bo
		boxes += 1
		startNode = 1
		# Delay to avoid multiple spawning of objects
		pygame.time.wait(DELAY)

	# If Key_f is pressed, set goal node
	if kbdObj[pygame.K_f]:
		gBox = getGridBoxes(int(len(gridObjects)))
		x = gBox.x
		y = gBox.y
		sx = gBox.sx
		sy = gBox.sy
		bo = Box(x,y,sx,sy,BLUE)
		boxObjects[boxes] = bo
		boxes += 1
		goalNode = GRIDX*GRIDX
		# Delay to avoid multiple spawning of objects
		pygame.time.wait(DELAY)

	# If Key_x is pressed, spawn / instantiate an obstacle
	if kbdObj[pygame.K_x]:
		obs = Obstacle(mouseObj)
		obstacleObjects[obstacles] = obs
		# print(obs.gridBox)
		obstacles += 1
		# print(obstacleObjects)
		gridObstacle[obs.gridBox] = obstacles
		# Delay to avoid multiple spawning of objects
		pygame.time.wait(DELAY)

	# if Key_SPACE is pressed, start the magic
	if kbdObj[pygame.K_SPACE]:
		graph = generateGraph(GRIDY,GRIDX)
		bfs = BFS(graph, startNode, goalNode)
		# print(bfs.solve())
		pathFound = bfs.solve()
		# Delay to avoid multiple spawning of objects
		pygame.time.wait(DELAY)


# GAME LOOP :> This super loop runs the game!!!
done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	SCREEN.fill(WHITE)

	kbd = pygame.key.get_pressed()
	mse = pygame.mouse.get_pos()

	UIHandler(mse)
	eventHandler(kbd, mse)

	pygame.display.update()
	CLOCK.tick(FPS)