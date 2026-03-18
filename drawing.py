from tkinter import Canvas, Tk

"""
Represents a point for drawing.
members:
- x: pixel location (0 on left)
- y: pixel location (0 on top)
"""
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return f"({self.x}, {self.y})"

"""
Represents a line for drawing.
members:
pointA: 
pointB:
"""
class Line:
	def __init__(self, pointA:Point, pointB:Point):
		self.pointA = pointA
		self.pointB = pointB

	def __str__(self):
		return f"Line from {self.pointA} to {self.pointB}"
	
	"""
	given a canvas and a fill color, draw a line between the member points.
	"""
	def draw(self, canvas:Canvas, fill_color:str):
		x1 = self.pointA.x
		y1 = self.pointA.y
		x2 = self.pointB.x
		y2 = self.pointB.y

		canvas.create_line(x1, y1, x2, y2, fill=fill_color, width = 2)

"""
The main drawing manager.
members:
width, height: dimensions of the window
root: the main Tk() object
canvas: the drawing surface
is_running: boolean used to maintain or terminate the GUI display loop
"""
class Window:
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.root = Tk()
		self.root.title = "Maze Solver"
		self.canvas = Canvas(width=self.width, height=self.height)
		self.canvas.pack()
		self.is_running = False

		self.root.protocol("WM_DELETE_WINDOW", self.close)

	def redraw(self):
		self.root.update_idletasks()
		self.root.update()

	def wait_for_close(self):
		self.is_running = True
		while self.is_running:
			self.redraw()
	
	def close(self):
		self.is_running = False

	def draw_line(self, line:Line, fill_color="black"):
		line.draw(self.canvas, fill_color)