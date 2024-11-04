import gym
import numpy as np
from my_gym import RubiksCubeEnv
from DQN2 import DQNAgent

env = RubiksCubeEnv()
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

agent = DQNAgent(state_dim, action_dim)
episodes = 100000
target_update_frequency = 100  # Update target network every 10 episodes
adaptive_epsilon_reset = 5000
for e in range(episodes):
    state = env.reset()
    total_reward = 0
    for time in range(env.max_steps):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        if done:
            print(f"Episode: {e+1}/{episodes}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")
            break
        
        # Perform experience replay and update the model
        agent.replay()

    # Update target network
    if e % target_update_frequency == 0:
        agent.update_target_model()

    if e % adaptive_epsilon_reset == 0:
        agent.epsilon = max(agent.epsilon, 0.3)  # Reset epsilon periodically to induce exploration

    if agent.epsilon > agent.epsilon_min:
        agent.epsilon *= agent.epsilon_decay

