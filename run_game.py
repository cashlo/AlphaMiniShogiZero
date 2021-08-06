from gamewindow import GameWindow
from mini_shogi import MiniShogi

window = GameWindow("Mini Shogi")

game = MiniShogi.Game()

window.draw_board(game.board)

window.mainloop()