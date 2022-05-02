from game_log_data_generator import GameLogDataGenerator
import pickle
import numpy as np
import unittest
import os

class TestAlphaMiniShogiSearchTree(unittest.TestCase):
	def setUp(self):
		game_log = {
			'x': [1,2,3],
			'y': [[4,5,6],[7,8,9]]
		}
		file_name=f"test_1.pickle"
		f = open(file_name, "wb")
		f.write(pickle.dumps(game_log))
		f.close()

		game_log = {
			'x': [2,4,3],
			'y': [[5,3,6],[2,1,8]]
		}
		file_name=f"test_2.pickle"
		f = open(file_name, "wb")
		f.write(pickle.dumps(game_log))
		f.close()

	def tearDown(self):
		os.remove("test_1.pickle")
		os.remove("test_2.pickle")

	def test_batching(self):
		gen = GameLogDataGenerator("test_*.pickle",3)
		self.assertEqual(len(gen),2)
		self.assertEqual(gen.__getitem__(0)[0].tolist(), [1,2,3])
		self.assertEqual(gen.__getitem__(1)[0].tolist(), [2,4,3])

		gen = GameLogDataGenerator("test_*.pickle",2)
		self.assertEqual(len(gen),2)
		self.assertEqual(gen.__getitem__(0)[0].tolist(), [1,2])
		self.assertEqual(gen.__getitem__(1)[0].tolist(), [3])
		self.assertEqual(gen.__getitem__(2)[0].tolist(), [4,3])


