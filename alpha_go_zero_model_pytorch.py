import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import glob
import threading

model_lock = threading.Lock()

def rotate_data(data, board_size, rotations):
    x, y0, y1 = data
    xr = torch.rot90(x, k=rotations, dims=[-2, -1])
    y0r = y0.view(-1, board_size, board_size, 1)
    y0r = torch.rot90(y0r, k=rotations, dims=[-2, -1])
    y0r = y0r.view(-1, board_size * board_size)

    return xr, y0r, y1

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, filters, kernel_size, l2_regularization=0.0001):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, filters, kernel_size, padding=1)
        self.bn1 = nn.BatchNorm2d(filters)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(filters, filters, kernel_size, padding=1)
        self.bn2 = nn.BatchNorm2d(filters)
    
    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out += identity
        return self.relu(out)

class AlphaGoZeroModel(nn.Module):
    def __init__(
            self,
            input_board_size=7,
            number_of_input_planes=2,
            policy_output_size=7*7,
            number_of_filters=8,
            kernel_size=3,
            number_of_residual_block=1,
            value_head_hidden_layer_size=8,
            l2_regularization=0.0001):
        super(AlphaGoZeroModel, self).__init__()
        self.number_of_filters = number_of_filters
        self.kernel_size = kernel_size
        self.number_of_residual_block = number_of_residual_block
        self.policy_output_size = policy_output_size
        self.value_head_hidden_layer_size = value_head_hidden_layer_size

        self.conv_block = nn.Sequential(
            nn.Conv2d(number_of_input_planes, number_of_filters, kernel_size, padding=1),
            nn.BatchNorm2d(number_of_filters),
            nn.ReLU()
        )

        self.residual_blocks = nn.Sequential(*[ResidualBlock(number_of_filters, number_of_filters, kernel_size)
                                               for _ in range(number_of_residual_block)])

        self.policy_head = nn.Sequential(
            nn.Conv2d(number_of_filters, 2, 1),
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * input_board_size * input_board_size, policy_output_size),
            nn.Softmax(dim=1)
        )

        self.value_head = nn.Sequential(
            nn.Conv2d(number_of_filters, 1, 1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(input_board_size * input_board_size, value_head_hidden_layer_size),
            nn.ReLU(),
            nn.Linear(value_head_hidden_layer_size, 1),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.residual_blocks(x)
        policy = self.policy_head(x)
        value = self.value_head(x)
        return policy, value

    def predict(self, input):
        with model_lock:
            self.eval()
            with torch.no_grad():
                return self(input)

    def init_model(self):
        self.model = self
        return self

    def clone(self):
        return copy.deepcopy(self)

    def load_model(self, model_folder=''):
        net_files = glob.glob(f'{model_folder}model_minishogi_*')
        if net_files:
            latest_model_file = max(net_files)
            self.load_state_dict(torch.load(latest_model_file))

    def evaluate_from_game_log(self, game_log, device):
        self.eval()
        x = torch.tensor(game_log['x'], dtype=torch.float32).to(device)
        y0 = torch.tensor(game_log['y'][0], dtype=torch.float32).to(device)
        y1 = torch.tensor(game_log['y'][1], dtype=torch.float32).to(device)

        criterion_policy = nn.CrossEntropyLoss()
        criterion_value = nn.MSELoss()

        policy_pred, value_pred = self(x)
        policy_loss = criterion_policy(policy_pred, y0)
        value_loss = criterion_value(value_pred, y1)
        total_loss = policy_loss + value_loss

        return total_loss.item()

    def train_from_game_log(self, game_log, device, epochs=3, lr=2e-4):
        self.train()
        x = torch.tensor(game_log['x'], dtype=torch.float32).to(device)
        y0 = torch.tensor(game_log['y'][0], dtype=torch.long).to(device)
        y1 = torch.tensor(game_log['y'][1], dtype=torch.float32).to(device)

        optimizer = optim.Adam(self.parameters(), lr=lr)

        criterion_policy = nn.CrossEntropyLoss()
        criterion_value = nn.MSELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            policy_pred, value_pred = self(x)
            policy_loss = criterion_policy(policy_pred, y0)
            value_loss = criterion_value(value_pred, y1)
            loss = policy_loss + value_loss
            loss.backward()
            optimizer.step()

    def train_from_game_log_gen(self, game_log_gen, device, epochs=3, lr=2e-4):
        self.train()
        optimizer = optim.Adam(self.parameters(), lr=lr)

        criterion_policy = nn.CrossEntropyLoss()
        criterion_value = nn.MSELoss()

        for epoch in range(epochs):
            for x, y0, y1 in game_log_gen:
                x = torch.tensor(x, dtype=torch.float32).to(device)
                y0 = torch.tensor(y0, dtype=torch.long).to(device)
                y1 = torch.tensor(y1, dtype=torch.float32).to(device)

                optimizer.zero_grad()
                policy_pred, value_pred = self(x)
                policy_loss = criterion_policy(policy_pred, y0)
                value_loss = criterion_value(value_pred, y1)
                loss = policy_loss + value_loss
                loss.backward()
                optimizer.step()
