from gamewindow import GameWindow
from mini_shogi import MiniShogi
from mini_shogi_search_tree import MiniShogiSearchTree
import glob
import tensorflow as tf

from alpha_go_zero_model import AlphaGoZeroModel
from alpha_mini_shogi_search_tree import AlphaMiniShogiSearchTree

def setup_puzzle1():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 2), False, 0))

	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   None  , False, 1))
	return game


def setup_puzzle2():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (3, 0), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   (4, 0), False, 0))


	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (1, 1), True, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,     None, False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER,   None, False, 1))
	return game

def setup_puzzle3():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 1), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   (3, 1), False, 0))


	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (0, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (1, 3), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (2, 3), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (3, 3), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,     None, False, 1))
	
	return game


game = setup_puzzle2()

window = GameWindow("Puzzle 1")
tree_window = GameWindow("Tree View", canvas_size=400,tree_window=True)
mind_window = GameWindow("Mind View", canvas_size=400)


window.draw_board(game)


best_net_so_far = AlphaGoZeroModel(
		input_board_size=MiniShogi.SIZE,
		number_of_input_planes=6*2*2+4*2,
		policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6),
		number_of_filters=64,
		number_of_residual_block=20,
		value_head_hidden_layer_size=64
	).init_model()

net_files = glob.glob(f'model_minishogi_*')
if net_files:
	lastest_model_file = max(net_files)
	print(f"Lastest net: {lastest_model_file}")
#	best_net_so_far.model = tf.keras.models.load_model(lastest_model_file)

no_net_search_tree = MiniShogiSearchTree(game.clone())

search_tree = AlphaMiniShogiSearchTree(game.clone(), best_net_so_far, simulation_limit=1000)
no_net_search_tree = no_net_search_tree.search(move_window=mind_window, tree_window=tree_window) #  
move = search_tree.from_move
# game.make_move(move)
window.draw_move(move)


window.mainloop()