from gamewindow import GameWindow
from mini_shogi import MiniShogi
from mini_shogi_search_tree import MiniShogiSearchTree


def setup_puzzle1():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 2), False, 0))

	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   None  , False, 1))
	return game


def setup_puzzle2():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (3, 0), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   (4, 0), False, 0))


	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (1, 1), True, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,     None, False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER,   None, False, 1))
	return game

def setup_puzzle3():
	game = MiniShogi.Game()
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (2, 1), False, 0))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   (3, 1), False, 0))


	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (0, 2), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (1, 3), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (2, 3), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (3, 3), False, 1))
	game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,     None, False, 1))
	
	return game


game = setup_puzzle3()

window = GameWindow("Puzzle 1")

window.draw_board(game)

search_tree = MiniShogiSearchTree(game.clone())

search_tree = search_tree.search()
move = search_tree.from_move
game.make_move(move)
window.draw_board(game)


window.mainloop()