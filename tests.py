import unittest
from maze import Maze
from drawing import Point

class Tests(unittest.TestCase):
	def test_maze_create_cells(self):
		num_cols = 12
		num_rows = 10
		NWpoint = Point(10, 10)
		m1 = Maze(NWpoint, 50, num_rows, num_cols)
		self.assertEqual(num_cols, len(m1.cells))
		self.assertEqual(num_rows, len(m1.cells[0]))

if __name__ == "__main__":
	unittest.main()