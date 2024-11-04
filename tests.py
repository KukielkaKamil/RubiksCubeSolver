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
def hasWhiteEdge(cube):
    # Define positions and colors for one white edge configuration
    pattern_positions = [(37, 19, '🟦'), (41, 10, '🟥'), (43, 1, '🟩'), (39, 28, '🟧')]
    correct_cubies = 0
    for up_pos, adj_pos, adj_col in pattern_positions:
        if cube.cube[up_pos] == '⬜' and cube.cube[adj_pos] == adj_col:
            correct_cubies += 1
            print(f"Found white edge at position {up_pos} with correct adjacent color at {adj_pos}.")
    return correct_cubies


# Breadth-First Search for solving any one white edge
# def solve_white_edge_bfs(cube):
#     queue = deque([(deepcopy(cube), [])])
#     visited = set()

#     while queue:
#         current_cube, move_sequence = queue.popleft()

#         # Check if the goal is achieved
#         if hasWhiteEdge(current_cube):
#             # If `move_sequence` is empty, it means the initial state solved the puzzle
#             print("Solution found with moves:", move_sequence if move_sequence else "No moves needed (initial state)")
            
#             # Apply the found solution moves to the original cube and return the move sequence
#             for move in move_sequence:
#                 if isinstance(move, tuple):  # If it's a sequence, apply each move in it
#                     for sub_move in move:
#                         cube.make_move(sub_move)
#                 else:
#                     cube.make_move(move)

#             return move_sequence if move_sequence else []  # Return the sequence of moves (or empty if already solved)

#         # Continue BFS if not already solved at initial state
#         cube_state_hash = hash(tuple(current_cube.cube))
#         if cube_state_hash in visited:
#             continue
#         visited.add(cube_state_hash)

#         # Generate next states using both individual moves and move sequences
#         for move in available_moves:
#             next_cube = deepcopy(current_cube)  # Make a copy of the current cube
#             if isinstance(move, tuple):  # If move is a sequence
#                 for sub_move in move:
#                     next_cube.make_move(sub_move)
#             else:  # If move is a single integer move
#                 next_cube.make_move(move)

#             new_move_sequence = move_sequence + [move]
#             queue.append((next_cube, new_move_sequence))

#     print("No solution found.")
#     return None

def is_goal(cube,goal_state):
    match goal_state:
        case 0: #One white cross cubie
            print("Checkig goal")
            return hasWhiteEdge(cube) >= 1
            

def solve_with_bfs(cube, available_moves, goal_state):
    queue = deque([(deepcopy(cube), [])])
    visited = set()

    while queue:
        current_cube, move_sequence = queue.popleft()

        if is_goal(current_cube,goal_state):
            print("Solution found with moves:", move_sequence if move_sequence else "No moves needed (initial state)")
            
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




# Run BFS to solve one white edge
solution_moves = solve_with_bfs(cube,available_moves_1,0)

# Output the solution moves if found
if solution_moves:
    print("Solution moves:", solution_moves)
    print("Total moves:", len(solution_moves))
else:
    print("No solution found.")  # This line is unlikely to be reached
