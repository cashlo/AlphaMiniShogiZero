from monte_carlo_tree_search import Node

class MiniShogiSearchTree(Node):
	def __init__(self, game, parent=None, from_move=None, gui=None):
		Node.__init__(self, parent=parent, from_move=from_move)
		self.game = game
		self.gui = gui

	def rollout(self):
		simulation_game = self.game.clone()

		move_count = 0
		while simulation_game.check_game_over() is None:
			move = simulation_game.random_move()
			# print("move_count: ", move_count)
			simulation_game.board_check()
			simulation_game.make_move(move)
			if self.gui:
				gui.draw_board(simulation_game)
			simulation_game.board_check()
			if move_count > 100:
				return 0
			move_count += 1
		winner = simulation_game.check_game_over()
		return -1 if self.game.current_player == winner else 1

	def create_from_move(self, move):
		# print("create_from_move: ", move)
		if move in self.expanded_children:
			return self.expanded_children[move]

		self.game.board_check()
		new_game = self.game.clone()
		new_game.make_move(move)
		return MiniShogiSearchTree(new_game, self, from_move=move)

	def get_all_possible_moves(self):
		return self.game.all_legal_move_list()

	def is_terminal(self):
		return self.game.check_game_over() is not None

