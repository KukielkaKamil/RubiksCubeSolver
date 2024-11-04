import gym
from stable_baselines3 import DQN, HER
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.her.goal_selection_strategy import GoalSelectionStrategy
import torch as th
from my_gym import RubiksCubeEnv

# Assuming RubiksCubeEnv is already defined and implemented
env = RubiksCubeEnv()

# Define the DQN policy and network parameters
# You can customize the MLP architecture (multilayer perceptron)
policy_kwargs = dict(
    net_arch=[512, 512],  # Example network architecture with two hidden layers of 256 units each
    activation_fn=th.nn.ReLU,  # Using ReLU activations
)

# Initialize the DQN model
model = DQN(
    policy="MlpPolicy",
    env=env,
    learning_rate=0.00005,
    buffer_size=200000,
    learning_starts=10000,
    batch_size=64,
    tau=1.0,
    gamma=0.99,
    train_freq=4,
    policy_kwargs=policy_kwargs,
    verbose=1,
    target_update_interval=1000,
    exploration_initial_eps=1.0,
    exploration_final_eps=0.05,
    exploration_fraction=0.4,  # More exploration
)





# Train the agent for a specified number of timesteps
total_timesteps = 2000000      # Adjust depending on your hardware and goals
model.learn(total_timesteps=total_timesteps)

# Save the trained model
model.save("wc_rubiks_cube")

# After training, you can load the model like this:
# model = DQN.load("dqn_rubiks_cube")
