import gym
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
import torch as th
from my_gym import RubiksCubeEnv

# Assuming RubiksCubeEnv is already defined and implemented
env = RubiksCubeEnv()

# Define the DQN policy and network parameters
# You can customize the MLP architecture (multilayer perceptron)
policy_kwargs = dict(
    net_arch=[256, 256,256,256],  # Example network architecture with two hidden layers of 256 units each
    activation_fn=th.nn.ReLU,  # Using ReLU activations
)

# Initialize the DQN model
model = DQN(
    policy="MlpPolicy",
    env=env,
    learning_rate=0.001,  # Learning rate for the optimizer
    buffer_size=50000,     # Replay buffer size
    learning_starts=1000,  # Steps before training begins (populating replay buffer)
    batch_size=32,         # Batch size for experience replay
    tau=1.0,               # Soft update parameter for target network
    gamma=0.99,            # Discount factor for future rewards
    train_freq=5,          # How often to train the network (in steps)
    policy_kwargs=policy_kwargs,
    verbose=1,             # Set to 1 to see training progress
    target_update_interval=1000,  # How often to update the target network
    exploration_initial_eps=1.0,
    exploration_final_eps=0.01,
    exploration_fraction=0.1,
)

# Train the agent for a specified number of timesteps
total_timesteps = 1000000      # Adjust depending on your hardware and goals
model.learn(total_timesteps=total_timesteps)

# Save the trained model
model.save("dqn_rubiks_cube")

# After training, you can load the model like this:
# model = DQN.load("dqn_rubiks_cube")