from alpha_go_zero_model import AlphaGoZeroModel
from mini_shogi import MiniShogi
from alpha_mini_shogi_search_tree import AlphaMiniShogiSearchTree
from time import time
import pickle
import tensorflow as tf
import concurrent.futures
import glob
import os
import argparse
import sys
from gamewindow import GameWindow

def backfill_end_reward(game_log, game_steps_count, result, last_player):
	game_reward = [0]*game_steps_count
	index = game_steps_count-1
	reward = 1 if last_player == result else -1
	if result is None:
		reward = 0
	while index >= 0:
		game_reward[index] = reward
		reward = -reward
		index -= 1
	game_log['y'][1].extend(game_reward)
	return game_log

def save_game_log(game_log, sim_limit, file_name=None):
	if not file_name:
		file_name=f"game_log_minishogi_{sim_limit}.pickle"
	f = open(file_name, "wb")
	f.write(pickle.dumps(game_log))
	f.close()
		

def generate_data(game_log, net, number_of_games, gui, mind_window, simulation_limit=50):
	for i in range(number_of_games):
		game = MiniShogi.Game()
		game.setup()
		search_tree = AlphaMiniShogiSearchTree(game.clone(), net,simulation_limit=simulation_limit)
		game_steps_count = 0
		# gui.set_status(f"Game {i+1}")
		while game.check_game_over() is None:
			# print(search_tree.game)
			move = search_tree.search(step=game_steps_count, gui=mind_window).from_move

			game_log['x'].append(search_tree.encode_input())
			game_log['y'][0].append(search_tree.encode_output())
			
			game_steps_count += 1
			game.make_move(move)
			gui.draw_board(game)
			gui.draw_move(move)

			search_tree = search_tree.create_from_move(move)
			if game.is_repeating():
				break
			if game_steps_count >= 100:
				break
		winner = game.check_game_over()
		print(f"Game {i+1}: {game_steps_count} moves {winner} win")
		game.print()
		backfill_end_reward(game_log, game_steps_count, winner, 1-game.current_player)

def net_vs(net_0, net_1, number_of_games, game_log, gui, mind_window_0, mind_window_1, simulation_limit=50):
	winner_count = [0, 0]
	for i in range(number_of_games):
		gui.set_status(f"Game {i+1}    Score so far {winner_count[0]}:{winner_count[1]}")
		game = MiniShogi.Game()
		game.setup()
		
		tree_dict = {
			0: [
				0,
				AlphaMiniShogiSearchTree(game.clone(), net_0, simulation_limit=simulation_limit),
				mind_window_0
			],
			1: [
				1,
				AlphaMiniShogiSearchTree(game.clone(), net_1, simulation_limit=simulation_limit),
				mind_window_1
			]
		}
		if i%2:
			tree_dict = {
				1: tree_dict[0],
				0: tree_dict[1]
			}
		#print(f"Black is net {tree_dict[Gomoku.BLACK][0]}")
		#print(f"White is net {tree_dict[Gomoku.WHITE][0]}")
		player = game.current_player
		game_steps_count = 0
		while game.check_game_over() is None:
			move = tree_dict[player][1].search(step=game_steps_count, gui=tree_dict[player][2]).from_move

			game_log['x'].append(tree_dict[player][1].encode_input())
			game_log['y'][0].append(tree_dict[player][1].encode_output())

			game_steps_count += 1
			game.make_move(move)
			gui.draw_board(game)
			gui.draw_move(move)

			tree_dict[player][1] = tree_dict[player][1].create_from_move(move)
			player = 1-player
			tree_dict[player][1] = tree_dict[player][1].create_from_move(move)
			# game.board.print()
			if game.is_repeating():
				break
			if game_steps_count >= 100:
				break
		game.print()
		result = game.check_game_over()
		backfill_end_reward(game_log, game_steps_count, result, 1-player)
		#if result != Gomoku.DRAW:
		if result is not None:
			winner = tree_dict[result][0]
			winner_count[winner] += 1
		print(f"Game {i+1}: {winner_count[0]}:{winner_count[1]}")
	print(f"Net 0 win rate: {winner_count[0]/number_of_games:.0%}")
	print(f"Net 1 win rate: {winner_count[1]/number_of_games:.0%}")
	return winner_count[1]/number_of_games

parser = argparse.ArgumentParser()
parser.add_argument("--gen-data", help="Generate new data with latest net", action="store_true")
parser.add_argument("--train-new-net", help="Train new NN", action="store_true")
parser.add_argument("id", type=int, help="instant id", default=0, nargs='?')

args = parser.parse_args()
if args.gen_data:
	sim_limit = 1000

	game_log = {
		'x': [],
		'y': [[],[]]
	}
	if os.path.isfile(f"game_log_minishogi_{sim_limit}_{args.id}.pickle"):
		game_log = pickle.loads(open(f"game_log_minishogi_{sim_limit}_{args.id}.pickle", "rb").read())

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
	else:
		print("Model file not found")

	gui = GameWindow("Current AI self-play to generate new data for training")
	# mind_window = GameWindow("Considering move", canvas_size=400, show_title=False)

	while True:
		net_files = glob.glob(f'model_minishogi_*')
		if net_files and lastest_model_file != max(net_files):
			lastest_model_file = max(net_files)
			gui.set_status(f"Lastest net: {lastest_model_file}")
			best_net_so_far.model = tf.keras.models.load_model(lastest_model_file)

		start_time = time()
		gui.set_status("Generating new data...")
		generate_data(game_log, best_net_so_far, 1, gui, None, sim_limit)
		save_game_log(game_log, sim_limit, file_name=f"game_log_minishogi_{sim_limit}_{args.id}.pickle")
		gui.set_status(f"Time taken: {time()-start_time}")			

	

if args.train_new_net:
	game_log = {
		'x': [],
		'y': [[],[]]
	}
	net_vs_game_log = {
		'x': [],
		'y': [[],[]]
	}

	sim_limit = 100
	
	if os.path.isfile(f"net_vs_game_log_minishogi_{sim_limit}.pickle"):
		net_vs_game_log = pickle.loads(open(f"net_vs_game_log_minishogi_{sim_limit}.pickle", "rb").read())
	

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
		# print(f"Lastest net: {lastest_model_file}")
		# best_net_so_far.model = tf.keras.models.load_model(lastest_model_file)

	gui = GameWindow("Newly trained AI fight current AI to become the data generating AI")
	mind_window_1 = GameWindow("Current AI", show_title=False, line_width=4, canvas_size=400)
	mind_window_2 = GameWindow("New AI", show_title=False, line_width=4, canvas_size=400)

	while True:
		gui.set_status("Training new AI...")
		start_time = time()


		fresh_net = AlphaGoZeroModel(
			input_board_size=MiniShogi.SIZE,
			number_of_input_planes=6*2*2+4*2,
			policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6),
			number_of_filters=32,
			number_of_residual_block=10,
			value_head_hidden_layer_size=32
		).init_model()

		extra_game_log_files = glob.glob(f'game_log_minishogi_1000_*')
		for file in extra_game_log_files:
			extra_game_log = pickle.loads(open(file, "rb").read())

			game_log['x'].extend( extra_game_log['x'] )
			game_log['y'][0].extend( extra_game_log['y'][0] )
			game_log['y'][1].extend( extra_game_log['y'][1] )

		extra_game_log_files = glob.glob(f'mac_data/game_log_minishogi_1000_*')
		for file in extra_game_log_files:
			extra_game_log = pickle.loads(open(file, "rb").read())

			game_log['x'].extend( extra_game_log['x'] )
			game_log['y'][0].extend( extra_game_log['y'][0] )
			game_log['y'][1].extend( extra_game_log['y'][1] )



		fresh_net.train_from_game_log(game_log)
		print(f"Time taken: {time()-start_time}")

		print("Evaluate old net:")
		#best_net_so_far.model.summary()
		print(best_net_so_far.evaluate_from_game_log(game_log))
		print("Evaluate new net:")
		#fresh_net.model.summary()
		print(fresh_net.evaluate_from_game_log(game_log))

		gui.set_status("Checking new net performance...")
		start_time = time()
		fresh_net_win_rate = net_vs(best_net_so_far, fresh_net, 20, net_vs_game_log, gui, mind_window_1, mind_window_2, sim_limit)
		save_game_log(net_vs_game_log, sim_limit, f"net_vs_game_log_{sim_limit}.pickle")
		if fresh_net_win_rate >= 0.65:
			gui.set_status("New net won!")
			best_net_so_far = fresh_net
			saved_model_dir = f'model_minishogi_{time()}'
			fresh_net.model.save(saved_model_dir)
		print(f"Time taken: {time()-start_time}")

parser.print_help()
