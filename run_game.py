from gamewindow import GameWindow
from mini_shogi import MiniShogi
import time
from mini_shogi_search_tree import MiniShogiSearchTree
from alpha_go_zero_model import AlphaGoZeroModel
from alpha_mini_shogi_search_tree import AlphaMiniShogiSearchTree
import glob
import tensorflow as tf

game = MiniShogi.Game()
game.setup()


player_1_model = AlphaGoZeroModel(
        input_board_size=MiniShogi.SIZE,
        number_of_input_planes=6*2*2+4*2,
        policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6),
        number_of_filters=64,
        number_of_residual_block=20,
        value_head_hidden_layer_size=64
    )

player_2_model = AlphaGoZeroModel(
        input_board_size=MiniShogi.SIZE,
        number_of_input_planes=6*2*2+4*2,
        policy_output_size=MiniShogi.SIZE*(MiniShogi.SIZE+1)*(MiniShogi.SIZE*MiniShogi.SIZE+6),
        number_of_filters=64,
        number_of_residual_block=20,
        value_head_hidden_layer_size=64
    )


human_player_2 = False

net_files = glob.glob(f'model_minishogi_*')
if net_files:
    print("Pick player 1:")
    for i, file in enumerate(net_files):
        print(f"{i}: {file}")
    file_index = int(input())
    picked_model_file = net_files[file_index]
    print(f"Picked: {picked_model_file}")
    player_1_model.model = tf.keras.models.load_model(picked_model_file)

    print("Pick player 2:")
    print(f"-1: Human")
    for i, file in enumerate(net_files):
        print(f"{i}: {file}")
    file_index = int(input())
    if file_index == -1:
        human_player_2 = True
    else:
        picked_model_file = net_files[file_index]
        print(f"Picked: {picked_model_file}")
        player_2_model.model = tf.keras.models.load_model(picked_model_file)

search_tree_1 = AlphaMiniShogiSearchTree(game.clone(), player_1_model,simulation_limit=600, exploration_constant=1)
search_tree_2 = AlphaMiniShogiSearchTree(game.clone(), player_2_model,simulation_limit=600, exploration_constant=1)



last_clicked_piece = None
def on_click(x, y, promotion):
    global search_tree_1
    winner = game.check_game_over()
    if winner is not None:
        print("Winner is ", winner)
        return
    if not game.board.is_position_on_board( (x, y) ):
        p = GameWindow.capture_position_to_piece(game, (x, y))
    else:
        p = game.board.piece_at( (x, y) )
    global last_clicked_piece
    global search_tree

    if p is None or (last_clicked_piece and p.player != last_clicked_piece.player):
        if last_clicked_piece is not None:
            player = last_clicked_piece.player
            legal_moves = game.all_legal_moves(last_clicked_piece.player)
            clicked_move = (last_clicked_piece.pieceType, last_clicked_piece.position, (x, y), promotion)
            if clicked_move in legal_moves:
                game.make_move(clicked_move)
                search_tree_1 = search_tree_1.create_from_move(clicked_move)
                # search_tree = search_tree.create_from_move( clicked_move )
                window.draw_board(game)
                window.draw_move(clicked_move)
                winner = game.check_game_over()
                if winner is not None:
                    print("Winner is ", winner)
                    return
    
                player_1_move()
                # search_tree = search_tree.search(step=100, move_window=mind_window_1)
                # move = search_tree.from_move
                # game.make_move(move)
                # window.draw_board(game)
                # window.draw_move(move)
                
            last_clicked_piece = None
        return

    if p.player == 1:
        return
    last_clicked_piece = p
    legal_moves = game.all_legal_moves(p.player)
    # print(legal_moves)
    window.draw_possible_moves(legal_moves, p)

def make_random_move():
    winner = game.check_game_over()
    if winner is None:
        move = game.random_move()
        game.make_move(move)
        window.draw_board(game)
        window.window.after(1, make_random_move)
    else:
        print("Winner: ", winner)

window = GameWindow("Mini Shogi", on_click=on_click)
mind_window_1 = GameWindow("Player 1", show_title=False, line_width=4, canvas_size=400)
mind_window_2 = GameWindow("Player 2", show_title=False, line_width=4, canvas_size=400)

tree_window_1 = GameWindow("Player 1 Tree", show_title=False, line_width=2, canvas_size=200, tree_window=True)


def player_1_move():
    global search_tree_1
    global search_tree_2
    global mind_window_1

    search_tree_1 = search_tree_1.search(step=100, move_window=mind_window_1, tree_window=tree_window_1)
    move = search_tree_1.from_move
    game.make_move(move)
    if not human_player_2:
        search_tree_2 = search_tree_2.create_from_move(move)
    window.draw_board(game)
    window.draw_move(move)
    winner = game.check_game_over()
    if winner is None:
        if not human_player_2:
            player_2_move()
    else:
        print("Winner: ", winner)

def player_2_move():
    global search_tree_1
    global search_tree_2
    global mind_window_2

    search_tree_2 = search_tree_2.search(step=100, move_window=mind_window_2)
    move = search_tree_2.from_move
    game.make_move(move)
    search_tree_1 = search_tree_1.create_from_move(move)
    window.draw_board(game)
    window.draw_move(move)
    winner = game.check_game_over()
    if winner is None:
        player_1_move()
    else:
        print("Winner: ", winner)

window.draw_board(game)
player_1_move()
                

window.mainloop()