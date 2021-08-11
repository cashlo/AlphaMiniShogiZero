from mini_shogi import MiniShogi
from alpha_mini_shogi_search_tree import AlphaMiniShogiSearchTree
import unittest

class TestAlphaMiniShogiSearchTreeMethods(unittest.TestCase):
	def test_output_index_distribution(self):
		index_distribution = [0]*(MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6))

		for player in [0, 1]:
			index_distribution = [0]*(MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6))						
			for pieceType in MiniShogi.PieceType:
				if pieceType in {MiniShogi.PieceType.KING, MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
					continue
				
				for new_position_x in range(MiniShogi.SIZE):
					for new_position_y in range(MiniShogi.SIZE):
						promoted = False
						index_distribution[AlphaMiniShogiSearchTree.get_output_index( pieceType, None, (new_position_x, new_position_y), promoted, player )] += 1

			for old_position_x in range(MiniShogi.SIZE):
				for old_position_y in range(MiniShogi.SIZE):
					for new_position_x in range(MiniShogi.SIZE):
						for new_position_y in range(MiniShogi.SIZE):
							for promoted in [False, True]:
								if promoted and player == 0 and new_position_y != 4:
									continue
								if promoted and player == 1 and new_position_y != 0:
									continue

								index_distribution[AlphaMiniShogiSearchTree.get_output_index( None, (old_position_x, old_position_y), (new_position_x, new_position_y), promoted, player )] += 1
			for d in index_distribution:
				self.assertTrue(d <= 1)