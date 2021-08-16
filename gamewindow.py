from tkinter import *
import tkinter.font as tkFont

from mini_shogi import MiniShogi

class GameWindow:
	def __init__(self, title='', canvas_size=600, font_size=20, line_width=2, show_title=True, on_click=None):
		self.window = Tk()
		self.window.title(title)
		self.window.configure(bg="black")

		self.font_style = tkFont.Font(family="Helvetica", size=font_size)

		if show_title:
			self.title_bar = Label(self.window, text=title, bg="black", fg="white", font=self.font_style)
			self.title_bar.pack()

		self.render_counter = 0

		self.canvas_size = canvas_size
		self.margin_size = self.canvas_size/7
		self.row_height = (self.canvas_size - self.margin_size*2)/MiniShogi.SIZE

		self.canvas = Canvas(self.window, width=self.canvas_size, height=self.canvas_size, bg="#964B00")
		self.canvas.bind('<Button-1>', self.click)
		self.line_width=line_width
		self.draw_lines()
		self.canvas.pack()

		self.status_label = Label(self.window, text='', bg="black", fg="white", font=self.font_style)
		self.status_label.pack()

		self.on_click = on_click
		
		self.window.update()

	def click(self, event):
		x = int((event.x-self.margin_size)//self.row_height)
		y = int((event.y-self.margin_size)//self.row_height)

		promotion = False
		if y == 0:
			if (event.x-self.margin_size)/self.row_height - x > 0.5:
				promotion = True
		self.on_click(x, y, promotion)


	def draw_lines(self):		
		for i in range(MiniShogi.SIZE+1):
			self.canvas.create_line(
				self.margin_size+i*self.row_height,
				self.margin_size,
				self.margin_size+i*self.row_height,
				self.canvas_size-self.margin_size,
				width=self.line_width
			)
			self.canvas.create_line(
				self.margin_size,
				self.margin_size+i*self.row_height,
				self.canvas_size-self.margin_size,
				self.margin_size+i*self.row_height,
				width=self.line_width
			)

	def piece_to_capture_position(piece):
		if piece.player == 0:
			return {
				MiniShogi.PieceType.KING:   (2, -1),
				MiniShogi.PieceType.ROOK:   (-1, 0),
				MiniShogi.PieceType.BISHOP: (-1, 1),
				MiniShogi.PieceType.GOLD:   (-1, 2),
				MiniShogi.PieceType.SILVER: (-1, 3),
				MiniShogi.PieceType.PAWN:   (-1, 4),
			}[piece.pieceType]
		else:
			return {
				MiniShogi.PieceType.KING:   (2, 5),
				MiniShogi.PieceType.ROOK:   (5, 4),
				MiniShogi.PieceType.BISHOP: (5, 3),
				MiniShogi.PieceType.GOLD:   (5, 2),
				MiniShogi.PieceType.SILVER: (5, 1),
				MiniShogi.PieceType.PAWN:   (5, 0),
			}[piece.pieceType]

	def capture_position_to_piece(game, position):
		player, piece_type = {
			(2,  -1): (0, MiniShogi.PieceType.KING),
			(-1,  0): (0, MiniShogi.PieceType.ROOK),
			(-1,  1): (0, MiniShogi.PieceType.BISHOP),
			(-1,  2): (0, MiniShogi.PieceType.GOLD),
			(-1,  3): (0, MiniShogi.PieceType.SILVER),
			(-1,  4): (0, MiniShogi.PieceType.PAWN),
			(2,   5): (1, MiniShogi.PieceType.KING),
			(5,   4): (1, MiniShogi.PieceType.ROOK),
			(5,   3): (1, MiniShogi.PieceType.BISHOP),
			(5,   2): (1, MiniShogi.PieceType.GOLD),
			(5,   1): (1, MiniShogi.PieceType.SILVER),
			(5,   0): (1, MiniShogi.PieceType.PAWN)
		}[position]

		for p in game.player_pieces[player]:
			if p.pieceType == piece_type and p.position is None:
				return p


	def draw_piece(self, piece):
		if piece is None:
			return
		row_height = (self.canvas_size - self.margin_size*2 )/MiniShogi.SIZE
		
		points = [1/2, 1/10, 8/10, 2/10, 9/10, 9/10, 1/10, 9/10, 2/10, 2/10, 1/2, 1/10]
		if piece.player == 0:
			points = [1-p if i%2 else p for i, p in enumerate(points)]
		position = piece.position if piece.position is not None else GameWindow.piece_to_capture_position(piece)
		points = [self.margin_size+(position[i%2]+p)*row_height for i, p in enumerate(points)]
		self.canvas.create_polygon(
			points,
			fill="#FFD167",
			tags = "piece"
		)
		font = tkFont.Font(family="Helvetica", size=40)
		self.canvas.create_text(
			self.margin_size+(position[0]+1/2)*row_height,
			self.margin_size+(position[1]+1/2)*row_height,
			text=piece.get_name(),
			font=font,
			tags = "piece",
			angle=0  if piece.player else 180
		)

	def draw_possible_moves(self, moves, piece):
		self.canvas.delete('possible_moves')
		for m in moves:
			piece_type, old_position, new_position, promoted = m
			if piece.pieceType != piece_type or piece.position != old_position:
				continue
			self.canvas.create_rectangle(
				self.margin_size+new_position[0]*self.row_height,
				self.margin_size+new_position[1]*self.row_height,
				self.margin_size+(new_position[0]+1)*self.row_height,
				self.margin_size+(new_position[1]+1)*self.row_height,
				outline='red',
				width=5,
				# dash=(4, 4),
				tags='possible_moves'
			)

	def draw_move(self, move, clear_old_move = True, score=1, arrow_width=20):
		if clear_old_move:
			self.canvas.delete('move')
		
		piece_type, old_position, new_position, promoted = move
		if old_position is None:
			self.canvas.create_line(
				self.margin_size+(new_position[0]+0.5)*self.row_height,
				self.margin_size+(new_position[1]+0.1)*self.row_height,
				self.margin_size+(new_position[0]+0.5)*self.row_height,
				self.margin_size+(new_position[1]+0.5)*self.row_height,
				arrow=LAST,
				arrowshape=(20,20,6),
				fill='red',
				width=arrow_width*score,
				tags='move'
			)
		else:	
			self.canvas.create_line(
				self.margin_size+(old_position[0]+0.5)*self.row_height,
				self.margin_size+(old_position[1]+0.5)*self.row_height,
				self.margin_size+(new_position[0]+0.5)*self.row_height,
				self.margin_size+(new_position[1]+0.5)*self.row_height,
				arrow=LAST,
				arrowshape=(20,20,6),
				fill='red',
				width=arrow_width*score,
				tags='move'
			)
		self.window.update()


	def draw_board(self, game):
		self.canvas.delete('piece')
		self.canvas.delete('possible_moves')

		for player_pieces in game.player_pieces:
			for piece in player_pieces:
				self.draw_piece(piece)
		self.window.update()

	def set_status(self, status):
		self.status_label['text'] = status
		self.window.update()

	def mainloop(self):
		self.window.mainloop()