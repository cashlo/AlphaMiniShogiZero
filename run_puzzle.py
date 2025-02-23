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

def setup_puzzle4(): # puzzle book 6
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 0), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (4, 2), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, (3, 0), False, 0))
	


	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   (3, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (2, 0), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   None, False, 1))
	
	
	return game

def setup_puzzle5(): # puzzle book 7
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (3, 0), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (4, 0), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, (2, 0), False, 0))
	


	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   (4, 1), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,     None, False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER,   None, False, 1))
	
	
	return game


game = setup_puzzle5()

window = GameWindow("Puzzle 1")
tree_window = GameWindow("Tree View", canvas_size=200,tree_window=True)
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

no_net_search_tree = MiniShogiSearchTree(game.clone(), simulation_limit=5000)

search_tree = AlphaMiniShogiSearchTree(game.clone(), best_net_so_far, simulation_limit=5000)
import time
start_time = time.perf_counter()
# search_tree = search_tree.search(move_window=mind_window, tree_window=tree_window)
no_net_search_tree = no_net_search_tree.search(move_window=mind_window, tree_window=tree_window)

end_time = time.perf_counter()
print(f"Thinking for  {end_time - start_time:0.4f} seconds")

move = search_tree.from_move
# game.make_move(move)
window.draw_move(move)


window.mainloop()