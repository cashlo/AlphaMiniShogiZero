import math
import code
import random
from time import time

class Node:
	def __init__(self, parent=None, from_move=None, simulation_limit=1000, exploration_constant=1, reward_decay=1):
		self.parent=parent
		self.reward = 0
		self.visit_count = 1
		self.possible_move_list = None
		self.expanded_children = {}
		self.simulation_limit = simulation_limit
		self.exploration_constant = exploration_constant
		self.reward_decay = reward_decay
		self.from_move = from_move

	def search(self):
		simulation_count = 0
		start_time = time()
		#past_nodes = []
		while simulation_count < self.simulation_limit:
			# print("simulation_count:", simulation_count)
			next_node = self.pick_next_node(self.exploration_constant)
			reward = next_node.rollout()
			next_node.backup(reward)
			simulation_count += 1
			#past_nodes.append(next_node)
		# self.print('')
		# code.interact(local=locals())
		# print(f"Number of sumulation: {simulation_count}")
		print("=================")
		for move in self.expanded_children:
			print(move, self.expanded_children[move].reward, self.expanded_children[move].visit_count)
		return self.best_UCB_child(0)

	def expand_last_move(self):
		move = self.possible_move_list.pop()

		new_child = self.create_from_move(move)
		self.expanded_children[move] = new_child
		return new_child

	def best_UCB_child(self, exploration_constant):
		def ucb(n):
			return n.reward/n.visit_count + exploration_constant*math.sqrt(2*math.log(self.visit_count)/n.visit_count)
		return max(self.expanded_children.values(), key=ucb)

	def pick_next_node(self, exploration_constant):
		if self.is_terminal():
			return self

		if self.possible_move_list is None:
			self.possible_move_list = self.get_all_possible_moves()
			random.shuffle(self.possible_move_list)

		if self.possible_move_list:
			return self.expand_last_move()

		#code.interact(local=locals())
		return self.best_UCB_child(exploration_constant).pick_next_node(exploration_constant)

	def backup(self, reward):
		self.visit_count += 1
		self.reward += reward
		if self.parent is not None:
			self.parent.backup(-reward*self.reward_decay)

	def sorted_UCB_child(self, exploration_constant):
		def ucb(n):
			return n.reward/n.visit_count + exploration_constant*math.sqrt(2*math.log(self.visit_count)/n.visit_count)
		return sorted(self.expanded_children.values(), key=ucb, reverse=True)

	def print(self, prefix):
		print(prefix + f"visit_count: {self.visit_count} reward: {self.reward} score: {self.reward/self.visit_count}")
		for child in self.sorted_UCB_child(0):
			child.print(prefix + f"    {child.from_move%7+1} {child.from_move//7+1} ")

	def create_from_move(self, move):
		pass

	def rollout(self):
		pass

	def get_all_possible_moves(self):
		pass

	def is_terminal(self):
		pass
