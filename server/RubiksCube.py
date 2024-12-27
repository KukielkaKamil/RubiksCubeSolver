from enum import Enum
import numpy as np
import random as rnd


class FACE(Enum):
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    TOP = 4
    BOTTOM = 5


class RubiksCube:
    _attached_faces = {
        FACE.FRONT: (FACE.BOTTOM, FACE.RIGHT, FACE.TOP, FACE.LEFT),
        FACE.RIGHT: (FACE.BOTTOM, FACE.BACK, FACE.TOP, FACE.FRONT),
        FACE.BACK: (FACE.BOTTOM, FACE.LEFT, FACE.TOP, FACE.RIGHT),
        FACE.LEFT: (FACE.BOTTOM, FACE.FRONT, FACE.TOP, FACE.BACK),
        FACE.TOP: (FACE.FRONT, FACE.RIGHT, FACE.BACK, FACE.LEFT),
        FACE.BOTTOM: (FACE.BACK, FACE.RIGHT, FACE.FRONT, FACE.LEFT),
    }
    _attached_indices = {
        FACE.FRONT: [(45, 46, 47), (9, 12, 15), (42, 43, 44), (29, 32, 35)],
        FACE.RIGHT: [(47, 50, 53), (18, 21, 24), (38, 41, 44), (2, 5, 8)],
        FACE.BACK: [(51, 52, 53), (27, 30, 33), (36, 37, 38), (11, 14, 17)],
        FACE.LEFT: [(45, 48, 51), (0, 3, 6), (36, 39, 42), (20, 23, 26)],
        FACE.TOP:[(0, 1, 2), (9, 10, 11), (18, 19, 20), (27, 28, 29)],
        FACE.BOTTOM: [(24, 25, 26), (15, 16, 17), (6, 7, 8), (33, 34, 35)],
    }
    _flip_colors_clockwise = {
        FACE.FRONT: (1, -1, 1, -1),
        FACE.RIGHT: (1, -1, -1, 1),
        FACE.BACK: (-1, 1, -1, 1),
        FACE.LEFT: (-1, 1, 1, -1),
        FACE.TOP: (1, 1, 1, 1),
        FACE.BOTTOM: (1, 1, 1, 1),
    }
    _flip_colors_Counter_clockwise = {
        FACE.FRONT: (-1, 1, -1, 1),
        FACE.RIGHT: (-1, -1, 1, 1),
        FACE.BACK: (1, -1, 1, -1),
        FACE.LEFT: (1, 1, -1, -1),
        FACE.TOP: (1, 1, 1, 1),
        FACE.BOTTOM: (1, 1, 1, 1),
    }

    _moves_shifts = {
        FACE.FRONT: (0,0,0,0,0,0,0,0,0,0,0,0),
        FACE.RIGHT:(6,6,2,2,-4,-4,-4,-4,0,0,0,0),
        FACE.LEFT:(4,4,4,4,-2,-2,-6,-6,0,0,0,0),
        FACE.BACK:(2,2,-2,-2,2,2,-2,-2,0,0,0,0),
        FACE.TOP:(0,0,0,0,6,6,2,2,-4,-4,-4,-4),
        FACE.BOTTOM:(0,0,0,0,4,4,4,4,-2,-2,-6,-6)
    }


    def __init__(self):
        self.cube = list(
            "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟦🟦🟦🟦🟦🟦🟦🟦🟦🟧🟧🟧🟧🟧🟧🟧🟧🟧⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨🟨🟨🟨🟨🟨"
        )
        self.total_moves = 0
        self.rotation = FACE.FRONT

    def face(self, face: FACE):
        start = face.value * 9
        end = start + 9
        return self.cube[start:end]

    def print_face(self, face_name, start_index):
        print(f"{face_name}:")
        for i in range(3):
            print(" ".join(self.cube[start_index + i * 3 : start_index + (i + 1) * 3]))
        print()

    def print_cube(self):
        # Represent the Rubik's Cube as a string
        self.print_face("Front", 0)
        self.print_face("Right", 9)
        self.print_face("Back", 18)
        self.print_face("Left", 27)
        self.print_face("Up", 36)
        self.print_face("Down", 45)

    def _get_adj_index(self, x, i):
        if x == 1:
            return i
        elif x == -1:
            return 2 - i
        
    def _spin_face_clockwise(self,face: FACE):
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]

    def _rotate_face_clockwise(self, face):
        # Rotate the specified face clockwise
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            index1 = self._get_adj_index(self._flip_colors_clockwise[face][0], i)
            index2 = self._get_adj_index(self._flip_colors_clockwise[face][1], i)
            index3 = self._get_adj_index(self._flip_colors_clockwise[face][2], i)
            index4 = self._get_adj_index(self._flip_colors_clockwise[face][3], i)
            self.cube[self._attached_indices[face][0][i]] = original_cube[
                self._attached_indices[face][1][index2]
            ]
            self.cube[self._attached_indices[face][1][i]] = original_cube[
                self._attached_indices[face][2][index3]
            ]
            self.cube[self._attached_indices[face][2][i]] = original_cube[
                self._attached_indices[face][3][index4]
            ]
            self.cube[self._attached_indices[face][3][i]] = original_cube[
                self._attached_indices[face][0][index1]
            ]

            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]

    def _spin_face_counter_clockwise(self,face: FACE):
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + j * 3 + (2 - i)]

    def _rotate_face_counter_clockwise(self, face: FACE):
        # Rotate the specified face counter-clockwise
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            index1 = self._get_adj_index(
                self._flip_colors_Counter_clockwise[face][0], i
            )
            index2 = self._get_adj_index(
                self._flip_colors_Counter_clockwise[face][1], i
            )
            index3 = self._get_adj_index(
                self._flip_colors_Counter_clockwise[face][2], i
            )
            index4 = self._get_adj_index(
                self._flip_colors_Counter_clockwise[face][3], i
            )
            self.cube[self._attached_indices[face][0][i]] = original_cube[
                self._attached_indices[face][3][index4]
            ]
            self.cube[self._attached_indices[face][3][i]] = original_cube[
                self._attached_indices[face][2][index3]
            ]
            self.cube[self._attached_indices[face][2][i]] = original_cube[
                self._attached_indices[face][1][index2]
            ]
            self.cube[self._attached_indices[face][1][i]] = original_cube[
                self._attached_indices[face][0][index1]
            ]
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + j * 3 + (2 - i)]

    def F(self):
        # Rotate the front face clockwise
        self._rotate_face_clockwise(FACE.FRONT)

    def F_prime(self):
        # Rotate the front face clockwise
        self._rotate_face_counter_clockwise(FACE.FRONT)

    def L(self):
        # Rotate the left face clockwise
        self._rotate_face_clockwise(FACE.LEFT)

    def L_prime(self):
        # Rotate the left face counterclockwise
        self._rotate_face_counter_clockwise(FACE.LEFT)

    def R(self):
        # Rotate the right face clockwise
        self._rotate_face_clockwise(FACE.RIGHT)

    def R_prime(self):
        # Rotate the right face counterclockwise
        self._rotate_face_counter_clockwise(FACE.RIGHT)

    def B(self):
        # Rotate the back face clockwise
        self._rotate_face_clockwise(FACE.BACK)

    def B_prime(self):
        # Rotate the back face counterclockwise
        self._rotate_face_counter_clockwise(FACE.BACK)

    def D(self):
        # Rotate the down face clockwise
        self._rotate_face_clockwise(FACE.BOTTOM)

    def D_prime(self):
        # Rotate the down face counterclockwise
        self._rotate_face_counter_clockwise(FACE.BOTTOM)

    def U(self):
        # Rotate the up face clockwise
        self._rotate_face_clockwise(FACE.TOP)

    def U_prime(self):
        # Rotate the up face counterclockwise
        self._rotate_face_counter_clockwise(FACE.TOP)

    def do_move(self, move):
        self.total_moves += 1
        match move:
            case 0:
                self.R()
                # print("R")
            case 1:
                self.R_prime()
                # print("R'")
            case 2:
                self.L()
                # print("L")
            case 3:
                self.L_prime()
                # print("L'")
            case 4:
                self.F()
                # print("F")
            case 5:
                self.F_prime()
                # print("F'")
            case 6:
                self.B()
                # print("B")
            case 7:
                self.B_prime()
                # print("B'")
            case 8:
                self.D()
                # print("D")
            case 9:
                self.D_prime()
                # print("D'")
            case 10:
                self.U()
                # print("U")
            case 11:
                self.U_prime()
                # print("U'")

    def undo_move(self, move):
        self.total_moves += 1
        match move:
            case 0:
                self.R_prime()
                # print("R")
            case 1:
                self.R()
                # print("R'")
            case 2:
                self.L_prime()
                # print("L")
            case 3:
                self.L()
                # print("L'")
            case 4:
                self.F_prime()
                # print("F")
            case 5:
                self.F()
                # print("F'")
            case 6:
                self.B_prime()
                # print("B")
            case 7:
                self.B()
                # print("B'")
            case 8:
                self.D_prime()
                # print("D")
            case 9:
                self.D()
                # print("D'")
            case 10:
                self.U_prime()
                # print("U")
            case 11:
                self.U()
                # print("U'")

    def make_move(self, move):
        move += self._moves_shifts[self.rotation][move]
        self.do_move(move)


    def rotate_y(self, times=1):
        # Normalize times to be within [0, 3] since 4 rotations = no rotation
        times = times % 4

        for _ in range(times):
            # Rotate FRONT -> RIGHT -> BACK -> LEFT
            front = self.cube[0:9]
            right = self.cube[9:18]
            back = self.cube[18:27]
            left = self.cube[27:36]

            self.cube[9:18] = front  # RIGHT = FRONT
            self.cube[18:27] = right  # BACK = RIGHT
            self.cube[27:36] = back   # LEFT = BACK
            self.cube[0:9] = left     # FRONT = LEFT

            # Rotate the TOP and BOTTOM faces
            self._spin_face_clockwise(FACE.TOP)
            self._spin_face_counter_clockwise(FACE.BOTTOM)

            # print(self._attached_faces[self.rotation][1])

    def rotate_x(self, times=1):
        # Normalize times to be within [0, 3] since 4 rotations = no rotation
        times = times % 4

        for _ in range(times):
            # Rotate TOP -> FRONT -> BOTTOM -> BACK
            top = self.cube[36:45]
            front = self.cube[0:9]
            bottom = self.cube[45:54]
            back = self.cube[18:27]

            self.cube[0:9] = top  # FRONT = TOP
            self.cube[45:54] = front  # BOTTOM = FRONT
            self.cube[18:27] = bottom  # BACK = BOTTOM
            self.cube[36:45] = back  # TOP = BACK

            # Rotate the LEFT and RIGHT faces
            self._spin_face_clockwise(FACE.LEFT)
            self._spin_face_counter_clockwise(FACE.RIGHT)


    def scramble(self, moves):
        for i in range(moves):
            move = rnd.randint(0, 11)
            self.make_move(move)

    def do_moves(self, moves):
        if isinstance(moves, int): self.make_move(moves )
        else:
            for move in moves:
                self.make_move(move)

    _color_to_int = {
        "🟩": 0,  # Green
        "🟥": 1,  # Red
        "🟦": 2,  # Blue
        "🟧": 3,  # Orange
        "⬜": 4,  # White
        "🟨": 5,  # Yellow
    }

    _color_to_str = {
        "🟩": 'G',  # Green
        "🟥": 'R',  # Red
        "🟦": 'B',  # Blue
        "🟧": 'O',  # Orange
        "⬜": 'W',  # White
        "🟨": "Y",  # Yellow
    }

    _letter_to_color = {
        'G': "🟩",
        'R': "🟥",
        'B': "🟦",
        'O': "🟧",
        'W': "⬜",
        'Y': "🟨",
    }

    def encode_to_cubestring(self):
        return [self._color_to_str[facelet] for facelet in self.cube]


    def is_solved(self):
        colors = ["🟩","🟥","🟦","🟧","⬜","🟨"]
        for i in range(6):
            face_start = 9*i
            for j in range(face_start,face_start+9):
                if self.cube[j] != colors[i]:
                    return False
        return True


    def hasWhiteCross(self):
        patter_positions = [(37,19,'🟦'),(41,10,'🟥'),(43,1,'🟩'),(39,28,'🟧')]

        for up_pos, adj_pos, adj_col in patter_positions:
            if self.cube[up_pos] != '⬜' or self.cube[adj_pos] != adj_col:
                return False
        return True


    def encode_state(self):
        """
        Encodes the current state of the Rubik's Cube as a list of integers.
        """
        return [self._color_to_int[facelet] for facelet in self.cube]
    
    def decode_state_num(self,state):
        int_to_color = {v: k for k, v in self._color_to_int.items()}
        cube_list = [int_to_color[i] for i in state]
        self.cube = cube_list
    
    def decode_state_lett(self,state):
        cube_list = [self._letter_to_color[l] for l in state]
        self.cube = cube_list

        
    

