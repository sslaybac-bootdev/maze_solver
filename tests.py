import unittest
from maze import Maze
from drawing import Point

class Tests(unittest.TestCase):
	def create_maze(self, num_rows, num_cols):
		NWpoint = Point(10, 10)
		return Maze(NWpoint, 50, num_rows, num_cols)

	def test_maze_create_cells(self):
		num_cols = 12
		num_rows = 10
		m1 = self.create_maze(num_rows, num_cols)
		self.assertEqual(num_cols, len(m1.cells))
		self.assertEqual(num_rows, len(m1.cells[0]))

	def test_open_entrance_and_exit(self):
		m1 = self.create_maze(10, 12)
		self.assertFalse(m1.cells[0][0].has_top_wall)
		self.assertFalse(m1.cells[-1][-1].has_bottom_wall)

	def test_visit_reset(self):
		m1 = self.create_maze(10, 12)
		for col in m1.cells:
			for cell in col:
				self.assertFalse(cell.visited)


if __name__ == "__main__":
	unittest.main()