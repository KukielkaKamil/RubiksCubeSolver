from gymEnvironment import CubeEnv
from DQNAgent import DQNAgent

env = CubeEnv()
agent = DQNAgent(input_dim=54, output_dim=12)

episodes = 10000
target_update_frequency = 10

for episode in range(episodes):
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    
    while not done:
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        agent.train()
        
        state = next_state
        total_reward += reward
        steps += 1
        
        if done:
            print(f"Episode {episode + 1}, Total Reward: {total_reward}, Steps: {steps}")
    
    agent.update_epsilon()
    
    if episode % target_update_frequency == 0:
        agent.update_target_model()

agent.save('test_model.pth')
