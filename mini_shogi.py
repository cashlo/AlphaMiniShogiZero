from enum import Enum, auto
from collections import defaultdict
import random
import code

class MiniShogi:
	SIZE = 5
	class Game():
		def __init__(self):
			self.player_kings = [None, None]
			self.current_player = 1
			self.player_pieces = [[], []]
			self.board = MiniShogi.Board(MiniShogi.SIZE)
		
		def setup(self):
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   (0, 0), False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (1, 0), False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, (2, 0), False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   (3, 0), False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 0), False, 0))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (4, 1), False, 0))

			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.ROOK,   (4, 4), False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (3, 4), False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.SILVER, (2, 4), False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.GOLD,   (1, 4), False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 4), False, 1))
			self.place_piece(MiniShogi.Piece(MiniShogi.PieceType.PAWN,   (0, 3), False, 1))


		def board_check(self):
			return
			for player, pieces in enumerate(self.player_pieces):
				for p in pieces:
					if p.position is not None:
						if self.board.piece_at(p.position) is not p:
							self.print()
							print(p.position)
							raise ValueError('board mismatch!')

		def print(self):
			for player, pieces in enumerate(self.player_pieces):
				print("Player", player)
				for p in pieces:
					print(p.get_name(), p.position)
			
			self.board.print()

		def clone(self):
			clone_game = MiniShogi.Game()
			for player, pieces in enumerate(self.player_pieces):
				for p in pieces:
					clone_game.place_piece(p.clone())
			clone_game.current_player = self.current_player
			return clone_game

		def place_piece(self, piece):
			self.player_pieces[piece.player].append(piece)
			if piece.pieceType == MiniShogi.PieceType.KING:
				self.player_kings[piece.player] = piece
			if piece.position is not None:
				self.board.place_piece(piece)

		def make_move(self, move):
			piece_type, old_position, new_position, promoted = move
			
			piece = None
			for p in self.player_pieces[self.current_player]:
				if p.pieceType == piece_type and p.position == old_position:
					piece = p
					break

			if piece is None:
				raise ValueError('Piece not found!')

			if self.current_player != piece.player:
				raise ValueError('Not your piece!')
			player = piece.player
			capturing_piece = self.board.piece_at(new_position)
			if capturing_piece is not None:
				if capturing_piece.player == piece.player:
					print(piece.get_name())
					print(move)
					self.print()
					raise ValueError('Capture own piece!')
			
				self.player_pieces[capturing_piece.player].remove(capturing_piece)
				capturing_piece.promoted = False
				capturing_piece.player = player
				capturing_piece.position = None
				self.player_pieces[player].append(capturing_piece)
			self.board.make_move(piece, new_position, promoted)
			self.current_player = 1-self.current_player
			

		def all_legal_move_list(self):
			return list(self.all_legal_moves(self.current_player))

		def random_move(self):
			return random.sample(self.all_legal_move_list(), 1)[0]

		def check_game_over(self):
			for player, king in enumerate(self.player_kings):
				if king is None:
					return 1-player
				if king.position is None:
					return 1-player
			if len(self.all_legal_move_list()) == 0:
				return 1-self.current_player
			return None

		def king_attacking_pieces(self, player):
			other_player = 1-player

			king_attacking_pieces = set()

			for p in self.player_pieces[other_player]:
				attacking_moves = p.get_moves(self.board, True)
				if self.player_kings[player].position in attacking_moves:
					king_attacking_pieces.add(p)
			return king_attacking_pieces



		def all_legal_moves(self, player):
			other_player = 1-player
			player_king = self.player_kings[player]
			king_attacking_pieces = self.king_attacking_pieces(player)
			other_player_attack_area_set = self.board.player_attack_area(other_player, player_king)

			possible_moves = set()
			if king_attacking_pieces:
				king_move_set = set(player_king.get_moves(self.board, True))
				king_move_set -= other_player_attack_area_set
				if king_move_set:
					possible_moves.update({ (player_king.pieceType, player_king.position, m, False) for m in king_move_set })
				if len(king_attacking_pieces) > 1:
					return possible_moves
				king_attacking_piece = list(king_attacking_pieces)[0]
				for p in self.player_pieces[player]:
					if p == player_king:
						continue
					moves = p.get_moves(self.board)
					for m in moves:
						if (m[0], m[1]) == king_attacking_piece.position or (m[0], m[1]) in self.board.between(player_king, king_attacking_piece):
							possible_moves.add( (p.pieceType, p.position, (m[0], m[1]), m[2]) )

				return possible_moves
			else:
				for p in self.player_pieces[player]:
					if p == player_king:
						move_set = p.get_moves(self.board, True)
						move_set -= other_player_attack_area_set
						possible_moves.update({ (p.pieceType, p.position, m, False) for m in move_set })
					else:
						possible_moves.update({ (p.pieceType, p.position, (m[0], m[1]), m[2]) for m in p.get_moves(self.board) })
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

		def player_attack_area(self, player, ignore_piece = None, skip_piece = None):
			area = set()

			for f in range(MiniShogi.SIZE):
				for r in range(MiniShogi.SIZE):
					board_piece = self.piece_at( (f, r) )
					if board_piece is None:
						continue
					if board_piece.player != player:
						continue
					if board_piece == skip_piece:
						continue
					area.update(board_piece.get_moves(self, True, ignore_piece))
			return area

		def make_move(self, piece, new_position, promoted):
			player = piece.player
			if piece.position is not None:
				self.board[piece.position[0]][piece.position[1]] = None
			self.board[new_position[0]][new_position[1]] = piece
			piece.position = (new_position[0], new_position[1])
			piece.promoted = piece.promoted or promoted

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
			code.interact(local=locals())
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
		def __init__(self, pieceType, position, promoted: bool, player: int):
			self.pieceType = pieceType
			self.position = position
			self.promoted = promoted
			self.player = player

		def clone(self):
			return MiniShogi.Piece(self.pieceType, self.position, self.promoted, self.player)

		def get_name(self):
			if not self.promoted:
				return self.pieceType.value
			else:
				if self.pieceType == MiniShogi.PieceType.PAWN:
					return 'と'
				return self.pieceType.promotion().value

		def pawn_drop_checkmate(self, drop_position, board):
			if self.player == 0:
				check_positon = (drop_position[0], drop_position[1]+1)
			else:
				check_positon = (drop_position[0], drop_position[1]-1)
			check_piece = board.piece_at( check_positon )
			if check_piece is None:
				return False
			if check_piece.pieceType != MiniShogi.PieceType.KING:
				return False

			player_attack_area = board.player_attack_area(self.player)
			if check_piece.get_moves(board, True) - player_attack_area:
				# print("Their king can move")
				return False
			if drop_position in board.player_attack_area(1-self.player, skip_piece=check_piece):
				# print("The drop pawn can be taken their other pieces")
				return False
			if drop_position not in player_attack_area:
				# print("The pawn can be taken by their king")
				return False
			return True


		def get_moves(self, board, position_only = False, ignore_piece = None):
			valid_moves = set()
			if self.position is None:
				if self.pieceType != MiniShogi.PieceType.PAWN:
					for f in range(MiniShogi.SIZE):
						for r in range(MiniShogi.SIZE):
							if board.piece_at( (f, r) ) is None:
								valid_moves.add( (f, r, False) )
				else:
					no_drop_ranks = set()
					no_drop_files = set()
					if self.player == 0:
						no_drop_ranks.add(4)
					else:
						no_drop_ranks.add(0)

					for f in range(MiniShogi.SIZE):
						for r in range(MiniShogi.SIZE):
							board_piece = board.piece_at( (f, r) )
							if board_piece is None:
								continue
							if board_piece.pieceType == MiniShogi.PieceType.PAWN and board_piece.player == self.player:
								no_drop_files.add(f)

					for f in range(MiniShogi.SIZE):
						if f in no_drop_files:
							continue
						for r in range(MiniShogi.SIZE):
							if r in no_drop_ranks:
								continue
							if board.piece_at( (f, r) ) is None and not self.pawn_drop_checkmate((f, r), board):
								valid_moves.add( (f, r, False) )
				if position_only:
					return { (m[0], m[1]) for m in valid_moves}
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

					if capturing_piece is not None and capturing_piece != ignore_piece:
						break
					
			if position_only:
				return { (m[0], m[1]) for m in valid_moves}
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

