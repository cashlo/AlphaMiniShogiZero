from enum import Enum, auto
from collections import defaultdict
import random

class MiniShogi:
	SIZE = 5
	class Game():
		def __init__(self):
			self.player_kings = [
				MiniShogi.Piece(MiniShogi.PieceType.KING, 4, 0, False, 0),
				MiniShogi.Piece(MiniShogi.PieceType.KING, 0, 4, False, 1)
			]
			self.current_player = 1
			self.player_pieces = [[], []]
			self.board = MiniShogi.Board(MiniShogi.SIZE)
			
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   0, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, 1, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, 2, 0, False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   3, 0, False, 0))
			self.place_piece(self.player_kings[0])
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   4, 1, False, 0))

			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   4, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, 3, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, 2, 4, False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   1, 4, False, 1))
			self.place_piece(self.player_kings[1])
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   0, 3, False, 1))

		def place_piece(self, piece):
			self.player_pieces[piece.player].append(piece)
			self.board.place_piece(piece)

		def make_move(self, piece, move):
			print("game.make_move", piece, move)
			player = piece.player
			capturing_piece = self.board.piece_at(move)
			if capturing_piece is not None:
				self.player_pieces[capturing_piece.player].remove(capturing_piece)
				capturing_piece.promoted = False
				capturing_piece.player = player
				capturing_piece.position = None
				self.player_pieces[player].append(capturing_piece)
			self.board.make_move(piece, move)
			self.current_player = 1-self.current_player

		def random_move(self):
			move_options = []
			move_dict = self.all_legal_moves(self.current_player)
			for p in move_dict:
				move_options.extend( (p, m) for m in move_dict[p] )
			return random.sample(move_options, 1)[0]

		def check_game_over(self):
			if len(self.all_legal_moves(self.current_player)) == 0:
				return 1-self.current_player
			for king in self.player_kings:
				if king.position is None:
					return king.player
			return None

		def player_attack_area(self, player):
			area = set()
			for piece in self.player_pieces[player]:
				if piece.position is not None:
					area.update(piece.get_moves(self.board))
			return area

		def king_attacking_pieces(self, player):
			other_player = 1-player

			king_attacking_pieces = set()

			for p in self.player_pieces[other_player]:
				attacking_moves = p.get_moves(self.board)
				if self.player_kings[player].position in attacking_moves:
					king_attacking_pieces.add(p)
			return king_attacking_pieces



		def all_legal_moves(self, player):
			other_player = 1-player
			player_king = self.player_kings[player]
			king_attacking_pieces = self.king_attacking_pieces(player)
			other_player_attack_area_set = self.player_attack_area(other_player)

			possible_moves = defaultdict(set)
			if king_attacking_pieces:
				king_move_set = set(player_king.get_moves(self.board))
				if king_move_set - other_player_attack_area_set:
					possible_moves[player_king].update(king_move_set - other_player_attack_area_set)
				if len(king_attacking_pieces) > 1:
					return possible_moves
				king_attacking_piece = list(king_attacking_pieces)[0]
				for p in self.player_pieces[player]:
					if p == player_king:
						continue
					moves = p.get_moves(self.board)
					for m in moves:
						if m == king_attacking_piece.position or m in self.board.between(player_king, king_attacking_piece):
							possible_moves[p].add(m)
				return possible_moves
			else:
				for p in self.player_pieces[player]:
					if p == player_king:
						possible_moves[p].update( p.get_moves(self.board) - other_player_attack_area_set )
					else:
						possible_moves[p].update( p.get_moves(self.board) )
				return possible_moves
			


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

		def make_move(self, piece, move):
			print("board.make_move", piece, move)
			player = piece.player
			if piece.position is not None:
				self.board[piece.position[0]][piece.position[1]] = None
			self.board[move[0]][move[1]] = piece
			piece.position = move
			piece.promoted = piece.promoted or move[2]

		def between(self, piece1, piece2):
			position1 = piece1.position
			position2 = piece2.position

			directions = [(-1,-1), (-1,0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
			for d in directions:
				line_between = set()
				new_position = ( position1[0], position1[1] )
				while new_position := ( new_position[0] + d[0], new_position[1] + d[1] ):
					if not self.is_position_on_board(new_position):
						break
					if new_position == position2:
						return line_between
					line_between.add(new_position)
			raise ValueError('Not on a line')



		# def check_board(self, current_player):
		# 	other_player = 1-current_player

		# 	king_attacking_pieces = []

		# 	for p in self.player_pieces[other_player]:
		# 		if self.player_kings[current_player].position in p.get_moves(self):
		# 			king_attacking_pieces.append(p)

		# 	if not king_attacking_pieces:
		# 		return (MiniShogi.State.IN_PROGRESS, None)

		# 	other_player_attack_area_set = set(self.player_attack_area(other_player))
		# 	current_player_attack_area_set = set(self.player_attack_area(other_player))

		# 	if set(self.player_kings[current_player].get_moves(self)) - other_player_attack_area_set:
		# 		return (MiniShogi.State.IN_PROGRESS, None)
		# 	if len(king_attacking_pieces) == 1:
		# 		if king_attacking_pieces[0].position in current_player_attack_area_set:
		# 			return (MiniShogi.State.IN_PROGRESS, None)
		# 		if self.between(
		# 				self.player_kings[current_player].position,
		# 				king_attacking_pieces[0].position
		# 			).intersection(current_player_attack_area_set):
		# 			return (MiniShogi.State.IN_PROGRESS, None)
		# 	return (MiniShogi.State.CHECKMATE, other_player)

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

		def get_name(self):
			if not self.promoted:
				return self.pieceType.value
			else:
				if self.pieceType == MiniShogi.PieceType.PAWN:
					return 'と'
				return self.pieceType.promotion().value

		def get_moves(self, board):
			valid_moves = set()
			if self.position is None:
				if self.pieceType != MiniShogi.PieceType.PAWN:
					for f in range(MiniShogi.SIZE):
						for r in range(MiniShogi.SIZE):
							if board.piece_at( (f, r) ) is None:
								valid_moves.add( (f, r, False) )
					return valid_moves
				else:
					# TODO: Pawn drop
					pass
				return valid_moves

			moveType = self.pieceType.promotion() if self.promoted else self.pieceType
			

			for m in moveType.short_moves():
				if self.player == 0:
					m = (m[0], -m[1])
				new_position = ( self.position[0] + m[0], self.position[1] + m[1], False )
				if not board.is_position_on_board(new_position):
					continue
				if board.piece_at(new_position) != None and self.player == board.piece_at(new_position).player:
					continue
				valid_moves.add(new_position)

				# Promotion option
				if (self.player == 0 and new_position[1] == 4) or (self.player == 1 and new_position[1] == 0):
					if self.pieceType == MiniShogi.PieceType.PAWN:
						valid_moves.remove( new_position )
					valid_moves.add( (new_position[0], new_position[1], True) )

			for m in moveType.long_moves():
				new_position = ( self.position[0], self.position[1], False )
				while new_position := ( new_position[0] + m[0], new_position[1] + m[1], False ):
					if not board.is_position_on_board(new_position):
						break
					capturing_piece = board.piece_at(new_position)
					if capturing_piece != None and capturing_piece.player == self.player:
						break
					valid_moves.add(new_position)

					# Promotion option
					if (self.player == 0 and new_position[1] == 4) or (self.player == 1 and new_position[1] == 0):
						if self.pieceType == MiniShogi.PieceType.PAWN:
							valid_moves.remove( new_position )
						valid_moves.add( (new_position[0], new_position[1], True) )

					if capturing_piece != None:
						break
					
			return valid_moves

	class State(Enum):
		IN_PROGRESS	= auto()
		CHECKMATE   = auto()
		

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
				MiniShogi.PieceType.GOLD: [(-1,-1), (0,-1), (1, -1), (-1, 0), (1, 0), (0, 1)],
				MiniShogi.PieceType.SILVER: [(-1,-1), (0,-1), (1, -1), (-1, 1), (1, 1)],
				MiniShogi.PieceType.PAWN: [(0, -1)],
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

