from gymEnvironment import CubeEnv
from DQNAgent import DQNAgent
from RubiksCube import RubiksCube

env = CubeEnv()
agent = DQNAgent(input_dim=54,output_dim=12)

agent.load('final_model26.pth')

agent.epsilon=0.0

cube = RubiksCube()
cube.scramble(5)

state = env.reset()

env.cube.print_cube()


done = False
total_steps  = 0
total_reward = 0
max_steps = 26


while not done and total_steps < max_steps:
    # Agent chooses action based on the current state
    action = agent.act(state)
    
    # Take the action in the environment
    next_state, reward, done, info = env.step(action)
    
    # Update the state
    state = next_state
    total_reward += reward
    total_steps += 1
    
    # Optionally, print the state or progress
    print(f"Step {total_steps}: Action {action}, Reward {total_reward}")

    # Check if done (cube solved)
    if done:
        print(f"Rubik's Cube solved in {total_steps} steps!")
        env.cube.print_cube()
    elif total_steps >= max_steps:
        print("Max steps reached, the cube wasn't solved.")