from enum import Enum
import numpy as np
class FACE(Enum):
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    TOP = 4
    BOTTOM = 5

class RubiksCube:
    _atached_faces = {
        FACE.FRONT : (FACE.BOTTOM,FACE.RIGHT,FACE.TOP,FACE.LEFT)
    }
    def __init__(self):
        self.cube = list("🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟦🟦🟦🟦🟦🟦🟦🟦🟦🟧🟧🟧🟧🟧🟧🟧🟧🟧⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨🟨🟨🟨🟨🟨")
    
    def face(self, face : FACE):
        start = face.value * 9
        end = start + 9
        return self.cube[start:end]
    
    def _rotate_face_clockwise(self, face):
        # Rotate the specified face clockwise
        start = face.value * 9
        end = start + 9
        original_face = self.cube[start:end]
        original_cube = self.cube.copy()
        for i in range(3):
            bottom_index = self._atached_faces[face][0].value * 9 + i
            right_index =(self._atached_faces[face][1].value * 9) + i +(2 * i)
            top_index = (self._atached_faces[face][2].value * 9) + i + 6
            left_index = (self._atached_faces[face][3].value * 9) + 2 +(3 * i)
            self.cube[bottom_index] = original_cube[right_index - (6 * (i-1))]
            self.cube[right_index] = original_cube[top_index]
            self.cube[top_index] = original_cube[left_index - (6 * (i-1))]
            self.cube[left_index] = original_cube[bottom_index]

            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]
        
    def _rotate_face_counter_clockwise(self, face:FACE):
        start = face.value * 9
        end = start + 9
        original_face = self.cube[start:end]

        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_face[(2 - i) + 3 * j]
# cube = RubiksCube()
# cube._rotate_face_clockwise(FACE.FRONT)
# # print(len(cube.cube))
# print(cube.face(FACE.FRONT))
# print(cube.face(FACE.TOP))
# print(cube.face(FACE.RIGHT))
# print(cube.face(FACE.BOTTOM))
# print(cube.face(FACE.LEFT))
# print(cube._atached_faces[FACE.FRONT][1])