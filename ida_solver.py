import RubiksCube as rc
import kociemba_utils as kcu
from copy import copy,deepcopy
import sqlite3
from depth_predictor import predict_depth

class State:
    def __init__(self,state:rc.RubiksCube,parent=None,cost=0,heuristic=0):
        self.state=state
        self.parent=parent
        self.cost=cost #g(n) cost from the A* algorithm
        self.heuristic = heuristic #h(n) cost from the A* algorithm

    def __lt__(self,other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

_correct_corners = {
    (0,29,42):('🟩','🟧','⬜'),
    (2,9,44):('🟩','🟥','⬜'),
    (6,35,45):('🟩','🟧','🟨'),
    (8,15,47):('🟩','🟥','🟨'),
    (18,11,38):('🟦','🟥','⬜'),
    (20,27,36):('🟦','🟧','⬜'),
    (24,17,53):('🟦','🟥','🟨'),
    (26,33,51):('🟦','🟧','🟨')
}

_correct_edges = {
    (1,43):('🟩','⬜'),
    (3,32):('🟩','🟧'),
    (5,12):('🟩','🟥'),
    (7,46):('🟩','🟨'),
    (10,41):('🟥','⬜'),
    (14,21):('🟥','🟦'),
    (16,50):('🟥','🟨'),
    (19,37):('🟦','⬜'),
    (23,30):('🟦','🟧'),
    (25,52):('🟦','🟨'),
    (28,39):('🟧','⬜'),
    (34,48):('🟧','🟨')
}


#CAn reorient those later so that 1 and 2 are switched



# def phase1_heuristic_value(cube):

#     correct_count = 0

#     # Check each corner
#     for (i,j,l),colors in _correct_corners.items():
#         current_corner = (cube[i],cube[j],cube[l])
#         if current_corner != colors:
#             correct_count += 1

#     # Check each edge
#     for (i,j),colors in _correct_edges.items():
#         current_edge = (cube[i],cube[j])
#         if current_edge != colors:
#             correct_count += 1

#     return correct_count
    
import sqlite3

def phase1_heuristic_value(cube):
    # Assuming kcu functions return orientation states
    _, corner_state = kcu.check_corner_orientation(cube)
    _, edge_state = kcu.check_edges_orientation(cube)
    slice_state = kcu.get_ud_slice_point(cube)
    
    depth = predict_depth(edge_state,corner_state,slice_state)
    return depth
    
def is_phase1_goal(cube):

    corner_state, _ = kcu.check_corner_orientation(cube)
    edge_state, _ = kcu.check_edges_orientation(cube)
    slice_state = kcu.get_ud_slice_point(cube)
    # print(f'Current states: {corner_state} {edge_state} {slice_state}')
    return corner_state == 0 and edge_state == 0 and slice_state == 0


def encode_cube(cube: rc.RubiksCube) -> list:
    return cube.cube

def decode_to_cube(encoded_state: list) -> rc.RubiksCube:
    cube = rc.RubiksCube()
    cube.cube = deepcopy(encoded_state)
    return cube


# cb.do_move(1)
# cb.do_move(2)
# cb.print_cube()

# print(phase1_heuristic_value(cb.cube))
# def get_succesors_phase1(state:rc.RubiksCube):
#     succesors = []
#     # moves = [0,1,2,3,4,5,6,7,8,9,10,11,(0,0),(2,2),(4,4),(6,6),(8,8),(10,10)]
#     moves=[0,2,4,6,8,10]
#     for move in moves:
#         next_state = deepcopy(state)
#         # print("NEXT STATE __________________________________-")
#         next_state.do_moves(move)
#         cost = 1
#         succesors.append((next_state,cost))
#     return succesors

def get_succesors_phase1(state: rc.RubiksCube, last_move=None):
    successors = []
    # Moves that should be avoided based on the previous move
    inverse_moves = {0: 1, 2: 3, 4: 5, 6: 7, 8: 9, 10: 11}
    allowed_moves = [0, 2, 4, 6, 8, 10] if last_move is None else [m for m in [0, 2, 4, 6, 8, 10] if m != inverse_moves.get(last_move, -1)]
    
    for move in allowed_moves:
        next_state = deepcopy(state)
        next_state.do_moves(move)
        cost = 1
        successors.append((next_state, cost, move))  # Add move information for pruning
    return successors


def phase1(root,goal,phase1_heuristic_value):
    def search(state:State,g,bound):
        # print(state.heuristic)
        f = g + state.heuristic
        print(state.heuristic)
        if f > bound:
            return f
        if is_phase1_goal(state.state.cube):
            return state
        min_treshold = float('inf')
        for succesor, cost, m in get_succesors_phase1(state.state):
            succesor_state = State(succesor,state,g+cost,phase1_heuristic_value(succesor.cube))
            result = search(succesor_state, g+cost, bound)
            if isinstance(result, State):
                return result
            if result < min_treshold:
                min_treshold = result
        return min_treshold
    
    bound = phase1_heuristic_value(root.state.cube)
    while True:
        result = search(root,1,bound)
        if isinstance(result,State):
            return result
        if result == float('inf'):
            return None #NO solution found
        bound = result

def reconstruct_moves(state:State):
    path = []
    while state:
        path.append(state.state)
        state = state.parent
    return path[::-1]

cb = rc.RubiksCube()
goal = rc.RubiksCube().cube
cb.scramble(7)
# cb.do_moves([1,3])
cb.total_moves=0
cb2 = copy(cb)
# cb.make_move(0)



root_state = State(cb,heuristic=phase1_heuristic_value(cb.cube))
# check_edges_orientation(cb.cube)
# print(binomal_coefficient(1,2))
# s = get_succesors_phase1(root_state.state)
# for c in s: c[0].print_cube()
# root_state.state.print_cube()

goal_state = phase1(root_state,goal,phase1_heuristic_value)
print(goal_state.state.total_moves)

if goal_state:
    print("MAMY TO")
else:
    print("Szukaj dalej")

