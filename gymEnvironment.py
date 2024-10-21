import gym
from gym import spaces
import numpy as np
from RubiksCube import RubiksCube,FACE
from copy import deepcopy

_correct_corners = {
    (0,29,42):('🟩','🟧','⬜'),
    (2,9,44):('🟩','🟥','⬜'),
    (6,35,45):('🟩','🟧','🟨'),
    (8,15,47):('🟩','🟥','🟨'),
    (18,11,38):('🟦','🟥','⬜'),
    (20,27,36):('🟦','🟧','⬜'),
    (24,17,53):('🟦','🟥','🟨'),
    (26,33,51):('🟦','🟧','🟨')
}

_correct_edges = {
    (1,43):('🟩','⬜'),
    (3,32):('🟩','🟧'),
    (5,12):('🟩','🟥'),
    (7,46):('🟩','🟨'),
    (10,41):('🟥','⬜'),
    (14,21):('🟥','🟦'),
    (16,50):('🟥','🟨'),
    (19,37):('🟦','⬜'),
    (23,30):('🟦','🟧'),
    (25,52):('🟦','🟨'),
    (28,39):('🟧','⬜'),
    (34,48):('🟧','🟨')
}

_learning_depth = 5
_current_cube = None
class CubeEnv(gym.Env):
    def __init__(self):
        super(CubeEnv, self).__init__()

        # Define the action and observation space
        self.action_space = spaces.Discrete(12)  # 12 possible moves (R, R', L, L', F, F', B, B', D, D', U, U')
        self.observation_space = spaces.Box(0, 5, shape=(54,), dtype=int)  # 6 possible colors for each of the 54 stickers

        self.cube = RubiksCube()  # Create an instance of your Rubik's cube
        # self.cube.scramble(_learning_depth)
        self.current_cube = deepcopy(self.cube)
        self.max_moves = _learning_depth  # Set the maximum number of moves
        self.current_moves = 0  # Initialize move counter

        # Define color-to-integer mapping (adjust based on your actual cube symbols)
        self.color_map = {
            '🟩': 0,  # Green
            '🟥': 1,  # Red
            '🟦': 2,  # Blue
            '🟨': 3,  # Yellow
            '🟧': 4,  # Orange
            '⬜': 5   # White
        }

    def reset(self):
        # Reset the cube and move counter
        print("RESET")
        self.cube = RubiksCube()
        self.cube.scramble(_learning_depth)
        self.current_cube = deepcopy(self.cube)
        self.current_moves = 0
        return self._get_observation()

    def step(self, action):

        if self.current_moves > self.max_moves:
            self.cube = self.current_cube
            print("CURR CUBE")
            self.current_cube.print_cube()
            # print("ACTUAL CUBE")
            # self.cube.print_cube()
            self.current_moves = 0
        # Execute the action
        self.cube.do_move(action)
        self.current_moves += 1  # Increment move counter

        # Get the new observation and reward
        observation = self._get_observation()
        reward = self._get_reward()
        

        # Check if done (either the cube is solved or max moves are reached)
        done = self.is_solved()


        return observation, reward, done, {}

    def _get_observation(self):
        # Convert cube's stickers (symbols) into integers using the color map
        cube_state = [self.color_map[symbol] for symbol in self.cube.cube]  # Assume self.cube.cube contains 54 symbols
        return np.array(cube_state, dtype=int)
    




    def _get_reward(self):

        if self.is_solved():
            reward = 1  # Add a large reward if solved
        else:
            reward = 0

        # correct_count = 0

        # # Check each corner
        # for (i,j,l),colors in _correct_corners.items():
        #     current_corner = (self.cube.cube[i],self.cube.cube[j],self.cube.cube[l])
        #     if current_corner == colors:
        #         correct_count += 1

        # # Check each edge
        # for (i,j),colors in _correct_edges.items():
        #     current_edge = (self.cube.cube[i],self.cube.cube[j])
        #     if current_edge == colors:
        #         correct_count += 1

        # reward = correct_count  # Normalize reward between 0 and 1

        # if self.is_solved():
        #     reward += 100  # Add a large reward if solved

        # # print(f"Correct Pieces: {correct_count}, Reward: {reward}")


        # # print(f"Correct Pieces: {correct_count}, Reward: {reward}")
        return reward


    def is_solved(self):
        # Check if the cube is solved (i.e., all faces are uniform)
        faces = [self.cube.face(face) for face in FACE]  # Get all faces
        for face in faces:
            if len(set(face)) != 1:  # All stickers on a face should be the same
                return False
        return True
    
