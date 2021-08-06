from enum import Enum

class MiniShogi:
	SIZE = 5
	class Game():
		def __init__(self):
			self.player_pieces = [[], []]
			self.board = MiniShogi.Board(MiniShogi.SIZE)
			
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   0, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, 1, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, 2, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   3, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   4, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   4, 1, False, 0))

			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   4, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, 3, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, 2, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   1, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   0, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   0, 3, False, 1))

		def place_piece(self, piece):
			self.player_pieces[piece.player].append(piece)
			self.board.place_piece(piece)



	class Board():
		def __init__(self, size: int):
			self.size = size
			self.board = [ [None]*size for i in range(size) ]

		def is_position_on_board(self, position):
			if position[0] < 0 or position[1]< 0:
				return False
			if position[0] >= self.size or position[1] >= self.size:
				return False
			return True 

		def piece_at(self, position):
			return self.board[position[0]][position[1]]

		def place_piece(self, piece):
			self.board[piece.position[0]][piece.position[1]] = piece

		def print(self):
			ranks = ['']*self.size
			for file in self.board:
				for i, piece in enumerate(file):
					if piece != None:
						ranks[i] += piece.pieceType.value
					else:
						ranks[i] += '  '
			for r in ranks:
				print(r)

	class Piece():
		def __init__(self, pieceType, x: int, y: int, promoted: bool, player: int):
			self.pieceType = pieceType
			self.position = (x, y)
			self.promoted = promoted
			self.player = player

		def get_moves(self, board):
			moveType = self.pieceType.promotion() if self.promoted else self.pieceType
			valid_moves = []

			for m in moveType.short_moves():
				new_position = ( self.position[0] + m[0], self.position[1] + m[1] )
				if not board.is_position_on_board(new_position):
					continue
				if board.piece_at(new_position) != None and self.player == board.piece_at(new_position).player:
					continue
				valid_moves.append(new_position)

			for m in moveType.long_moves():
				new_position = ( self.position[0], self.position[1] )
				while new_position := ( new_position[0] + m[0], new_position[1] + m[1] ):
					if not board.is_position_on_board(new_position):
						break
					if board.piece_at(new_position) != None:
						if self.player != board.piece_at(new_position).player:
							valid_moves.append(new_position)
						break
					valid_moves.append(new_position)

			return valid_moves		



	class PieceType(Enum):
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
				MiniShogi.PieceType.KING: [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)],
				MiniShogi.PieceType.ROOK: [],
				MiniShogi.PieceType.BISHOP: [],
				MiniShogi.PieceType.GOLD: [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,0)],
				MiniShogi.PieceType.SILVER: [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,-1), (1,1)],
				MiniShogi.PieceType.PAWN: [(-1, 0)],
				MiniShogi.PieceType.DRAGON: [(-1,-1), (-1, 1), (1,-1), (1,1)],
				MiniShogi.PieceType.HORSE: [(-1,0), (0,-1), (0,1), (1,0)]
			}[self]

		def long_moves(self):
			return {
				MiniShogi.PieceType.KING: [],
				MiniShogi.PieceType.ROOK: [(-1,0), (0,-1), (0,1), (1,0)],
				MiniShogi.PieceType.BISHOP: [(-1,-1), (-1, 1), (1,-1), (1,1)],
				MiniShogi.PieceType.GOLD: [],
				MiniShogi.PieceType.SILVER: [],
				MiniShogi.PieceType.PAWN: [],
				MiniShogi.PieceType.DRAGON: [(-1,0), (0,-1), (0,1), (1,0)],
				MiniShogi.PieceType.HORSE: [(-1,-1), (-1, 1), (1,-1), (1,1)]
			}[self]

		def promotion(self):
			return {
				MiniShogi.PieceType.KING: MiniShogi.PieceType.KING,
				MiniShogi.PieceType.ROOK: MiniShogi.PieceType.DRAGON,
				MiniShogi.PieceType.BISHOP: MiniShogi.PieceType.HORSE,
				MiniShogi.PieceType.GOLD: MiniShogi.PieceType.GOLD,
				MiniShogi.PieceType.SILVER: MiniShogi.PieceType.GOLD,
				MiniShogi.PieceType.PAWN: MiniShogi.PieceType.GOLD,
				MiniShogi.PieceType.DRAGON: MiniShogi.PieceType.DRAGON,
				MiniShogi.PieceType.HORSE: MiniShogi.PieceType.HORSE
			}[self]

