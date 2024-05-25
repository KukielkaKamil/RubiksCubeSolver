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
        FACE.FRONT : (FACE.BOTTOM,FACE.RIGHT,FACE.TOP,FACE.LEFT),
        FACE.RIGHT : (FACE.BOTTOM, FACE.BACK,FACE.TOP,FACE.FRONT),
        FACE.BACK : (FACE.BOTTOM, FACE.LEFT, FACE.TOP, FACE.RIGHT),
        FACE.LEFT : (FACE.BOTTOM,FACE.FRONT, FACE.TOP, FACE.BACK),
        FACE.TOP : (FACE.FRONT, FACE.RIGHT, FACE.BACK, FACE.LEFT),
        FACE.BOTTOM : (FACE.BACK, FACE.RIGHT, FACE.FRONT, FACE.LEFT)
    }
    _attached_indices = {
        FACE.FRONT:[(45,46,47),(9,12,15),(42,43,44),(29,32,35)],
        FACE.RIGHT:[(47,50,53),(20,23,26),(42,43,44),(2,5,8)],
        FACE.BACK:[(51,52,53),(27,30,33),(36,37,38),(11,14,17)],
        FACE.LEFT:[(45,48,51),(0,3,6),(36,39,42),(18,21,24)],
        FACE.TOP:[(0,1,2),(9,10,11),(18,19,20),(27,28,29)],
        FACE.BOTTOM:[(24,25,26),(15,16,17),(6,7,8),(33,34,35)]
    }
    def __init__(self):
        self.cube = list("🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟦🟦🟦🟦🟦🟦🟦🟦🟦🟧🟧🟧🟧🟧🟧🟧🟧🟧⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨🟨🟨🟨🟨🟨")
    
    def face(self, face : FACE):
        start = face.value * 9
        end = start + 9
        return self.cube[start:end]
    
    def print_face(self, face_name, start_index):
        print(f"{face_name}:")
        for i in range(3):
            print(" ".join(self.cube[start_index + i*3:start_index + (i+1)*3]))
        print()
            
    
    def print_cube(self):
        # Represent the Rubik's Cube as a string
        self.print_face("Front", 0)
        self.print_face("Right", 9)
        self.print_face("Back", 18)
        self.print_face("Left", 27)
        self.print_face("Up", 36)
        self.print_face("Down", 45)
    
    def _rotate_face_clockwise(self, face):
        # Rotate the specified face clockwise
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            self.cube[self._attached_indices[face][0][i]] = original_cube[self._attached_indices[face][1][-1 * (i+1)]]
            self.cube[self._attached_indices[face][1][i]] = original_cube[self._attached_indices[face][2][i]]
            self.cube[self._attached_indices[face][2][i]] = original_cube[self._attached_indices[face][3][-1 * (i+1)]]
            self.cube[self._attached_indices[face][3][i]] = original_cube[self._attached_indices[face][0][i]]

            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]
        
    def _rotate_face_counter_clockwise(self, face:FACE):
        # Rotate the specified face counter-clockwise
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            self.cube[self._attached_indices[face][0][i]] = original_cube[(self._attached_indices[face][3][-1 * (i+1)])]
            self.cube[self._attached_indices[face][3][i]] = original_cube[self._attached_indices[face][2][i]]
            self.cube[self._attached_indices[face][2][i]] = original_cube[self._attached_indices[face][1][-1 * (i+1)]]
            self.cube[self._attached_indices[face][1][i]] = original_cube[self._attached_indices[face][0][i]]
    
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
    
    def make_move(self, move):
        match move:
            case 0:
                self.R()
                print('R')
            case 1:
                self.R_prime()
                print('R\'')
            case 2:
                self.L()
                print('L')
            case 3:
                self.L_prime()
                print('L\'')
            case 4:
                self.F()
                print('F')
            case 5:
                self.F_prime()
                print('F\'')
            case 6:
                self.B()
                print('B')
            case 7:
                self.B_prime()
                print('B\'')
            case 8:
                self.D()
                print('D')
            case 9:
                self.D_prime()
                print('D\'')
            case 10:
                self.U()
                print('U')
            case 11:
                self.U_prime()
                print('U\'')

    def scramble(self, moves):
        for i in range(moves):
            move = rnd.randint(0,11)
            self.make_move(move)