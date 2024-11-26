import numpy as np
from collections import deque
from RubiksCube import RubiksCube
import tensorflow as tf

class IDAStarSolver:
    def __init__(self, cube: RubiksCube, model):
        self.cube = cube
        self.model = model
        self.max_depth = 12  # Set the maximum depth as per your cube

    def heuristic(self, state):
        """
        Return the heuristic value (predicted depth) for a given state using the model.
        """
        state_array = np.array(state)
        state_array = state_array.reshape(1, -1)
        return np.rint(self.model.predict(state_array)[0][0])

    def apply_move(self, cube, move):
        """
        Apply the given move to the Rubik's Cube.
        """
        # Here, we use RubiksCube's do_move method (which uses move integers)
        cube.do_move(move)

    def get_neighbors(self, cube):
        """
        Return all possible states that can be reached from the current state.
        We generate neighbors by making valid moves on the cube.
        """
        neighbors = []
        for move in range(12):  # There are 12 possible moves (0 to 11)
            new_cube = RubiksCube()
            new_cube.cube = cube.cube.copy()  # Make a copy of the cube
            self.apply_move(new_cube, move)
            neighbors.append(new_cube)
        return neighbors

    def dfs(self, cube, g, bound, path):
        """
        Perform a depth-first search with the given bound (IDA*).
        g is the cost to reach this state, bound is the threshold for this iteration.
        path stores the path for reconstructing the solution later.
        """
        state = cube.encode_state()  # Get the current state as an encoded list
        f = g + self.heuristic(state)  # Total cost: depth + heuristic

        print(f"Depth: {bound}")

        if f > bound:
            return f  # If the estimated cost exceeds the bound, return the cost
        
        if cube.is_solved():
            return "FOUND"  # Found a solution

        min_cost = float('inf')
        neighbors = self.get_neighbors(cube)
        
        for neighbor in neighbors:
            path.append(neighbor)
            cost = self.dfs(neighbor, g + 1, bound, path)
            if cost == "FOUND":
                return "FOUND"  # Solution found
            if cost < min_cost:
                min_cost = cost
            path.pop()  # Backtrack

        return min_cost  # Return the minimum cost

    def ida_star(self):
        """
        Main function for the IDA* algorithm.
        Iteratively deepens the threshold to search for the solution.
        """
        bound = self.heuristic(self.cube.encode_state())  # Initial bound is the heuristic of the initial state
        path = deque([self.cube])  # Start with the initial state in the path

        while True:
            result = self.dfs(self.cube, 0, bound, path)
            if result == "FOUND":
                return path  # Solution found, return the path of states
            if result == float('inf'):
                return None  # No solution exists within the max depth
            bound = result  # Increase the threshold for the next iteration

# Example Usage
if __name__ == "__main__":
    # Create a Rubik's Cube object
    rubiks_cube = RubiksCube()
    
    # Optionally, scramble the cube
    rubiks_cube.scramble(10)  # Scramble the cube with 20 random moves
    
    print("Scrambled Cube:")
    rubiks_cube.print_cube()

    # Load your trained model
    model = tf.keras.models.load_model('rubiks_cube_model.h5')  # Assuming your model is saved here

    # Create an IDA* solver with the cube and model
    solver = IDAStarSolver(rubiks_cube, model)
    
    # Solve the cube using IDA*
    solution_path = solver.ida_star()

    if solution_path:
        print("Solution found:")
        for state in solution_path:
            state.print_cube()
    else:
        print("No solution found.") 