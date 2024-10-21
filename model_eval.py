import gym
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
import torch as th
from my_gym import RubiksCubeEnv

env = RubiksCubeEnv()
model = DQN.load("dqn_rubiks_cube")

# Evaluate the agent
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)

print(f"Mean reward: {mean_reward} ± {std_reward}")

# Test the agent by running it on a new scrambled cube
obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()  # This will print the cube after each action