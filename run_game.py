from gamewindow import GameWindow
from mini_shogi import MiniShogi

window = GameWindow("Mini Shogi")

game = MiniShogi.Game()

window.draw_board(game.board)

p0_all_moves = game.all_possible_moves(0)
p1_all_moves = game.all_possible_moves(1)


for p in p0_all_moves:
	print(p.pieceType.value)
	window.draw_moves(p0_all_moves[p])
	input()


for p in p1_all_moves:
	print(p.pieceType.value)
	window.draw_moves(p1_all_moves[p])
	input()

window.mainloop()