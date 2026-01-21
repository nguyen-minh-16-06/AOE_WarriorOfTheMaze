import numpy as np
import random
import pickle

class QLearningAgent:
    def __init__(self, action_space_size=4, learning_rate=0.5, discount_factor=0.9, epsilon=0.3):
        self.q_table = {}
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.action_space = action_space_size

    def get_q(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_space)
        return self.q_table[state]

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space - 1)
        return np.argmax(self.get_q(state))

    def learn(self, state, action, reward, next_state):
        old_value = self.get_q(state)[action]
        next_max = np.max(self.get_q(next_state))

        # Q-Learning Formula
        new_value = old_value + self.lr * (reward + self.gamma * next_max - old_value)
        self.q_table[state][action] = new_value

    def save_model(self, filename="q_table.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_model(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                if isinstance(data, dict):
                    self.q_table = data
                else:
                    self.q_table = data.q_table
        except FileNotFoundError:
            print(f"Warning: Model file '{filename}' not found. Starting with empty Q-table.")