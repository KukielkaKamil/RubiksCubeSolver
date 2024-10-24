import gym
from gym import spaces
import numpy as np
from RubiksCube import RubiksCube

class RubiksCubeEnv(gym.Env):
    def __init__(self):
        super(RubiksCubeEnv, self).__init__()

        self.cube = RubiksCube()

        self.action_space = spaces.Discrete(12)
        self.observation_space =spaces.Box(low=0,high=1,shape=(54,),dtype=np.int64)

        self.max_steps = 10
        self.current_step = 0

    def reset(self):
        self.cube = RubiksCube()
        self.cube.scramble(5)
        self.current_step = 0

        return np.array(self.cube.encode_state(),dtype=np.int64)
    
    def step(self,action):
        self.cube.do_move(action)
        self.current_step +=1

        new_state = np.array(self.cube.encode_state(), dtype=np.int64)

        reward = 0
        

        if self.cube.hasWhiteCross():
            reward += 100
            done = True
        else:
            # colors = ["🟩","🟥","🟦","🟧","⬜","🟨"]
            # for i in range(6):
            #     face_start = 9*i
            #     for j in range(face_start,face_start+9):
            #         if self.cube.cube[j] == colors[i]:
            #             reward += 1

            patter_positions = [(37,19,'🟦'),(41,10,'🟥'),(43,1,'🟩'),(39,28,'🟧')]

            for up_pos, adj_pos, adj_col in patter_positions:
                if self.cube.cube[up_pos] == '⬜' or self.cube.cube[adj_pos] == adj_col:
                    reward += 1
            done = False
        
        if self.current_step >= self.max_steps:
            done = True

        return new_state, reward, done, {}

    def render(self):
        self.cube.print_cube()