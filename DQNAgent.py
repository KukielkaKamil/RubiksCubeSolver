import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import numpy as np

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def __init__(self, input_dim, output_dim, gamma=0.99, epsilon=1.0, lr=0.001, epsilon_decay=0.995, min_epsilon=0.01):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        self.model = DQN(input_dim, output_dim)
        self.target_model = DQN(input_dim, output_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.output_dim - 1)  # Random action
        else:
            state = torch.tensor(state, dtype=torch.float).unsqueeze(0)
            q_values = self.model(state)
            return torch.argmax(q_values).item()

    def train(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = np.array(states)
        states = torch.tensor(states, dtype=torch.float)
        actions = np.array(actions)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = np.array(rewards)
        rewards = torch.tensor(rewards, dtype=torch.float)
        next_states = np.array(next_states)
        next_states = torch.tensor(next_states, dtype=torch.float)
        dones = np.array(dones)
        dones = torch.tensor(dones, dtype=torch.float)

        q_values = self.model(states)
        next_q_values = self.target_model(next_states)
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        max_next_q_value = next_q_values.max(1)[0]

        target_q_value = rewards + self.gamma * max_next_q_value * (1 - dones)
        loss = self.criterion(q_value, target_q_value.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

 # Method to save the model weights
    def save(self, filepath):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'target_model_state_dict': self.target_model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, filepath)
        print(f"Model saved to {filepath}")

    # Method to load the model weights
    def load(self, filepath):
        checkpoint = torch.load(filepath)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.target_model.load_state_dict(checkpoint['target_model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
        print(f"Model loaded from {filepath}")