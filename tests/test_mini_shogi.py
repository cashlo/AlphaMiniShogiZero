from mini_shogi import MiniShogi
import unittest

class TestMiniShogi(unittest.TestCase):
	def test_board_hash(self):
		game = MiniShogi.Game()
		game.setup()
		(
			((MiniShogi.PieceType.ROOK, (0, 0), False, 0), None, None, (MiniShogi.PieceType.PAWN, (0, 3), False, 1), (MiniShogi.PieceType.KING, (0, 4), False, 1)),
			((MiniShogi.PieceType.BISHOP, (1, 0), False, 0), None, None, None, (MiniShogi.PieceType.GOLD, (1, 4), False, 1)),
			((MiniShogi.PieceType.SILVER, (2, 0), False, 0), None, None, None, (MiniShogi.PieceType.SILVER, (2, 4), False, 1)),
			((MiniShogi.PieceType.GOLD, (3, 0), False, 0), None, None, None, (MiniShogi.PieceType.BISHOP, (3, 4), False, 1)),
			((MiniShogi.PieceType.KING, (4, 0), False, 0), (MiniShogi.PieceType.PAWN, (4, 1), False, 0), None, None, (MiniShogi.PieceType.ROOK, (4, 4), False, 1))
		)
		self.assertEqual(game.board.to_tuple(), (
			((MiniShogi.PieceType.ROOK, (0, 0), False, 0), None, None, (MiniShogi.PieceType.PAWN, (0, 3), False, 1), (MiniShogi.PieceType.KING, (0, 4), False, 1)),
			((MiniShogi.PieceType.BISHOP, (1, 0), False, 0), None, None, None, (MiniShogi.PieceType.GOLD, (1, 4), False, 1)),
			((MiniShogi.PieceType.SILVER, (2, 0), False, 0), None, None, None, (MiniShogi.PieceType.SILVER, (2, 4), False, 1)),
			((MiniShogi.PieceType.GOLD, (3, 0), False, 0), None, None, None, (MiniShogi.PieceType.BISHOP, (3, 4), False, 1)),
			((MiniShogi.PieceType.KING, (4, 0), False, 0), (MiniShogi.PieceType.PAWN, (4, 1), False, 0), None, None, (MiniShogi.PieceType.ROOK, (4, 4), False, 1))
		))
