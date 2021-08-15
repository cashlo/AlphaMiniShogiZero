from mini_shogi_search_tree import MiniShogiSearchTree
from mini_shogi import MiniShogi
from alpha_go_zero_model import AlphaGoZeroModel

from collections import defaultdict
import numpy as np
import math
from time import time

class AlphaMiniShogiSearchTree(MiniShogiSearchTree):

		def __init__(self, game, model, parent=None, from_move=None, simulation_limit=1500):
			MiniShogiSearchTree.__init__(self, game, parent=parent, from_move=from_move)
			self.simulation_limit = simulation_limit
			self.model = model
			self.policy = None
			self.reward = 0

		def search(self, step=5, gui=None):
			simulation_count = 0
			#past_nodes = []
			start_time = time()
			while simulation_count < self.simulation_limit:
				next_node = self.pick_next_node(self.exploration_constant)
				if gui is not None:
					gui.draw_board(next_node.game)
				# next_node.board.print()
				reward = next_node.rollout()
				next_node.backup(reward)
				simulation_count += 1
				#past_nodes.append(next_node)
			# self.print('')
			# code.interact(local=locals())
			# print(f"Number of sumulation: {simulation_count}")
			# print(f"thinking time: {time()-start_time}")
			return self.most_visited_child(random=step <= 10)

		def most_visited_child(self, random=False):
			if not random:
				return max(self.expanded_children.values(), key = lambda c: c.visit_count)
			child_list = list(self.expanded_children.values())
			probability_list = np.array([c.visit_count for c in child_list])
			probability_list = probability_list + probability_list.sum()/2 # Extra Randomness
			probability_list = probability_list / probability_list.sum()
			return np.random.choice(child_list, p=probability_list)

		def create_from_move(self, move):
			if move in self.expanded_children:
				return self.expanded_children[move]
			new_game = self.game.clone()
			new_game.make_move(move)
			return AlphaMiniShogiSearchTree(new_game, self.model, self, from_move=move, simulation_limit=self.simulation_limit)
			
		def ucb(self, n, exploration_constant):
			policy_index = AlphaMiniShogiSearchTree.get_output_index(n.from_move, n.game.current_player)
			return n.reward/n.visit_count + exploration_constant*self.policy[policy_index]*math.sqrt(self.visit_count)/(1+n.visit_count)        

		def pick_next_node(self, exploration_constant):
			def move_ucb(m, player):
				policy_index = AlphaMiniShogiSearchTree.get_output_index(m, player)
				return exploration_constant*self.policy[policy_index]*math.sqrt(self.visit_count)/1

			if self.is_terminal():
				return self

			if self.policy is None:
				self.rollout()

			if self.possible_move_list is None:
				self.possible_move_list = self.get_all_possible_moves()
				# random.shuffle(self.possible_move_list)
				# code.interact(local=locals())
				self.possible_move_list.sort(key=lambda m: move_ucb(m, self.game.current_player))
			
			if not self.expanded_children:
				return self.expand_last_move()

			max_ucb_child = self.best_UCB_child(exploration_constant)

			if self.possible_move_list:
				# code.interact(local=locals())
				max_ucb_move = self.possible_move_list[-1]
				if move_ucb(max_ucb_move, self.game.current_player) > self.ucb(max_ucb_child, exploration_constant):
					return self.expand_last_move()

			return max_ucb_child.pick_next_node(exploration_constant)

		def best_UCB_child(self, exploration_constant, random=False):
			if random:
				children_list = list(self.expanded_children.values())
				return np.random.choice(children_list)
			return max(self.expanded_children.values(), key= lambda c: self.ucb(c, exploration_constant))
		
		def rollout(self):
			winner = self.game.check_game_over()
			if winner == self.game.current_player:
				return -1
			if winner == 1-self.game.current_player:
				return 1
			policy, reward = self.predict()
			self.policy = policy
			return reward[0]

		def encode_input(self):
			player_piece             = defaultdict(lambda: [np.zeros((MiniShogi.SIZE, MiniShogi.SIZE)), np.zeros((MiniShogi.SIZE, MiniShogi.SIZE))])
			player_promoted_piece    = defaultdict(lambda: [np.zeros((MiniShogi.SIZE, MiniShogi.SIZE)), np.zeros((MiniShogi.SIZE, MiniShogi.SIZE))])

			player_prisoner = defaultdict(lambda: [np.zeros((MiniShogi.SIZE, MiniShogi.SIZE)), np.zeros((MiniShogi.SIZE, MiniShogi.SIZE))])
			
			for pieceType in MiniShogi.PieceType:
				if pieceType in {MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
					continue
			

			for player, pieces in enumerate(self.game.player_pieces):
				for p in pieces:
					if p.position is None:
						player_prisoner[p.pieceType][player] += np.ones((MiniShogi.SIZE, MiniShogi.SIZE))
					else:
						position = AlphaMiniShogiSearchTree.normalize_positon(p.position, self.game.current_player)
						if p.promoted:
							if pieceType in {MiniShogi.PieceType.KING, MiniShogi.PieceType.GOLD}:
								raise ValueError('illegal promotion!')
							player_promoted_piece[p.pieceType][player][position[0]][position[1]] = 1
						else:
							player_piece[p.pieceType][player][position[0]][position[1]] = 1


			plane_stack = []
			for pieceType in MiniShogi.PieceType:
				if pieceType in {MiniShogi.PieceType.DRAGON, MiniShogi.PieceType.HORSE}:
					continue
				order = [self.game.current_player, 1-self.game.current_player]
				for player in order:
					plane_stack.append(player_piece[pieceType][player])
					if pieceType not in {MiniShogi.PieceType.KING, MiniShogi.PieceType.GOLD}:
						plane_stack.append(player_promoted_piece[pieceType][player])
					plane_stack.append(player_prisoner[pieceType][player])

			return np.stack(tuple(plane_stack), axis=-1)

		def encode_output(self):
			distribution = np.zeros(MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6))
			for move in self.expanded_children:
				output_index  = AlphaMiniShogiSearchTree.get_output_index( move, self.game.current_player )
				distribution[output_index] = self.expanded_children[move].visit_count/self.visit_count
			return distribution

		def get_output_index_multipler(piece_type, old_position, player):
			old_position = AlphaMiniShogiSearchTree.normalize_positon(old_position, player)
			piece_type_index = { t: i for i, t in enumerate(MiniShogi.PieceType) }
			if old_position is None:
				return piece_type_index[piece_type]
			# print("get_output_index_multipler", old_position[0], old_position[1])
			return old_position[0] + old_position[1]*MiniShogi.SIZE + 6

		def get_output_index(move, player):
			piece_type, old_position, new_position, promoted = move
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


