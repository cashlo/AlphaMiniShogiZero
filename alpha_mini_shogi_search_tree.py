from mini_shogi_search_tree import MiniShogiSearchTree
from mini_shogi import MiniShogi
from alpha_go_zero_model import AlphaGoZeroModel

from collections import defaultdict
import numpy as np


def setup_puzzle1():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 2), False, 0))

	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   None  , False, 1))
	return game

class AlphaMiniShogiSearchTree(MiniShogiSearchTree):

		def __init__(self, game, model):
			self.game = game
			self.model = model

		def encode_input(self):
			player_piece    = defaultdict(lambda: [np.zeros((MiniShogi.SIZE, MiniShogi.SIZE)), np.zeros((MiniShogi.SIZE, MiniShogi.SIZE))])
			player_prisoner = defaultdict(lambda: [np.zeros((MiniShogi.SIZE, MiniShogi.SIZE)), np.zeros((MiniShogi.SIZE, MiniShogi.SIZE))])
			
			for pieceType in MiniShogi.PieceType:
				if pieceType in {MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
					continue
			

			for player, pieces in enumerate(self.game.player_pieces):
				for p in pieces:
					if p.position is None:
						player_prisoner[p.pieceType][player] += np.ones((MiniShogi.SIZE, MiniShogi.SIZE))
					else:
						player_piece[p.pieceType][player][p.position[0]][p.position[1]] = 1


			plane_stack = []
			for pieceType in MiniShogi.PieceType:
				if pieceType in {MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
					continue
				order = [self.game.current_player, 1-self.game.current_player]
				for player in order:
					plane_stack.append(player_piece[pieceType][player])
					plane_stack.append(player_prisoner[pieceType][player])

			return np.stack(tuple(plane_stack), axis=-1)

		def predict(self):
			model_input = np.expand_dims(self.encode_input(), axis=0)
			policy, reward = self.model.predict(model_input)
			return policy[0], reward[0]



game = setup_puzzle1()
tree = AlphaMiniShogiSearchTree(game, AlphaGoZeroModel(input_board_size=MiniShogi.SIZE, number_of_input_planes=6*2*2).init_model())

print(tree.predict())