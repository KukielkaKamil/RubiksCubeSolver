import numpy as np
import random as rnd

class RubiksCube:
    def __init__(self):
        # Initialize each face of the cube with colors
        self.front = np.array([['🟩' for _ in range(3)] for _ in range(3)])  # Green face
        self.back = np.array([['🟦' for _ in range(3)] for _ in range(3)])   # Blue face
        self.left = np.array([['🟧' for _ in range(3)] for _ in range(3)])   # Orange face
        self.right = np.array([['🟥' for _ in range(3)] for _ in range(3)])  # Red face
        self.up = np.array([['⬜' for _ in range(3)] for _ in range(3)])     # White face
        self.down = np.array([['🟨' for _ in range(3)] for _ in range(3)])   # Yellow face

    def __str__(self):
        # Represent the Rubik's Cube as a string
        cube_str = ""
        cube_str += "Front:\n" + self._format_face(self.front) + "\n"
        cube_str += "Back:\n" + self._format_face(self.back) + "\n"
        cube_str += "Left:\n" + self._format_face(self.left) + "\n"
        cube_str += "Right:\n" + self._format_face(self.right) + "\n"
        cube_str += "Up:\n" + self._format_face(self.up) + "\n"
        cube_str += "Down:\n" + self._format_face(self.down)
        return cube_str

    def _format_face(self, face):
        # Helper method to format each face for printing
        return "\n".join([" ".join(row) for row in face])

    def _rotate_face_clockwise(self, face):
        # Rotate the specified face clockwise
        face[:] = np.rot90(face, k=-1)
    
    def _rotate_face_counter_clockwise(self, face):
        # Rotate the specified face counterclockwise
        face[:] = np.rot90(face)

    def F(self):
        # Rotate the front face clockwise
        self._rotate_face_clockwise(self.front)
        
        # Rotate surrounding faces accordingly
        temp = np.copy(self.up[2, :])  # Store the top row of the top face
        self.up[2, :] = np.flip(self.left[:, 2])  # Set top row to the left column (reversed)
        self.left[:, 2] = self.down[0, :]  # Set left column to bottom row (reversed)
        self.down[0, :] = np.flip(self.right[:, 0])  # Set bottom row to right column
        self.right[:, 0] = temp  # Set right column to stored top row

    def F_prime(self):
        # Rotate the front face clockwise
        self._rotate_face_counter_clockwise(self.front)

        # Rotate surrounding faces accordingly
        temp = np.copy(self.up[2, :])  # Store the top row of the top face
        self.up[2, :] = self.right[:, 0]  # Set top row to the right column (reversed)
        self.right[:, 0] = np.flip(self.down[0, :])  # Set right column to bottom row (reversed)
        self.down[0, :] = self.left[:, 2]  # Set bottom row to left column
        self.left[:, 2] = np.flip(temp)  # Set left column to stored top row

    def L(self):
        # Rotate the left face clockwise
        self._rotate_face_clockwise(self.left)

        # Rotate surrounding faces accordingly
        temp_up = np.copy(self.up[:, 0])  # Store the leftmost column of the up face
        self.up[:, 0] = np.flip(self.back[:, 2])  # Set leftmost column of up face to front face (reversed)
        self.back[:, 2] = np.flip(self.down[:, 0])  # Set leftmost column of front face to down face
        self.down[:, 0] = self.front[:, 0] # Set leftmost column of down face to back face (reversed)
        self.front[:, 0] = temp_up  # Set leftmost column of back face to stored up face

    def L_prime(self):
        # Rotate the left face counterclockwise
        self._rotate_face_counter_clockwise(self.left)

        # Rotate surrounding faces accordingly
        temp_up = np.copy(self.up[:, 0])  # Store the leftmost column of the up face
        self.up[:, 0] = self.front[:, 0]  # Set leftmost column of up face to front face (reversed)
        self.front[:, 0] = self.down[:, 0]  # Set leftmost column of front face to down face
        self.down[:, 0] = np.flip(self.back[:, 2]) # Set leftmost column of down face to back face (reversed)
        self.back[:, 2] = np.flip(temp_up)  # Set leftmost column of back face to stored up face
    
    def R(self):
        # Rotate the right face clockwise
        self._rotate_face_clockwise(self.right)

        # Rotate surrounding faces accordingly
        temp_up = np.copy(self.up[:, 2])  # Store the rightmost column of the up face
        self.up[:, 2] = self.front[:, 2]  # Set rightmost column of up face to back face
        self.front[:, 2] = self.down[:, 2]  # Set rightmost column of back face to down face (reversed)
        self.down[:, 2] = np.flip(self.back[:, 0])  # Set rightmost column of down face to front face (reversed)
        self.back[:, 0] = np.flip(temp_up)  # Set rightmost column of front face to stored up face

    def R_prime(self):
        # Rotate the right face counterclockwise
        self._rotate_face_counter_clockwise(self.right)

        # Rotate surrounding faces accordingly
        temp_up = np.copy(self.up[:, 2])  # Store the rightmost column of the up face
        self.up[:, 2] = np.flip(self.back[:, 0])  # Set rightmost column of up face to back face
        self.back[:, 0] = np.flip(self.down[:, 2])  # Set rightmost column of back face to down face (reversed)
        self.down[:, 2] = self.front[:, 2]  # Set rightmost column of down face to front face (reversed)
        self.front[:, 2] = temp_up  # Set rightmost column of front face to stored up face

    def B(self):
        # Rotate the back face clockwise
        self._rotate_face_clockwise(self.back)

        # Rotate surrounding faces accordingly
        temp_up = np.copy(self.up[0, :])  # Store the top row of the up face
        self.up[0, :] = self.right[:, 2]  # Set top row of up face to right face (reversed)
        self.right[:, 2] = np.flip(self.down[2, :])  # Set rightmost column of right face to down face
        self.down[2, :] = self.left[:, 0]  # Set top row of down face to left face (reversed)
        self.left[:, 0] = np.flip(temp_up)  # Set leftmost column of left face to stored up face

    def B_prime(self):
        # Rotate the back face counterclockwise
        self._rotate_face_counter_clockwise(self.back)

        # Rotate surrounding faces accordingly
        temp_up = np.copy(self.up[0, :])  # Store the top row of the up face
        self.up[0, :] = np.flip(self.left[:, 0])  # Set top row of up face to right face (reversed)
        self.left[:, 0] = self.down[2, :]  # Set rightmost column of right face to down face
        self.down[2, :] = np.flip(self.right[:, 2]) # Set top row of down face to left face (reversed)
        self.right[:, 2] = temp_up  # Set leftmost column of left face to stored up face

    def D(self):
        # Rotate the down face clockwise
        self._rotate_face_clockwise(self.down)

        # Rotate surrounding faces accordingly
        temp_front = np.copy(self.front[2, :])  # Store the bottom row of the front face
        self.front[2, :] = self.left[2, :]  # Set bottom row of front face to right face (reversed)
        self.left[2, :] = self.back[2, :] # Set bottom row of right face to back face (reversed)
        self.back[2, :] = self.right[2, :]  # Set bottom row of back face to left face (reversed)
        self.right[2, :] = temp_front  # Set bottom row of left face to stored front face

    def D_prime(self):
        # Rotate the down face counterclockwise
        self._rotate_face_counter_clockwise(self.down)

        # Rotate surrounding faces accordingly
        temp_front = np.copy(self.front[2, :])  # Store the bottom row of the front face
        self.front[2, :] = (self.right[2, :])  # Set bottom row of front face to right face (reversed)
        self.right[2, :] = self.back[2, :] # Set bottom row of right face to back face (reversed)
        self.back[2, :] = self.left[2, :]  # Set bottom row of back face to left face (reversed)
        self.left[2, :] = temp_front  # Set bottom row of left face to stored front face

    def U(self):
        # Rotate the up face clockwise
        self._rotate_face_clockwise(self.up)

        # Rotate surrounding faces accordingly
        temp_front = np.copy(self.front[0, :])  # Store the bottom row of the front face
        self.front[0, :] = self.right[0, :]  # Set bottom row of front face to right face (reversed)
        self.right[0, :] = self.back[0, :] # Set bottom row of right face to back face (reversed)
        self.back[0, :] = self.left[0, :]  # Set bottom row of back face to left face (reversed)
        self.left[0, :] = temp_front

    def U_prime(self):
        # Rotate the up face counterclockwise
        self._rotate_face_counter_clockwise(self.up)

        # Rotate surrounding faces accordingly
        temp_front = np.copy(self.front[0, :])  # Store the bottom row of the front face
        self.front[0, :] = self.left[0, :]  # Set bottom row of front face to right face (reversed)
        self.left[0, :] = self.back[0, :] # Set bottom row of right face to back face (reversed)
        self.back[0, :] = self.right[0, :]  # Set bottom row of back face to left face (reversed)
        self.right[0, :] = temp_front  # Set bottom row of left face to stored front face
        
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