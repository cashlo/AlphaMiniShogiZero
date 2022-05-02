import tensorflow as tf
import glob
import pickle
import numpy as np

class GameLogDataGenerator(tf.keras.utils.Sequence):
	def __init__(self, batch_size):
		self.batch_size = batch_size
		self.file_names = glob.glob(f'**/game_log_minishogi_1000_*', recursive=True)
		self.game_log_sizes = []
		self.total_size = 0
		self.batched_total_size = 0
		for file in self.file_names:
			print(file)
			game_log = pickle.loads(open(file, "rb").read())
			self.game_log_sizes.append( ( self.total_size, len(game_log['x']) ) )
			self.total_size += len(game_log['x'])
			self.batched_total_size += len(game_log['x']) // self.batch_size
		self.current_file_index = 0
		self.current_file = pickle.loads(open(self.file_names[0], "rb").read())

	def __len__(self):
		return self.batched_total_size

	def __getitem__(self, index):
		print(f"getting {index}")
		real_index = index*self.batch_size
		changed_file = False
		while real_index < self.game_log_sizes[self.current_file_index][0]:
			#print(self.current_file_index)
			#print("to last file")
			self.current_file_index -= 1
			changed_file = True
		while real_index + self.batch_size >= self.game_log_sizes[self.current_file_index][0] +  self.game_log_sizes[self.current_file_index][1]:
			#print(self.current_file_index)
			#print("to next file")
			self.current_file_index += 1
			changed_file = True
		if changed_file:
			print(f"loading {self.file_names[self.current_file_index]}")
			self.current_file = pickle.loads(open(self.file_names[self.current_file_index], "rb").read())
		file_index = real_index - self.game_log_sizes[self.current_file_index][0]
		x = np.array(self.current_file['x'][file_index:file_index + self.batch_size])
		y0 = np.array(self.current_file['y'][0][file_index:file_index + self.batch_size])
		y1 = np.array(self.current_file['y'][1][file_index:file_index + self.batch_size])
		return x, [y0, y1]

# test = GameLogDataGenerator(32)
# print(test.__getitem__(9731))
# import code
# code.interact(local=locals())
