from enum import Enum
import random as rnd


class FACE(Enum):
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    TOP = 4
    BOTTOM = 5


class RubiksCube:
    _attached_indices = {
        FACE.FRONT: [(45, 46, 47), (9, 12, 15), (42, 43, 44), (29, 32, 35)],  # Down, Right, Up, Left
        FACE.RIGHT: [(47, 50, 53), (18, 21, 24), (38, 41, 44), (2, 5, 8)],    # Down, Back, Up, Front
        FACE.BACK: [(51, 52, 53), (27, 30, 33), (36, 37, 38), (11, 14, 17)],  # Down, Left, Up, Right
        FACE.LEFT: [(45, 48, 51), (0, 3, 6), (36, 39, 42), (20, 23, 26)],     # Down, Front, Up, Back
        FACE.TOP: [(0, 1, 2), (9, 10, 11), (18, 19, 20), (27, 28, 29)],       # Front, Right, Back, Left
        FACE.BOTTOM: [(24, 25, 26), (15, 16, 17), (6, 7, 8), (33, 34, 35)],  # Front, Right, Back, Left
    }

    def __init__(self):
        self.cube = list(
            "GGGGGGGGGRRRRRRRRRBBBBBBBBBOOOOOOOOOWWWWWWWWWYYYYYYYYY"
        )
        self.total_moves = 0

    def print_face(self, face_name, start_index):
        print(f"{face_name}:")
        for i in range(3):
            print(" ".join(self.cube[start_index + i * 3 : start_index + (i + 1) * 3]))
        print()

    def print_cube(self):
        self.print_face("Front", 0)
        self.print_face("Right", 9)
        self.print_face("Back", 18)
        self.print_face("Left", 27)
        self.print_face("Up", 36)
        self.print_face("Down", 45)

    def _rotate_face(self, face: FACE, clockwise=True):
        start = face.value * 9
        original_cube = self.cube.copy()

        # Rotate the face itself
        if clockwise:
            # Clockwise rotation of the face
            for i in range(3):
                for j in range(3):
                    self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]
        else:
            # Counterclockwise rotation of the face
            for i in range(3):
                for j in range(3):
                    self.cube[start + i * 3 + j] = original_cube[start + j * 3 + (2 - i)]

        # Rotate the adjacent edges
        idx1, idx2, idx3, idx4 = self._attached_indices[face]

        if clockwise:
            # Clockwise rotation adjustment
            temp = [self.cube[idx4[i]] for i in range(3)]  # Store the left edge (from left face)
            for i in range(3):
                self.cube[idx4[i]] = original_cube[idx1[i]]  # Left -> Front
                self.cube[idx1[i]] = original_cube[idx2[i]]  # Front -> Right
                self.cube[idx2[i]] = original_cube[idx3[i]]  # Right -> Back
                self.cube[idx3[i]] = temp[i]  # Back -> Left
        else:
            # Counterclockwise rotation adjustment
            temp = [self.cube[idx1[i]] for i in range(3)]  # Store the front edge (from front face)
            for i in range(3):
                self.cube[idx1[i]] = original_cube[idx4[i]]  # Left -> Front
                self.cube[idx2[i]] = original_cube[idx1[i]]  # Front -> Right
                self.cube[idx3[i]] = original_cube[idx2[i]]  # Right -> Back
                self.cube[idx4[i]] = temp[i]  # Back -> Left

    def rotate(self, move):
        face, clockwise = move[0], move[-1] == "'"
        moves = {
            "F": FACE.FRONT,
            "B": FACE.BACK,
            "R": FACE.RIGHT,
            "L": FACE.LEFT,
            "U": FACE.TOP,
            "D": FACE.BOTTOM
        }
        if face in moves:
            self._rotate_face(moves[face], not clockwise)  # Invert for counterclockwise
            self.total_moves += 1

    def scramble(self, moves):
        last_move = None
        for _ in range(moves):
            move_list = ["R", "R'", "L", "L'", "F", "F'", "B", "B'", "U", "U'", "D", "D'"]
            if last_move:
                # Avoid undoing the previous move
                move_list = [m for m in move_list if m[0] != last_move[0]]
            move = rnd.choice(move_list)
            self.rotate(move)
            last_move = move

    def rotate_y(self, times=1):
        times = times % 4
        for _ in range(times):
            front, right, back, left = self.cube[:9], self.cube[9:18], self.cube[18:27], self.cube[27:36]
            self.cube[:9], self.cube[9:18], self.cube[18:27], self.cube[27:36] = left, front, right, back
            self._rotate_face(FACE.TOP, True)
            self._rotate_face(FACE.BOTTOM, False)

    def rotate_x(self, times=1):
        times = times % 4
        for _ in range(times):
            top, front, bottom, back = self.cube[36:45], self.cube[:9], self.cube[45:54], self.cube[18:27]
            self.cube[:9], self.cube[36:45], self.cube[45:54], self.cube[18:27] = top, back, front, bottom
            self._rotate_face(FACE.LEFT, True)
            self._rotate_face(FACE.RIGHT, False)

    def do_moves(self, moves):
        if isinstance(moves, list):
            for move in moves:
                self.rotate(move)
        else:
            self.rotate(moves)


# Example of usage
cube = RubiksCube()
# Perform specific moves
cube.do_moves(["R", "R", "F","L'"])
cube.print_cube()
