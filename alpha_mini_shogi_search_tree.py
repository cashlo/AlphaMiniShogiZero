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
			MiniShogiSearchTree.__init__(self, game)
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
						position = AlphaMiniShogiSearchTree.normalize_positon(p.position, player)
						player_piece[p.pieceType][player][position[0]][position[1]] = 1


			plane_stack = []
			for pieceType in MiniShogi.PieceType:
				if pieceType in {MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
					continue
				order = [self.game.current_player, 1-self.game.current_player]
				for player in order:
					plane_stack.append(player_piece[pieceType][player])
					plane_stack.append(player_prisoner[pieceType][player])

			return np.stack(tuple(plane_stack), axis=-1)

		def encode_output(self):
			distribution = np.zeros(MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6))
			for move in self.expanded_children:
				piece_type, old_position, new_position, promoted = move
				output_index  = AlphaMiniShogiSearchTree.get_output_index( piece_type, old_position, new_position, promoted, self.game.current_player )
				distribution[output_index] = self.expanded_children[move].visit_count/self.visit_count
			return distribution

		def get_output_index_multipler(piece_type, old_position, player):
			old_position = AlphaMiniShogiSearchTree.normalize_positon(old_position, player)
			piece_type_index = { t: i for i, t in enumerate(MiniShogi.PieceType) }
			if old_position is None:
				return piece_type_index[piece_type]
			# print("get_output_index_multipler", old_position[0], old_position[1])
			return old_position[0] + old_position[1]*MiniShogi.SIZE + 6

		def get_output_index(piece_type, old_position, new_position, promoted, player):
			index_multipler = AlphaMiniShogiSearchTree.get_output_index_multipler(piece_type, old_position, player)

			new_position = AlphaMiniShogiSearchTree.normalize_positon(new_position, player)
			y_position = new_position[1]
			if not promoted:
				y_position += 1

			# print("get_output_index", new_position[0]+y_position*MiniShogi.SIZE)
			return new_position[0]+ y_position*MiniShogi.SIZE + index_multipler*(MiniShogi.SIZE*(MiniShogi.SIZE+1))

		def normalize_positon(position, player):
			if position is None:
				return None
			if player == 1:
				return position
			return (MiniShogi.SIZE - position[0] - 1, MiniShogi.SIZE - position[1] - 1)


		def predict(self):
			model_input = np.expand_dims(self.encode_input(), axis=0)
			policy, reward = self.model.predict(model_input)
			return policy[0], reward[0]



game = setup_puzzle1()
tree = AlphaMiniShogiSearchTree(game, AlphaGoZeroModel(input_board_size=MiniShogi.SIZE, number_of_input_planes=6*2*2, policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6)).init_model())
tree.search()
print(tree.predict())
print(tree.encode_output())
