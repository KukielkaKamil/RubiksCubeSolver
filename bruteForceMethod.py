import old_stuff.rubicsCube as rubicsCube
from copy import deepcopy
import random as rnd


## This method does not yet and probably won't be continued
class RubiksSolver:
    def __init__(self, cube):
        self.cube = cube
        self.solution = []

    def solve(self):
        self._solve_recursive(deepcopy(self.cube), [])

    def _solve_recursive(self, cube, moves):
        if self.is_solved(cube):
            self.solution = moves
            return True
        
        if len(moves) >= 12:  # Maximum depth reached
            return False

        for i in range(12):
            cube_copy = deepcopy(cube)
            cube_copy.make_move(i)
            if self._solve_recursive(cube_copy, moves + [i]):
                return True
        
        return False

    def is_solved(self, cube):
        # Check if all faces have the same color
        all_faces = [cube.front, cube.back, cube.left, cube.right, cube.up, cube.down]
        colors = set()
        for face in all_faces:
            colors.update(face.flatten())
        return len(colors) == 1

# Usage example:
cube = rubicsCube.RubiksCube()
# Perform some random moves to scramble the cube
for _ in range(20):
    random_move = rnd.randint(0, 11)
    cube.make_move(random_move)

solver = RubiksSolver(cube)
solver.solve()
print("Solution:", solver.solution)