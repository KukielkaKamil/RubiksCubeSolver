import RubiksCube as rb
from collections import deque
from copy import deepcopy

cube = rb.RubiksCube()
cube.scramble(100)
cube.total_moves = 0

# Moves available, with a mix of single moves and sequences
available_moves_1 = [0,1,2,3,4,5,6,7,8,9,10,11,
                   (4,11,0,10),(0,11,6,10),(6,11,2,10),(4,11,0,10),
                   (0,5,1),(6,1,7),(2,7,3),(4,3,5),
                   (3,4,2),(5,0,4),(1,6,0),(7,2,6),
                   (4, 4),(1, 8, 0, 5)]

# Function to check if any one white edge piece is in the correct position
def has_white_cross(cube):
    # Define positions and colors for one white edge configuration
    pattern_positions = [(37, 19, '🟦'), (41, 10, '🟥'), (43, 1, '🟩'), (39, 28, '🟧')]
    correct_cubies = 0
    for up_pos, adj_pos, adj_col in pattern_positions:
        if cube.cube[up_pos] == '⬜' and cube.cube[adj_pos] == adj_col:
            correct_cubies += 1
            # print(f"Found white edge at position {up_pos} with correct adjacent color at {adj_pos}.")
    return correct_cubies

def has_white_face(cube):
    correct_corners_postions = [(44,2,9,'🟩', '🟥'), (42,0,29,'🟩', '🟧'), (36,27,20,'🟧', '🟦'), (38,18,11,'🟦', '🟥')]
    correct_corners = 0
    for i,j,l,color1, color2 in correct_corners_postions:
        if cube.cube[i] == '⬜' and cube.cube[j] == color1 and cube.cube[l] == color2:
            correct_corners += 1
    return correct_corners

def has_second_layer(cube):
    correct_positions = [(5,12,'🟩', '🟥'), (14,21, '🟥','🟦'), (23,30, '🟦','🟧'), (3,32,'🟩', '🟧')]
    correct_cubies = 0
    for i,j,color1, color2 in correct_positions:
        if cube.cube[i] == color1 and cube.cube[j] == color2:
            correct_cubies += 1
    return correct_cubies

def has_yellow_cross(cube):
    cross_positions = [46,48,50,52]
    correct_cubies = 0
    for pos in cross_positions:
        if cube.cube[pos] == '🟨':
            correct_cubies += 1
            # print(f"Found white edge at position {up_pos} with correct adjacent color at {adj_pos}.")
    return correct_cubies

def has_full_white_cross(cube):
    positions=[(7,'🟩'),(16,'🟥'),(25,'🟦'),(34,'🟧')]
    correct_cubies = 0
    for pos, color in positions:
        if cube.cube[pos] == color:
            correct_cubies += 1
    return correct_cubies

def has_correct_corner_positions(cube):
    positions = [(45,6,35),(47,8,15),(53,17,24),(51,26,33)]
    colors = [('🟨','🟩','🟧'),('🟨','🟩','🟥'),('🟨','🟥','🟦'),('🟨','🟦','🟧')]
    correct_cubies = 0
    for i in range(4):
        cube_colors = (cube.cube[positions[i][0]], cube.cube[positions[i][1]],cube.cube[positions[i][2]])
        if sorted(cube_colors) == sorted (colors[i]):
            correct_cubies += 1
    return correct_cubies

def is_solved(cube):
    positions = [(45,6,35,'🟨','🟩','🟧'),(47,8,15,'🟨','🟩','🟥'),(53,17,24,'🟨','🟥','🟦'),(51,26,33,'🟨','🟦','🟧')]
    correct_cubies = 0
    for i,j,l,c1,c2,c3 in positions:
        if cube.cube[i] == c1 and cube.cube[j] == c2 and cube.cube[l] == c3:
            correct_cubies += 1
    return correct_cubies


def is_goal(cube,goal_state):
    match goal_state:
        case 0: #One white cross cubie
            return has_white_cross(cube) >= 1
        case 1:
            return has_white_cross(cube) >= 2
        case 2:
            return has_white_cross(cube) >= 3
        case 3:
            return has_white_cross(cube) >= 4
        case 4:
            return has_white_face(cube) >=1 and has_white_cross(cube) >= 4
        case 5:
            return has_white_face(cube) >=2 and has_white_cross(cube) >= 4
        case 6:
            return has_white_face(cube) >=3 and has_white_cross(cube) >= 4
        case 7:
            return has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 8:
            return has_second_layer(cube) >= 1 and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 9:
            return has_second_layer(cube) >= 2 and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 10:
            return has_second_layer(cube) >= 3 and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 11:
            return has_second_layer(cube) >= 4 and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 12:
            return has_yellow_cross(cube) >= 4 and has_second_layer(cube) >= 4 \
            and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 13:
            return has_full_white_cross(cube) >= 4 and has_yellow_cross(cube) >= 4 and has_second_layer(cube) >= 4 \
            and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 14:
            return has_correct_corner_positions(cube) >= 4 \
            and has_full_white_cross(cube) >= 4 and has_yellow_cross(cube) >= 4 and has_second_layer(cube) >= 4 \
            and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
        case 15:
            return is_solved(cube) and has_correct_corner_positions(cube) >= 4 \
            and has_full_white_cross(cube) >= 4 and has_yellow_cross(cube) >= 4 and has_second_layer(cube) >= 4 \
            and has_white_face(cube) >=4 and has_white_cross(cube) >= 4
            
        
            

def solve_with_bfs(cube, available_moves, goal_state):
    queue = deque([(deepcopy(cube), [])])
    visited = set()

    while queue:
        current_cube, move_sequence = queue.popleft()

        if is_goal(current_cube,goal_state):
            # print("Solution found with moves:", move_sequence if move_sequence else "No moves needed (initial state)")
            
            # Apply the found solution moves to the original cube and return the move sequence
            for move in move_sequence:
                if isinstance(move, tuple):  # If it's a sequence, apply each move in it
                    for sub_move in move:
                        cube.make_move(sub_move)
                else:
                    cube.make_move(move)

            return move_sequence if move_sequence else []  # Return the sequence of moves (or empty if already solved)
        
        # Continue BFS if not already solved at initial state
        cube_state_hash = hash(tuple(current_cube.cube))
        if cube_state_hash in visited:
            continue
        visited.add(cube_state_hash)

        # Generate next states using both individual moves and move sequences
        for move in available_moves:
            next_cube = deepcopy(current_cube)  # Make a copy of the current cube
            if isinstance(move, tuple):  # If move is a sequence
                for sub_move in move:
                    next_cube.make_move(sub_move)
            else:  # If move is a single integer move
                next_cube.make_move(move)

            new_move_sequence = move_sequence + [move]
            queue.append((next_cube, new_move_sequence))

    print("No solution found.")
    return None




# # Run BFS to solve one white edge
# solution_moves_1 = solve_with_bfs(cube,available_moves_1,0)

# # Output the solution moves if found
# if solution_moves_1:
#     print("Solution moves:", solution_moves_1)
#     print("Total moves:", len(solution_moves_1))
# else:
#     print("No moves needed (initial state)")  # This line is unlikely to be reached

# solution_moves_2 = solve_with_bfs(cube,available_moves_1,1)

# # Output the solution moves if found
# if solution_moves_2:
#     print("Solution moves:", solution_moves_2)
#     print("Total moves:", len(solution_moves_2))
# else:
#     print("No moves needed (initial state)") # This line is unlikely to be reached

# solution_moves_3 = solve_with_bfs(cube,available_moves_1,2)

# # Output the solution moves if found
# if solution_moves_3:
#     print("Solution moves:", solution_moves_3)
#     print("Total moves:", len(solution_moves_3))
# else:
#     print("No moves needed (initial state)")



# solution_moves_4 = solve_with_bfs(cube,available_moves_1,3)

# # Output the solution moves if found
# if solution_moves_4:
#     print("Solution moves:", solution_moves_4)
#     print("Total moves:", len(solution_moves_4))
# else:
#     print("No moves needed (initial state)")



available_moves_2 = [0,1,2,3,4,5,6,7,8,9,10,11,
                     (4,8,5),(0,8,1),(2,8,3),(6,8,7),
                     (1,8,8,0,8,1,9,0),(3,8,8,2,8,3,9,2),(5,8,8,4,8,5,9,4),(7,8,8,6,8,7,9,6),
                     (1,9,0,8),(3,9,2,8),(5,9,4,8),(7,9,6,8)]

# solution_moves_5 = solve_with_bfs(cube,available_moves_2,4)

# # Output the solution moves if found
# if solution_moves_5:
#     print("Solution moves:", solution_moves_5)
#     print("Total moves:", len(solution_moves_5))
# else:
#     print("No moves needed (initial state)")

# solution_moves_6 = solve_with_bfs(cube,available_moves_2,5)

# # Output the solution moves if found
# if solution_moves_6:
#     print("Solution moves:", solution_moves_6)
#     print("Total moves:", len(solution_moves_6))
# else:
#     print("No moves needed (initial state)")

# solution_moves_7 = solve_with_bfs(cube,available_moves_2,6)

# # Output the solution moves if found
# if solution_moves_7:
#     print("Solution moves:", solution_moves_7)
#     print("Total moves:", len(solution_moves_7))
# else:
#     print("No moves needed (initial state)")

# solution_moves_8 = solve_with_bfs(cube,available_moves_2,7)

# # Output the solution moves if found
# if solution_moves_8:
#     print("Solution moves:", solution_moves_8)
#     print("Total moves:", len(solution_moves_8))
# else:
#     print("No moves needed (initial state)")


available_moves_3 = [(9,1,8,0,8,4,9,5),(9,7,8,6,8,0,9,1),(9,7,8,6,8,2,9,3),(9,5,8,4,8,3,9,2),
(8,2,9,3,9,5,8,4),(8,6,9,7,9,3,8,2),(8,0,9,1,9,7,8,6),(8,4,9,5,9,1,8,0),(8,8)]

# solution_moves_9 = solve_with_bfs(cube,available_moves_3,8)

# # Output the solution moves if found
# if solution_moves_9:
#     print("Solution moves:", solution_moves_9)
#     print("Total moves:", len(solution_moves_9))
# else:
#     print("No moves needed (initial state)")

# solution_moves_10 = solve_with_bfs(cube,available_moves_3,9)

# # Output the solution moves if found
# if solution_moves_10:
#     print("Solution moves:", solution_moves_10)
#     print("Total moves:", len(solution_moves_10))
# else:
#     print("No moves needed (initial state)")

# solution_moves_11 = solve_with_bfs(cube,available_moves_3,10)

# # Output the solution moves if found
# if solution_moves_11:
#     print("Solution moves:", solution_moves_11)
#     print("Total moves:", len(solution_moves_11))
# else:
#     print("No moves needed (initial state)")

# solution_moves_12 = solve_with_bfs(cube,available_moves_3,11)

# # Output the solution moves if found
# if solution_moves_12:
#     print("Solution moves:", solution_moves_12)
#     print("Total moves:", len(solution_moves_12))
# else:
#     print("No moves needed (initial state)")

available_moves_4 = [(4,2,8,3,9,5),8,9]
available_moves_5 = [(2,8,3,8,2,8,8,3,8),(2,8,3,8,2,8,8,3)] # to adjust
available_moves_6 = [(8,2,9,1,8,3,9,0)]
available_moves_7 = [(3,11,2,10),8,9]

for goal_state in range(16):

    current_moveset = available_moves_1
    if goal_state > 3:
        current_moveset = available_moves_2
    if goal_state > 7:
        current_moveset = available_moves_3
    if goal_state > 11:
        current_moveset = available_moves_4
    if goal_state > 12:
        current_moveset = available_moves_5
    if goal_state > 13:
        current_moveset = available_moves_6
    if goal_state > 14:
        current_moveset = available_moves_7


    solution_moves = solve_with_bfs(cube,current_moveset,goal_state)
    
    if solution_moves:
        print(f"Solution moves for goal state {goal_state}:", solution_moves)
        print("Total moves:", len(solution_moves))
    else:
        print(f"No moves needed for goal state {goal_state} (initial state)")
cube.print_cube()
