from RubiksCube import RubiksCube as rb


## Generate States

def generate_scrambled_states(cube, num_scrambles, num_samples):
    scrambled_states = []
    solutions = []
    for _ in range(num_samples):
        cube.reset()  # Reset the cube to the solved state
        scramble_moves = cube.scramble(num_scrambles)  # Scramble the cube
        scrambled_states.append(cube.get_state())  # Record scrambled state
        solution_length = solve_cube(cube)  # Use a solver to find solution length
        solutions.append(solution_length)  # Heuristic value is solution length
    return scrambled_states, solutions

cube = rb()  # Initialize your cube class
num_samples = 10000
num_scrambles = 10