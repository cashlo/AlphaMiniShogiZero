from mini_shogi import MiniShogi
import unittest

class TestMiniShogi(unittest.TestCase):
	def test_board_hash(self):
		game = MiniShogi.Game()
		game.setup()
		self.assertEqual(game.board.to_tuple(), (
			((MiniShogi.PieceType.ROOK, (0, 0), False, 0), None, None, (MiniShogi.PieceType.PAWN, (0, 3), False, 1), (MiniShogi.PieceType.KING, (0, 4), False, 1)),
			((MiniShogi.PieceType.BISHOP, (1, 0), False, 0), None, None, None, (MiniShogi.PieceType.GOLD, (1, 4), False, 1)),
			((MiniShogi.PieceType.SILVER, (2, 0), False, 0), None, None, None, (MiniShogi.PieceType.SILVER, (2, 4), False, 1)),
			((MiniShogi.PieceType.GOLD, (3, 0), False, 0), None, None, None, (MiniShogi.PieceType.BISHOP, (3, 4), False, 1)),
			((MiniShogi.PieceType.KING, (4, 0), False, 0), (MiniShogi.PieceType.PAWN, (4, 1), False, 0), None, None, (MiniShogi.PieceType.ROOK, (4, 4), False, 1))
		))

	def test_no_repeating_move_ever(self):
		game = MiniShogi.Game()
		game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (0, 0), False, 0))
		game.place_piece(MiniShogi.Piece(MiniShogi.PieceType.KING,   (4, 4), False, 1))

		self.assertListEqual( sorted(game.all_legal_move_list()), [(MiniShogi.PieceType.KING, (4, 4), (3, 3), False), (MiniShogi.PieceType.KING, (4, 4), (3,4), False), (MiniShogi.PieceType.KING, (4, 4), (4, 3), False)] )

		game.make_move( (MiniShogi.PieceType.KING, (4, 4), (4, 3), False) )
		game.make_move( (MiniShogi.PieceType.KING, (0, 0), (0, 1), False) )
		game.make_move( (MiniShogi.PieceType.KING, (4, 3), (4, 4), False) )
		game.make_move( (MiniShogi.PieceType.KING, (0, 1), (0, 0), False) )		

		self.assertListEqual( sorted(game.all_legal_move_list()), [(MiniShogi.PieceType.KING, (4, 4), (3, 3), False), (MiniShogi.PieceType.KING, (4, 4), (3,4), False)] )

		game = game.clone()
		self.assertListEqual( sorted(game.all_legal_move_list()), [(MiniShogi.PieceType.KING, (4, 4), (3, 3), False), (MiniShogi.PieceType.KING, (4, 4), (3,4), False)] )

	def test_promotion_moves(self):
		game = MiniShogi.Game()
		test_piece_1 = MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (4, 4), False, 1)
		game.place_piece(test_piece_1)
		self.assertListEqual(sorted(test_piece_1.get_moves(game.board)), [(0, 0, False), (0, 0, True), (1, 1, False), (2, 2, False), (3, 3, False)])

		game = MiniShogi.Game()
		test_piece_2 = MiniShogi.Piece(MiniShogi.PieceType.BISHOP, (3, 0), False, 1)
		game.place_piece(test_piece_2)
		self.assertListEqual(sorted(test_piece_2.get_moves(game.board)), [
			(0, 3, False),(0, 3, True),
			(1, 2, False),(1, 2, True),
			(2, 1, False),(2, 1, True),
			(4, 1, False),(4, 1, True)
		])

		game = MiniShogi.Game()
		test_piece_3 = MiniShogi.Piece(MiniShogi.PieceType.SILVER, (0, 1), False, 1)
		game.place_piece(test_piece_3)
		self.assertListEqual(sorted(test_piece_3.get_moves(game.board)), [(0, 0, False), (0, 0, True), (1, 0, False), (1, 0, True), (1, 2, False)])

		game = MiniShogi.Game()
		test_piece_4 = MiniShogi.Piece(MiniShogi.PieceType.SILVER, (1, 0), False, 1)
		game.place_piece(test_piece_4)
		self.assertListEqual(sorted(test_piece_4.get_moves(game.board)), [(0, 1, False), (0, 1, True), (2, 1, False), (2, 1, True)])

		game = MiniShogi.Game()
		test_piece_5 = MiniShogi.Piece(MiniShogi.PieceType.SILVER, (1, 0), False, 0)
		game.place_piece(test_piece_5)
		self.assertListEqual(sorted(test_piece_5.get_moves(game.board)), [(0, 1, False), (1, 1, False), (2, 1, False)])







