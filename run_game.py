from gamewindow import GameWindow
from mini_shogi import MiniShogi
import time


game = MiniShogi.Game()

last_clicked_piece = None
def on_click(x, y, promotion):
	if not game.board.is_position_on_board( (x, y) ):
		p = GameWindow.capture_position_to_piece(game, (x, y))
	else:
		p = game.board.piece_at( (x, y) )
	global last_clicked_piece

	if p is None or (last_clicked_piece and p.player != last_clicked_piece.player):
		if last_clicked_piece is not None:
			player = last_clicked_piece.player
			legal_moves = game.all_legal_moves(last_clicked_piece.player)
			if (x, y, promotion) in legal_moves[last_clicked_piece]:
				game.make_move(last_clicked_piece, (x, y, promotion))
				window.draw_board(game)
				piece, move = game.random_move()
				game.make_move(piece, move)
				window.draw_board(game)
				
			last_clicked_piece = None
		return

	if p.player == 0:
		return
	last_clicked_piece = p
	legal_moves = game.all_legal_moves(p.player)
	print(legal_moves[p])
	window.draw_moves(legal_moves[p])

def make_random_move():
	winner = game.check_game_over()
	if winner is None:
		piece, move = game.random_move()
		game.make_move(piece, move)
		window.draw_board(game)
		window.window.after(1, make_random_move)
	else:
		print("Winner: ", winner)

window = GameWindow("Mini Shogi", on_click=on_click)

window.draw_board(game)
# window.window.after(1, make_random_move)

				

window.mainloop()