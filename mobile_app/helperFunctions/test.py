import random as rnd
from enum import Enum


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
        FACE.TOP: [(0, 1, 2), (9, 10, 11), (18, 19, 20), (27, 28, 29)],
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
        FACE.FRONT: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        FACE.RIGHT: (6, 6, 2, 2, -4, -4, -4, -4, 0, 0, 0, 0),
        FACE.LEFT: (4, 4, 4, 4, -2, -2, -6, -6, 0, 0, 0, 0),
        FACE.BACK: (2, 2, -2, -2, 2, 2, -2, -2, 0, 0, 0, 0),
        FACE.TOP: (0, 0, 0, 0, 6, 6, 2, 2, -4, -4, -4, -4),
        FACE.BOTTOM: (0, 0, 0, 0, 4, 4, 4, 4, -2, -2, -6, -6)
    }

    def __init__(self):
        # Face order: FRONT(0)=Green, RIGHT(1)=Red, BACK(2)=Blue,
        #             LEFT(3)=Orange, TOP(4)=White, BOTTOM(5)=Yellow
        self.cube = list(
            "🟩🟩🟩"
            "🟩🟩🟩"
            "🟩🟩🟩"  # FRONT (0..8)

            "🟥🟥🟥"
            "🟥🟥🟥"
            "🟥🟥🟥"  # RIGHT (9..17)

            "🟦🟦🟦"
            "🟦🟦🟦"
            "🟦🟦🟦"  # BACK (18..26)

            "🟧🟧🟧"
            "🟧🟧🟧"
            "🟧🟧🟧"  # LEFT (27..35)

            "⬜⬜⬜"
            "⬜⬜⬜"
            "⬜⬜⬜"   # TOP (36..44)

            "🟨🟨🟨"
            "🟨🟨🟨"
            "🟨🟨🟨"  # BOTTOM (45..53)
        )
        self.total_moves = 0
        self.rotation = FACE.FRONT

    # -------------------------------------------------------------------------
    # Basic methods to read / print faces
    # -------------------------------------------------------------------------
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
        self.print_face("Front", 0)
        self.print_face("Right", 9)
        self.print_face("Back", 18)
        self.print_face("Left", 27)
        self.print_face("Up", 36)
        self.print_face("Down", 45)

    # -------------------------------------------------------------------------
    # Internal helpers for spinning faces
    # -------------------------------------------------------------------------
    def _get_adj_index(self, x, i):
        if x == 1:
            return i
        elif x == -1:
            return 2 - i

    def _spin_face_clockwise(self, face: FACE):
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]

    def _spin_face_counter_clockwise(self, face: FACE):
        start = face.value * 9
        original_cube = self.cube.copy()
        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + j * 3 + (2 - i)]

    def _rotate_face_clockwise(self, face):
        # Rotate the specified face clockwise + adjust adjacent strips
        start = face.value * 9
        original_cube = self.cube.copy()

        # Rotate adjacent edges
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

        # Rotate the face itself
        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + (2 - j) * 3 + i]

    def _rotate_face_counter_clockwise(self, face: FACE):
        # Rotate the specified face counter-clockwise + adjust adjacent strips
        start = face.value * 9
        original_cube = self.cube.copy()

        # Rotate adjacent edges
        for i in range(3):
            index1 = self._get_adj_index(self._flip_colors_Counter_clockwise[face][0], i)
            index2 = self._get_adj_index(self._flip_colors_Counter_clockwise[face][1], i)
            index3 = self._get_adj_index(self._flip_colors_Counter_clockwise[face][2], i)
            index4 = self._get_adj_index(self._flip_colors_Counter_clockwise[face][3], i)

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

        # Rotate the face itself
        for i in range(3):
            for j in range(3):
                self.cube[start + i * 3 + j] = original_cube[start + j * 3 + (2 - i)]

    # -------------------------------------------------------------------------
    # Face-turns
    # -------------------------------------------------------------------------
    def F(self):
        self._rotate_face_clockwise(FACE.FRONT)

    def F_prime(self):
        self._rotate_face_counter_clockwise(FACE.FRONT)

    def L(self):
        self._rotate_face_clockwise(FACE.LEFT)

    def L_prime(self):
        self._rotate_face_counter_clockwise(FACE.LEFT)

    def R(self):
        self._rotate_face_clockwise(FACE.RIGHT)

    def R_prime(self):
        self._rotate_face_counter_clockwise(FACE.RIGHT)

    def B(self):
        self._rotate_face_clockwise(FACE.BACK)

    def B_prime(self):
        self._rotate_face_counter_clockwise(FACE.BACK)

    def D(self):
        self._rotate_face_clockwise(FACE.BOTTOM)

    def D_prime(self):
        self._rotate_face_counter_clockwise(FACE.BOTTOM)

    def U(self):
        self._rotate_face_clockwise(FACE.TOP)

    def U_prime(self):
        self._rotate_face_counter_clockwise(FACE.TOP)

    # -------------------------------------------------------------------------
    # Move helpers
    # -------------------------------------------------------------------------
    def do_move(self, move):
        self.total_moves += 1
        match move:
            case 0:  self.R()
            case 1:  self.R_prime()
            case 2:  self.L()
            case 3:  self.L_prime()
            case 4:  self.F()
            case 5:  self.F_prime()
            case 6:  self.B()
            case 7:  self.B_prime()
            case 8:  self.D()
            case 9:  self.D_prime()
            case 10: self.U()
            case 11: self.U_prime()

    def undo_move(self, move):
        self.total_moves += 1
        match move:
            case 0:  self.R_prime()
            case 1:  self.R()
            case 2:  self.L_prime()
            case 3:  self.L()
            case 4:  self.F_prime()
            case 5:  self.F()
            case 6:  self.B_prime()
            case 7:  self.B()
            case 8:  self.D_prime()
            case 9:  self.D()
            case 10: self.U_prime()
            case 11: self.U()

    def make_move(self, move):
        move += self._moves_shifts[self.rotation][move]
        self.do_move(move)

    # -------------------------------------------------------------------------
    # Rotations
    # -------------------------------------------------------------------------
    def rotate_y(self, times=1):
        times = times % 4
        for _ in range(times):
            front = self.cube[0:9]
            right = self.cube[9:18]
            back = self.cube[18:27]
            left = self.cube[27:36]

            self.cube[9:18] = front
            self.cube[18:27] = right
            self.cube[27:36] = back
            self.cube[0:9] = left

            self._spin_face_clockwise(FACE.TOP)
            self._spin_face_counter_clockwise(FACE.BOTTOM)

    def rotate_x(self, times=1):
        times = times % 4
        for _ in range(times):
            top = self.cube[36:45]
            front = self.cube[0:9]
            bottom = self.cube[45:54]
            back = self.cube[18:27]

            self.cube[0:9] = top
            self.cube[45:54] = front
            self.cube[18:27] = bottom
            self.cube[36:45] = back

            self._spin_face_clockwise(FACE.LEFT)
            self._spin_face_counter_clockwise(FACE.RIGHT)

    # -------------------------------------------------------------------------
    # Scramble helpers
    # -------------------------------------------------------------------------
    def scramble(self, moves):
        for i in range(moves):
            move = rnd.randint(0, 11)
            self.make_move(move)

    def do_moves(self, moves):
        if isinstance(moves, int):
            self.make_move(moves)
        else:
            for move in moves:
                self.make_move(move)

    # -------------------------------------------------------------------------
    # Encoding / Decoding states
    # -------------------------------------------------------------------------
    _color_to_int = {
        "🟩": 0,  # Green
        "🟥": 1,  # Red
        "🟦": 2,  # Blue
        "🟧": 3,  # Orange
        "⬜": 4,  # White
        "🟨": 5,  # Yellow
    }

    _color_to_str = {
        "🟩": 'G',
        "🟥": 'R',
        "🟦": 'B',
        "🟧": 'O',
        "⬜": 'W',
        "🟨": 'Y',
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
            for j in range(face_start, face_start+9):
                if self.cube[j] != colors[i]:
                    return False
        return True

    def encode_state(self):
        return [self._color_to_int[facelet] for facelet in self.cube]

    def decode_state_num(self, state):
        int_to_color = {v: k for k, v in self._color_to_int.items()}
        cube_list = [int_to_color[i] for i in state]
        self.cube = cube_list

    def decode_state_lett(self, state):
        cube_list = [self._letter_to_color[l] for l in state]
        self.cube = cube_list

    # -------------------------------------------------------------------------
    # Step 1) Color Count Verification
    # -------------------------------------------------------------------------
    def verify_color_distribution(self):
        """
        Checks that there are exactly 9 facelets of each color.
        Returns:
            True if correct, or an error message if wrong.
        """
        color_count = {}
        for facelet in self.cube:
            color_count[facelet] = color_count.get(facelet, 0) + 1

        for color in ["🟩","🟥","🟦","🟧","⬜","🟨"]:
            if color_count.get(color, 0) != 9:
                return f"Error: Expected 9 of {color}, found {color_count.get(color, 0)}"
        return True

    # -------------------------------------------------------------------------
    # Step 2) Full Physical Solvability Check
    # -------------------------------------------------------------------------
    def verify_full_physical(self):
        """
        Verifies that the cube is physically solvable by:
          - Identifying each corner piece (which corner, orientation).
          - Identifying each edge piece (which edge, flip).
          - Checking orientation sums and permutation parity.
        Returns:
            "CUBE_OK" if solvable, or error message if invalid.
        """

        # A) index helper
        def idx(f, r, c):
            return f * 9 + r * 3 + c

        # B) Convert emojis to letters
        emoji_to_letter = {
            "🟩": "G",
            "🟥": "R",
            "🟦": "B",
            "🟧": "O",
            "⬜": "W",
            "🟨": "Y",
        }
        try:
            facelets = [emoji_to_letter[c] for c in self.cube]
        except KeyError:
            return "Error: Cube has invalid color(s)."

        # C) Corner definitions that match this code's default orientation
        #    corner_slots[0] => triplet of (face, row, col) for corner #0, etc.
        #    We'll read them in the exact order that yields (W,O,G) for corner #0, etc.
        corner_slots = [
            # corner #0: top-left-front
            ((4,2,0),(3,0,2),(0,0,0)),  # -> 'W','O','G'
            # corner #1: top-right-front
            ((4,2,2),(0,0,2),(1,0,0)),  # -> 'W','G','R'
            # corner #2: top-right-back
            ((4,0,2),(1,0,2),(2,0,0)),  # -> 'W','R','B'
            # corner #3: top-left-back
            ((4,0,0),(2,0,2),(3,0,0)),  # -> 'W','B','O'

            # corner #4: bottom-left-front
            ((5,0,0),(0,2,0),(3,2,2)),  # -> 'Y','G','O'
            # corner #5: bottom-right-front
            ((5,0,2),(1,2,0),(0,2,2)),  # -> 'Y','R','G'
            # corner #6: bottom-right-back
            ((5,2,2),(2,2,0),(1,2,2)),  # -> 'Y','B','R'
            # corner #7: bottom-left-back
            ((5,2,0),(3,2,0),(2,2,2)),  # -> 'Y','O','B'
        ]
        corner_solved_colors = [
            ("W","O","G"), # corner 0
            ("W","G","R"), # corner 1
            ("W","R","B"), # corner 2
            ("W","B","O"), # corner 3
            ("Y","G","O"), # corner 4
            ("Y","R","G"), # corner 5
            ("Y","B","R"), # corner 6
            ("Y","O","B"), # corner 7
        ]

        # D) Edge definitions
        #    We'll define each edge so the code sees exactly the pair it
        #    reads in the solved state. 
        edge_slots = [
            # 0: top-front => 'W','G'
            ((4,2,1),(0,0,1)),
            # 1: top-right => 'W','R'
            ((4,1,2),(1,0,1)),
            # 2: top-back  => 'W','B'
            ((4,0,1),(2,0,1)),
            # 3: top-left  => 'W','O'
            ((4,1,0),(3,0,1)),

            # 4: left-front => 'O','G'
            ((3,1,2),(0,1,0)),
            # 5: right-front => 'R','G'
            ((1,1,0),(0,1,2)),
            # 6: right-back => 'R','B'
            ((1,1,2),(2,1,0)),
            # 7: left-back => 'O','B'
            ((3,1,0),(2,1,2)),

            # 8: bottom-front => 'Y','G'
            ((5,0,1),(0,2,1)),
            # 9: bottom-right => 'Y','R'
            ((5,1,2),(1,2,1)),
            # 10: bottom-back => 'Y','B'
            ((5,2,1),(2,2,1)),
            # 11: bottom-left => 'Y','O'
            ((5,1,0),(3,2,1)),
        ]
        edge_solved_colors = [
            ("W","G"), # #0
            ("W","R"), # #1
            ("W","B"), # #2
            ("W","O"), # #3
            ("O","G"), # #4
            ("R","G"), # #5
            ("R","B"), # #6
            ("O","B"), # #7
            ("Y","G"), # #8
            ("Y","R"), # #9
            ("Y","B"), # #10
            ("Y","O"), # #11
        ]

        def rotate_left(tup):
            return tup[1:] + tup[:1]

        # E) Corner ID
        corner_perm = [-1]*8
        corner_orient = [0]*8
        used_corners = set()

        for slot_idx, corner_def in enumerate(corner_slots):
            c_list = [facelets[idx(f,r,c)] for (f,r,c) in corner_def]
            found_trip = tuple(c_list)

            matched_corner = None
            matched_orient = None
            for corner_id, solved_trip in enumerate(corner_solved_colors):
                if set(found_trip) == set(solved_trip):
                    trial = solved_trip
                    for orientation in [0,1,2]:
                        if trial == found_trip:
                            matched_corner = corner_id
                            matched_orient = orientation
                            break
                        trial = rotate_left(trial)
                    if matched_corner is not None:
                        break

            if matched_corner is None:
                return f"Error: Corner at slot {slot_idx} has invalid color combo {found_trip}"
            if matched_corner in used_corners:
                return f"Error: Corner {matched_corner} appears more than once!"
            used_corners.add(matched_corner)

            corner_perm[slot_idx] = matched_corner
            corner_orient[slot_idx] = matched_orient

        # F) Edge ID
        edge_perm = [-1]*12
        edge_flip = [0]*12
        used_edges = set()

        for slot_idx, edge_def in enumerate(edge_slots):
            c1 = facelets[idx(edge_def[0][0], edge_def[0][1], edge_def[0][2])]
            c2 = facelets[idx(edge_def[1][0], edge_def[1][1], edge_def[1][2])]
            found_pair = (c1, c2)

            matched_edge = None
            matched_flip = None
            for edge_id, solved_pair in enumerate(edge_solved_colors):
                if set(found_pair) == set(solved_pair):
                    if found_pair == solved_pair:
                        matched_edge = edge_id
                        matched_flip = 0
                    else:
                        matched_edge = edge_id
                        matched_flip = 1
                    break

            if matched_edge is None:
                return f"Error: Edge at slot {slot_idx} has invalid color pair {found_pair}"
            if matched_edge in used_edges:
                return f"Error: Edge {matched_edge} appears more than once!"
            used_edges.add(matched_edge)

            edge_perm[slot_idx] = matched_edge
            edge_flip[slot_idx] = matched_flip

        # G) Orientation sums
        if sum(corner_orient) % 3 != 0:
            return "Error: Corner orientation sum is not divisible by 3."
        if sum(edge_flip) % 2 != 0:
            return "Error: Edge flip sum is not even."

        # H) Permutation parity
        def permutation_parity(perm):
            inv_count = 0
            for i in range(len(perm)):
                for j in range(i+1, len(perm)):
                    if perm[i] > perm[j]:
                        inv_count += 1
            return inv_count % 2

        cp = permutation_parity(corner_perm)
        ep = permutation_parity(edge_perm)
        if cp != ep:
            return "Error: Corner parity and edge parity do not match."

        return "CUBE_OK"

    # -------------------------------------------------------------------------
    # Step 3) Master verify() that calls both checks
    # -------------------------------------------------------------------------
    def verify(self):
        # 1) color distribution
        check_cd = self.verify_color_distribution()
        if check_cd is not True:
            return check_cd

        # 2) full physical
        result = self.verify_full_physical()
        return result


# --------------------- Demo Usage ---------------------
if __name__ == "__main__":
    cube = RubiksCube()
    print("Is it solved?", cube.is_solved())  
    print("Verification on new cube =>", cube.verify())  # Expect "CUBE_OK"

    # Let's scramble
    cube.scramble(10)
    print("\nScrambled => Is solved?", cube.is_solved())
    print("Verification =>", cube.verify())
