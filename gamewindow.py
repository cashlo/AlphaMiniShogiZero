from tkinter import *
import tkinter.font as tkFont

from mini_shogi import MiniShogi

class GameWindow:
	def __init__(self, title='', canvas_size=600, font_size=20, line_width=2, show_title=True):
		self.window = Tk()
		self.window.title(title)
		self.window.configure(bg="black")

		self.font_style = tkFont.Font(family="Helvetica", size=font_size)

		if show_title:
			self.title_bar = Label(self.window, text=title, bg="black", fg="white", font=self.font_style)
			self.title_bar.pack()

		self.render_counter = 0

		self.canvas_size = 600
		self.canvas = Canvas(self.window, width=self.canvas_size, height=self.canvas_size, bg="#964B00")
		self.line_width=line_width
		self.draw_lines()
		self.canvas.pack()

		self.status_label = Label(self.window, text='', bg="black", fg="white", font=self.font_style)
		self.status_label.pack()

		self.window.update()

	def draw_lines(self):
		margin_size = self.canvas_size/20
		row_height = (self.canvas_size - margin_size*2)/MiniShogi.SIZE
		for i in range(MiniShogi.SIZE+1):
			self.canvas.create_line( margin_size+i*row_height, margin_size, margin_size+i*row_height, self.canvas_size-margin_size, width=self.line_width)
			self.canvas.create_line(margin_size, margin_size+i*row_height, self.canvas_size-margin_size, margin_size+i*row_height, width=self.line_width)

	def draw_piece(self, piece):
		if piece is None:
			return
		margin_size = self.canvas_size/20
		row_height = (self.canvas_size - margin_size*2)/MiniShogi.SIZE
		
		points = [1/2, 1/10, 8/10, 2/10, 9/10, 9/10, 1/10, 9/10, 2/10, 2/10, 1/2, 1/10]
		if piece.player == 0:
			points = [1-p if i%2 else p for i, p in enumerate(points)]
		points = [margin_size+(piece.position[i%2]+p)*row_height for i, p in enumerate(points)]
		self.canvas.create_polygon(
			points,
			fill="#FFD167"
		)
		font = tkFont.Font(size=40)
		self.canvas.create_text(
			margin_size+(piece.position[0]+1/2)*row_height,
			margin_size+(piece.position[1]+1/2)*row_height,
			text=piece.pieceType.value,
			font=font,
			angle=0 if piece.player else 180
		)


	def draw_board(self, board):
		for file in board.board:
			for piece in file:
				self.draw_piece(piece)

	def mainloop(self):
		self.window.mainloop()