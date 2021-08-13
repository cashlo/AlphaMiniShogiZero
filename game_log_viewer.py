import pickle
from mini_shogi import MiniShogi
from gamewindow import GameWindow
from alpha_mini_shogi_search_tree import AlphaMiniShogiSearchTree
import numpy as np
from alpha_go_zero_model import AlphaGoZeroModel
import glob
import tensorflow as tf


def last_move(event):
	global index
	index -= 1
	show_game_log(game_log, index)

def next_move(event):
	global index
	index += 1
	show_game_log(game_log, index)
	
window = GameWindow("Game log viewer")
window.window.bind('<Left>', last_move)
window.window.bind('<Right>', next_move)
index = 0
game_log = pickle.loads(open('game_log_minishogi_100.pickle', "rb").read())

def place_piece_from_plane(game, plane, pieceType, promoted, player):
	for f in range(MiniShogi.SIZE):
		for r in range(MiniShogi.SIZE):
			if plane[f][r] == 1:
				game.place_piece( MiniShogi.Piece(pieceType,   (f, r), False, player) )


def resort_game(window, encoded_input):
	game = MiniShogi.Game()
	for pieceType in MiniShogi.PieceType:
		if pieceType in {MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
			continue

		for player in [1, 0]:
			place_piece_from_plane(game, encoded_input.pop(0), pieceType, False, player)
			if pieceType not in {MiniShogi.PieceType.KING, MiniShogi.PieceType.GOLD}:
				place_piece_from_plane(game, encoded_input.pop(0), pieceType, True, player)
			prisoner_plane = encoded_input.pop(0)
			for i in range(int(prisoner_plane[0][0])):
				game.place_piece( MiniShogi.Piece(pieceType,   None, False, player) )
	window.draw_board(game)
	return game

def show_policy(policy, game, player):
	legal_moves = game.all_legal_moves(player)
	move_list = []
	for m in legal_moves:
		move_prob = policy[AlphaMiniShogiSearchTree.get_output_index( m, player )]
		move_list.append( (move_prob, m) )
	move_list.sort(reverse=True, key=lambda m:m[0])
	for m in move_list:
		print(m)

def show_game_log(game_log, index):
	game_log_x = np.moveaxis(game_log['x'][index], -1, 0)
	print("Reward: ", game_log['y'][1][index])
	game = resort_game(window, game_log_x.tolist())
	policy, reward = AlphaMiniShogiSearchTree(game, best_net_so_far).predict()
	print("Model Reward: ", reward)
	print("Player 0 moves:")
	show_policy(game_log['y'][0][index], game, 0)
	print("Player 0 net moves:")
	show_policy(policy, game, 0)
	
	print("Player 1 moves:")
	show_policy(game_log['y'][0][index], game, 1)
	print("Player 1 net moves:")
	show_policy(policy, game, 1)
	
	
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
	best_net_so_far.model = tf.keras.models.load_model(lastest_model_file)
	
show_game_log(game_log, index)
window.mainloop()