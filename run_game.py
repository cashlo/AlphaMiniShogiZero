from gamewindow import GameWindow
from mini_shogi import MiniShogi


game = MiniShogi.Game()

last_clicked_piece = None
def on_click(x, y):
	if not game.board.is_position_on_board( (x, y) ):
		p = GameWindow.capture_position_to_piece(game, (x, y))
	else:
		p = game.board.piece_at( (x, y) )
	global last_clicked_piece

	if p is None or (last_clicked_piece and p.player != last_clicked_piece.player):
		if last_clicked_piece is not None:
			player = last_clicked_piece.player
			legal_moves = game.all_legal_moves(last_clicked_piece.player)
			if (x, y) in legal_moves[last_clicked_piece]:
				game.make_move(last_clicked_piece, (x, y))
				window.draw_board(game)
			last_clicked_piece = None
		return

	if p.player == 0:
		return
	last_clicked_piece = p
	legal_moves = game.all_legal_moves(p.player)
	print(legal_moves[p])
	window.draw_moves(legal_moves[p])

window = GameWindow("Mini Shogi", on_click=on_click)

window.draw_board(game)

window.mainloop()