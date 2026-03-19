from drawing import Point, Window
from maze import Maze

def main():
	win = Window(800, 600)

	NWpoint = Point(10, 10)
	maze = Maze(NWpoint, 20, 20, 30, win)
	maze.solve_maze(0, 0)
	win.wait_for_close()

if __name__ == "__main__":
	main()
