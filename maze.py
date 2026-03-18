from time import sleep

from drawing import Line, Point, Window

"""
A cell used to represent a grid square in the maze
- NWpoint: top left corner of the cell
- side_length: the length of a side. Cells will be square, so this will serve for horizontal and vertical
- has_*_wall: booleans representing the 4 walls. True means the wall exists, False means it doesn't
- window: a pointer to the main drawing manager. If None, backend logic will still operate, but nothing will be visible onscreen
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

	"""
	Finds the center of this cell, and returns it as a Point
	parameters: none (uses class members)
	return: a new Point object
	"""
	def find_center(self):
		ctr_x = self.NWPoint.x + (self.side_length // 2)
		ctr_y = self.NWPoint.y + (self.side_length // 2)
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
	def __init__(self, NWpoint:Point, cell_side_length:int, num_rows:int, num_cols:int, window:Window=None):
		self.NWpoint = NWpoint
		self.cell_side_length = cell_side_length
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.window = window
		self.cells = []
		self.create_cells()
		self.open_entrance_and_exit()
		self.draw_cells()

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

	def open_entrance_and_exit(self):
		self.cells[0][0].has_top_wall = False
		self.cells[-1][-1].has_bottom_wall = False
	
	def draw_cells(self):
		if self.window is None:
			return
		for col in self.cells:
			for cell in col:
				cell.draw()
				self.animate()

	def animate(self):
		self.window.redraw()
		sleep(0.01)
