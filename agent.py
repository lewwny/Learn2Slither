import random
import pickle
import os
from utils import *

class Agent:
    """"""
    def __init__(self, load_path=None, learning=True):
        """init the agent with the q-table and learning parameters"""
        self.learning = learning
        self.q_table = {}
        if load_path and os.path.exists(load_path):
            with open(load_path, 'rb') as f:
                self.q_table = pickle.load(f)
        self.lr = 0.1
        self.gamma = 0.9
        self.epsilon = 1.0 if learning else 0.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01