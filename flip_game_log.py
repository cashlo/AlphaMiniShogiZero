import pickle

game_log = pickle.loads(open('game_log_minishogi_10.pickle', "rb").read())
for index in range(len(game_log['x'])):
	game_log['y'][1][index] = -1*game_log['y'][1][index]

f = open(f"game_log_minishogi_10_fliped.pickle", "wb")
f.write(pickle.dumps(game_log))
f.close()