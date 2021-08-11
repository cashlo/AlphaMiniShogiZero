from mini_shogi import MiniShogi
from alpha_go_zero_model import AlphaGoZeroModel
from alpha_mini_shogi_search_tree import AlphaMiniShogiSearchTree
import unittest


def setup_puzzle1():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 2), False, 0))

	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   None  , False, 1))
	return game

def setup_puzzle2():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 2), False, 1))

	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 2), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   None  , False, 0))
	return game

class TestAlphaMiniShogiSearchTreeMethods(unittest.TestCase):

	def test_search(self):
		game = setup_puzzle1()
		tree = AlphaMiniShogiSearchTree(game, AlphaGoZeroModel(input_board_size=MiniShogi.SIZE, number_of_input_planes=6*2*2, policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6)).init_model())
		print("Reward: ", tree.search().reward)
		
		game = setup_puzzle2()
		# game.current_player = 0
		tree = AlphaMiniShogiSearchTree(game, AlphaGoZeroModel(input_board_size=MiniShogi.SIZE, number_of_input_planes=6*2*2, policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6)).init_model())
		print("Reward: ", tree.search().reward)
		
		# print(tree.predict())
		# print(tree.encode_output())


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
						index_distribution[AlphaMiniShogiSearchTree.get_output_index( (pieceType, None, (new_position_x, new_position_y), promoted), player )] += 1

			for old_position_x in range(MiniShogi.SIZE):
				for old_position_y in range(MiniShogi.SIZE):
					for new_position_x in range(MiniShogi.SIZE):
						for new_position_y in range(MiniShogi.SIZE):
							for promoted in [False, True]:
								if promoted and player == 0 and new_position_y != 4:
									continue
								if promoted and player == 1 and new_position_y != 0:
									continue

								index_distribution[AlphaMiniShogiSearchTree.get_output_index( (None, (old_position_x, old_position_y), (new_position_x, new_position_y), promoted), player )] += 1
			for d in index_distribution:
				self.assertTrue(d <= 1)