import random
from time import sleep

from drawing import Line, Point, Window

"""
A cell used to represent a grid square in the maze
- NWpoint: top left corner of the cell
- side_length: the length of a side. Cells will be square, so this will serve for horizontal and vertical
- has_*_wall: booleans representing the 4 walls. True means the wall exists, False means it doesn't
- window: a pointer to the main drawing manager. If None, backend logic will still operate, but nothing will be visible onscreen
- visited: when building the maze, the Maze object will traverse the cells and break walls, in order to create a path from start to end. During this process, we need to track whether a given cell has been visited. This variable is True if the cell has aready been visited, but false otherwise
"""
class Cell:
	"""
	constructor for Cell class
	parameters:
	NWpoint: a Point object showing the top left of the cell.
	side_length: the length of a side. Cells will be square, so this will serve for horizontal and vertical
	"""
	def __init__(self, NWpoint:Point, side_length:int, window:Window=None):
		self.NWpoint = NWpoint
		self.side_length = side_length
		self.has_left_wall = True
		self.has_right_wall = True
		self.has_top_wall = True
		self.has_bottom_wall = True
		self.window = window
		self.visited = False

	def getNWpoint(self):
		return self.NWpoint
	
	def getNEpoint(self):
		x = self.NWpoint.x + self.side_length
		y = self.NWpoint.y
		return Point(x,y)

	def getSWpoint(self):
		x = self.NWpoint.x
		y = self.NWpoint.y + self.side_length
		return Point(x,y)

	def getSEpoint(self):
		x = self.NWpoint.x + self.side_length
		y = self.NWpoint.y + self.side_length
		return Point(x,y)

	def draw(self):
		if self.window is None:
			return
		NWpoint = self.getNWpoint()
		SWpoint = self.getSWpoint()
		SEpoint = self.getSEpoint()
		NEpoint = self.getNEpoint()
		if self.has_left_wall:
			line = Line(NWpoint, SWpoint)
			self.window.draw_line(line)
		if self.has_bottom_wall:
			line = Line(SWpoint, SEpoint)
			self.window.draw_line(line)
		if self.has_right_wall:
			line = Line(NEpoint, SEpoint)
			self.window.draw_line(line)
		if self.has_top_wall:
			line = Line(NWpoint, NEpoint)
			self.window.draw_line(line)

	def visit(self):
		self.visited = True

	def reset_visit(self): 
		self.visited = False

	"""
	Finds the center of this cell, and returns it as a Point
	parameters: none (uses class members)
	return: a new Point object
	"""
	def find_center(self):
		ctr_x = self.NWpoint.x + (self.side_length // 2)
		ctr_y = self.NWpoint.y + (self.side_length // 2)
		return Point(ctr_x, ctr_y)
	
	"""
	Draws a line between the center of this Cell and another Cell
	parameters:
	- to_cell: the other Cell for this drawing
	- undo: a boolean used to select line color
		- False: this is a new line and we draw it in red
		- True: this is a bactrack over an old line, and we draw it in gray
	"""
	def draw_move(self, to_cell:"Cell", undo=False):
		pointA = self.find_center()
		pointB = to_cell.find_center()
		color = "gray" if undo else "red"
		self.window.draw_line(Line(pointA, pointB), color)

"""
Class representing a grid-based maze.
Includes backend logic, and links to drawing.
members:
NWpoint: the top left point of the whole maze
cell_side_length: the width/height of each square cell in pixels.
num_rows: number of rows in the maze
num_cols: number of columns in the maze
win: the GUI window used to display the maze
cells: a 2D array holding all cells
"""
class Maze:
	def __init__(self, NWpoint:Point, cell_side_length:int, num_rows:int, num_cols:int, window:Window=None, seed=None):
		self.NWpoint = NWpoint
		self.cell_side_length = cell_side_length
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.window = window
		if seed is not None:
			random.seed(seed)
		self.cells = []
		self.create_cells()
		self.open_entrance_and_exit()
		self.break_walls(0, 0)
		self.reset_visited()
		self.draw_cells()

	"""
	Creates a 2D list of Cells, ready to be drawn.
	"""
	def create_cells(self):
		for c in range(self.num_cols):
			col = []
			for r in range(self.num_rows):
				x = self.NWpoint.x + c*self.cell_side_length
				y = self.NWpoint.y + r*self.cell_side_length
				cell_NWpoint = Point(x, y)
				cell = Cell(cell_NWpoint, self.cell_side_length, self.window)
				col.append(cell)
			self.cells.append(col)

	"""
	Opens walls in the top left cell and bottom right cell. These will serve as the maze entrance and exit.
	"""
	def open_entrance_and_exit(self):
		self.cells[0][0].has_top_wall = False
		self.cells[-1][-1].has_bottom_wall = False
	
	"""
	(Recursive) Open a random set of walls throughout the maze.
	parameters
	- i, j: the x,y grid coordinates for the current cell
	return: none
	side effects: a random selection of walls will be removed
		from the current cell. The neighbors of the cell will
		also have their matching walls removed. The outside walls
		of the maze are not eligible for removal.
	"""
	def break_walls(self, i, j):
		self.cells[i][j].visit()
		while True:
			neighbors = []
			if i > 0 and not self.cells[i-1][j].visited:
				neighbors.append((i-1, j, "left"))
			if j > 0 and not self.cells[i][j-1].visited:
				neighbors.append((i, j-1, "top"))
			if i < self.num_cols - 1 and not self.cells[i+1][j].visited:
				neighbors.append((i+1, j, "right"))
			if j < self.num_rows - 1 and not self.cells[i][j+1].visited:
				neighbors.append((i, j+1, "bottom"))

			if len(neighbors) <= 0:
				return

			else:
				next = random.choice(neighbors)
				if next[2] == "left":
					self.cells[i][j].has_left_wall = False
					self.cells[i-1][j].has_right_wall = False
				if next[2] == "top":
					self.cells[i][j].has_top_wall = False
					self.cells[i][j-1].has_bottom_wall = False
				if next[2] == "right":
					self.cells[i][j].has_right_wall = False
					self.cells[i+1][j].has_left_wall = False
				if next[2] == "bottom":
					self.cells[i][j].has_bottom_wall = False
					self.cells[i][j+1].has_top_wall = False
				self.break_walls(next[0], next[1])

	"""
	reset the visited status of all cells
		This is run after breaking walls throughout the maze.
	side effects: visited member of all cells is set to False
	"""
	def reset_visited(self):
		for col in self.cells:
			for cell in col:
				cell.reset_visit()

	"""
	Check if it is possible to move from the given cell
	to a neighbor in the chosen direction
	parameters:
	i, j: coordinates of current cell
	return:
	- True if the neighbor exists,
		if there are no blocking walls,
		and if the neighbor hasn't already been visited.
	- False otherwise
	"""
	def can_go_left(self, i, j):
		if i == 0:
			return False
		if self.cells[i][j].has_left_wall:
			return False
		if self.cells[i-1][j].visited:
			return False
		return True

	def can_go_up(self, i, j):
		if j == 0:
			return False
		if self.cells[i][j].has_top_wall:
			return False
		if self.cells[i][j-1].visited:
			return False
		return True

	def can_go_right(self, i, j):
		if i == self.num_cols-1:
			return False
		if self.cells[i][j].has_right_wall:
			return False
		if self.cells[i+1][j].visited:
			return False
		return True

	def can_go_down(self, i, j):
		if j == self.num_rows-1:
			return False
		if self.cells[i][j].has_bottom_wall:
			return False
		if self.cells[i][j+1].visited:
			return False
		return True
	"""
	(Recursive): bruteforces the maze, backtracking as needed.
	parameters:
	- i,j coordinates of cell for current iteration
	return:
	- True: if the path from start to end passes through this cell
	- False: otherwise
	"""
	def solve_maze(self, i, j):
		self.animate()
		cell:Cell = self.cells[i][j]
		cell.visit()

		if i == self.num_cols-1 and j == self.num_rows-1:
			return True

		# move left
		if self.can_go_left(i, j):
			cell.draw_move(self.cells[i-1][j])
			if self.solve_maze(i-1, j):
				return True
			else:
				cell.draw_move(self.cells[i-1][j], True)
		# move up
		if self.can_go_up(i, j):
			cell.draw_move(self.cells[i][j-1])
			if self.solve_maze(i, j-1):
				return True
			else:
				cell.draw_move(self.cells[i][j-1], True)
		# move right
		if self.can_go_right(i, j):
			cell.draw_move(self.cells[i+1][j])
			if self.solve_maze(i+1, j):
				return True
			else:
				cell.draw_move(self.cells[i+1][j], True)
		# move down
		if self.can_go_down(i, j):
			cell.draw_move(self.cells[i][j+1])
			if self.solve_maze(i, j+1):
				return True
			else:
				cell.draw_move(self.cells[i][j+1], True)

		return False

	"""
	Draws all maze cells in the GUI
	parameters: none
	return: none
	side effects: adds to GUI
	"""
	def draw_cells(self):
		if self.window is None:
			return
		for col in self.cells:
			for cell in col:
				cell.draw()

	"""
	Cosmetic function for the GUI. Inserts a slight delay
		between drawing new lines to give the illusion of animation.
	parameters: none
	return: none
	"""
	def animate(self):
		self.window.redraw()
		sleep(0.05)
