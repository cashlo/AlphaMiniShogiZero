from gamewindow import GameWindow
from mini_shogi import MiniShogi
import time
from mini_shogi_search_tree import MiniShogiSearchTree


game = MiniShogi.Game()
game.setup()

sim_window = None # GameWindow("Simulation")
search_tree = MiniShogiSearchTree(game.clone(), gui=sim_window)

last_clicked_piece = None
def on_click(x, y, promotion):
	winner = game.check_game_over()
	if winner is not None:
		print("Winner is ", winner)
		return
	if not game.board.is_position_on_board( (x, y) ):
		p = GameWindow.capture_position_to_piece(game, (x, y))
	else:
		p = game.board.piece_at( (x, y) )
	global last_clicked_piece
	global search_tree

	if p is None or (last_clicked_piece and p.player != last_clicked_piece.player):
		if last_clicked_piece is not None:
			player = last_clicked_piece.player
			legal_moves = game.all_legal_moves(last_clicked_piece.player)
			clicked_move = (last_clicked_piece.pieceType, last_clicked_piece.position, (x, y), promotion)
			if clicked_move in legal_moves:
				game.make_move(clicked_move)
				search_tree = search_tree.create_from_move( clicked_move )
				window.draw_board(game)
				winner = game.check_game_over()
				if winner is not None:
					print("Winner is ", winner)
					return
	
				search_tree = search_tree.search()
				move = search_tree.from_move
				game.make_move(move)
				window.draw_board(game)
			last_clicked_piece = None
		return

	if p.player == 0:
	 	return
	last_clicked_piece = p
	legal_moves = game.all_legal_moves(p.player)
	# print(legal_moves)
	window.draw_moves(legal_moves, p)

def make_random_move():
	winner = game.check_game_over()
	if winner is None:
		move = game.random_move()
		game.make_move(move)
		window.draw_board(game)
		window.window.after(1, make_random_move)
	else:
		print("Winner: ", winner)

window = GameWindow("Mini Shogi", on_click=on_click)

window.draw_board(game)
# window.window.after(1, make_random_move)

				

window.mainloop()