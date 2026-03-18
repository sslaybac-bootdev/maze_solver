from time import sleep

from drawing import Line, Point, Window

"""
A cell used to represent a grid square in the maze
- x1, y1: the top-left corner
- x2, y2: the bottom-right corner
- has_*_wall: booleans representing the 4 walls. True means the wall is drawn, False means it isn't
- window: a pointer to the main drawing manager
"""
class Cell:
	def __init__(self, window:Window, x1=-1, y1=-1, x2=-1, y2=-1, top=True, left=True, right=True, bottom=True):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.normalize()
		self.has_left_wall = left
		self.has_right_wall = right
		self.has_top_wall = top
		self.has_bottom_wall = bottom
		self.window = window

	"""
	Aligns the x,y coordinates so that 1s are in the top left, 2s are in the botom right
	"""
	def normalize(self):
		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2
		self.x1 = min(x1, x2)
		self.y1 = min(y1, y2)
		self.x2 = max(x1, x2)
		self.y2 = max(y1, y2)

	def draw(self, x1=None, y1=None, x2=None, y2=None):
		if x1 is not None:
			self.x1 = x1
		if y1 is not None:
			self.y1 = y1
		if x2 is not None:
			self.x2 = x2
		if y2 is not None:
			self.y2 = y2
		self.normalize()
		NWpoint = Point(self.x1, self.y1)
		SWpoint = Point(self.x1,self.y2)
		SEpoint = Point(self.x2,self.y2)
		NEpoint = Point(self.x2,self.y1)
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

	"""
	Finds the center of this cell, and returns it as a Point
	parameters: none (uses class members)
	return: a new Point object
	"""
	def find_center(self):
		avg_x = (self.x1 + self.x2) // 2
		avg_y = (self.y1 + self.y2) // 2
		return Point(avg_x, avg_y)
	
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

class Maze:
	def __init__(self, x1, y1, rows, cols, cell_width, cell_height, win):
		self.x1 = x1
		self.y1 = y1
		self.rows = rows
		self.cols = cols
		self.cell_width = cell_width
		self.cell_height = cell_height
		self.window = win
		self.cells = []
		self.create_cells()
		self.draw_cells()

	def create_cells(self):
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				x1 = self.x1 + r*self.cell_width
				y1 = self.y1 + c*self.cell_height
				x2 = self.x1 + (r+1)*self.cell_width
				y2 = self.y1 + (c+1)*self.cell_height
				cell = Cell(self.window, x1, y1, x2, y2)
				row.append(cell)
			self.cells.append(row)
	
	def draw_cells(self):
		for row in self.cells:
			for cell in row:
				cell.draw()
				self.animate()

	def animate(self):
		self.window.redraw()
		sleep(0.05)
