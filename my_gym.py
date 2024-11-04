import gym
from gym import spaces
import numpy as np
from RubiksCube import RubiksCube

class RubiksCubeEnv(gym.Env):
    def __init__(self):
        super(RubiksCubeEnv, self).__init__()
        
        self.cube = RubiksCube()
        self.action_space = spaces.Discrete(12)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(54,), dtype=np.float32)
        
        self.max_steps = 20
        self.current_step = 0

    def reset(self):
        self.cube = RubiksCube()
        self.cube.scramble(10)
        self.current_step = 0
        return np.array(self.cube.encode_state(), dtype=np.float32)

    def step(self, action):
        self.cube.do_move(action)
        self.current_step += 1
        new_state = np.array(self.cube.encode_state(), dtype=np.float32)
        
        # Base reward penalty to encourage fewer moves
        reward = 0
        reward = -1
        done = False

        # Reward for achieving the white cross, our end goal
        if self.cube.hasWhiteCross():
            reward = 100
            done = True
        else:
            # Partial pattern matching (e.g., one correct piece in position = +5 reward)
            pattern_positions = [(37, 19, '🟦'), (41, 10, '🟥'), (43, 1, '🟩'), (39, 28, '🟧')]
            for up_pos, adj_pos, adj_col in pattern_positions:
                if self.cube.cube[up_pos] == '⬜' and self.cube.cube[adj_pos] == adj_col:
                    reward += 2  # Small reward for each correct pair
            
        # reward *= self.current_step/self.max_steps

        if self.current_step >= self.max_steps:
            done = True

        return new_state, reward, done, {}


    def render(self):
        self.cube.print_cube()
