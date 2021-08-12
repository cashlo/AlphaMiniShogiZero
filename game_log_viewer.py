import pickle
from mini_shogi import MiniShogi
from gamewindow import GameWindow
import numpy as np

def last_move(event):
	global index
	index -= 1
	game_log_x = np.moveaxis(game_log['x'][index], -1, 0)
	print(game_log['y'][1][index])
	show_game_log(window, game_log_x.tolist())

def next_move(event):
	global index
	index += 1
	game_log_x = np.moveaxis(game_log['x'][index], -1, 0)
	print(game_log['y'][1][index])
	show_game_log(window, game_log_x.tolist())

window = GameWindow("Game log viewer")
window.window.bind('<Left>', last_move)
window.window.bind('<Right>', next_move)
index = 0
game_log = pickle.loads(open('game_log_minishogi_10.pickle', "rb").read())

def place_piece_from_plane(game, plane, pieceType, promoted, player):
	for f in range(MiniShogi.SIZE):
		for r in range(MiniShogi.SIZE):
			if plane[f][r] == 1:
				game.place_piece( MiniShogi.Piece(pieceType,   (f, r), False, player) )


def show_game_log(window, encoded_input):
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



game_log_x = np.moveaxis(game_log['x'][index], -1, 0)
print(game_log['y'][1][index])
show_game_log(window, game_log_x.tolist())
window.mainloop()