from tkinter import Tk, BOTH, Canvas

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Line:
	def __init__(self, pointA:Point, pointB:Point):
		self.pointA = pointA
		self.pointB = pointB
	
	def draw(self, canvas:Canvas, fill_color:str):
		x1 = self.pointA.x
		y1 = self.pointA.y
		x2 = self.pointB.x
		y2 = self.pointB.y

		canvas.create_line(x1, y1, x2, y2, fill=fill_color, width = 2)


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


def main():
	win = Window(800, 600)
	pointA = Point(10, 10)
	pointB = Point(30, 30)
	pointC = Point(10, 50)
	pointD = Point(80, 10)
	line1 = Line(pointA, pointB)
	line2 = Line(pointA, pointC)
	line3 = Line(pointA, pointD)
	line4 = Line(pointB, pointD)
	win.draw_line(line1, "black")
	win.draw_line(line2)
	win.draw_line(line3, "green")
	win.draw_line(line4, "red")

	win.wait_for_close()

if __name__ == "__main__":
	main()
