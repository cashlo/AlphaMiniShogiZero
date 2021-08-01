from enum import Enum

class MiniShogi:
	class Piece(Enum):
		KING   = '王'
		ROOK   = '飛'
		BISHOP = '角'
		GOLD   = '金'
		SILVER = '銀'
		PAWN   = '歩'

		DRAGON = '龍'
		HORSE  = '馬'

		def short_moves(self):
			return {
				MiniShogi.Piece.KING: [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)],
				MiniShogi.Piece.ROOK: [],
				MiniShogi.Piece.BISHOP: [],
				MiniShogi.Piece.GOLD: [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,0)],
				MiniShogi.Piece.SILVER: [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,-1), (1,1)],
				MiniShogi.Piece.PAWN: [(-1, 0)],
				MiniShogi.Piece.DRAGON: [(-1,-1), (-1, 1), (1,-1), (1,1)],
				MiniShogi.Piece.HORSE: [(-1,0), (0,-1), (0,1), (1,0)]
			}[self]

		def long_moves(self):
			return {
				MiniShogi.Piece.KING: [],
				MiniShogi.Piece.ROOK: [(-1,0), (0,-1), (0,1), (1,0)],
				MiniShogi.Piece.BISHOP: [(-1,-1), (-1, 1), (1,-1), (1,1)],
				MiniShogi.Piece.GOLD: [],
				MiniShogi.Piece.SILVER: [],
				MiniShogi.Piece.PAWN: [],
				MiniShogi.Piece.DRAGON: [(-1,0), (0,-1), (0,1), (1,0)],
				MiniShogi.Piece.HORSE: [(-1,-1), (-1, 1), (1,-1), (1,1)]
			}[self]

		def promotion(self):
			return {
				MiniShogi.Piece.KING: MiniShogi.Piece.KING,
				MiniShogi.Piece.ROOK: MiniShogi.Piece.DRAGON,
				MiniShogi.Piece.BISHOP: MiniShogi.Piece.HORSE,
				MiniShogi.Piece.GOLD: MiniShogi.Piece.GOLD,
				MiniShogi.Piece.SILVER: MiniShogi.Piece.GOLD,
				MiniShogi.Piece.PAWN: MiniShogi.Piece.GOLD,
				MiniShogi.Piece.DRAGON: MiniShogi.Piece.DRAGON,
				MiniShogi.Piece.HORSE: MiniShogi.Piece.HORSE
			}[self]

	SIZE = 5


print(MiniShogi.Piece.KING.get_short_move())