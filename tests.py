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

	def test_open_entrance_and_exit(self):
		num_cols = 12
		num_rows = 10
		NWpoint = Point(10, 10)
		m1 = Maze(NWpoint, 50, num_rows, num_cols)
		self.assertFalse(m1.cells[0][0].has_top_wall)
		self.assertFalse(m1.cells[-1][-1].has_bottom_wall)


if __name__ == "__main__":
	unittest.main()