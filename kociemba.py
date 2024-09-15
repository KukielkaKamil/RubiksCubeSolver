import RubiksCube as rc
from copy import copy,deepcopy


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
_corner_orientation = {
    (42,0,29):('⬜','🟩','🟧'),
    (44,9,2):('⬜','🟥','🟩'),
    (45,35,6):('🟨','🟧','🟩'),
    (47,8,15):('🟨','🟩','🟥',),
    (38,18,11):('⬜','🟦','🟥'),
    (36,20,27):('⬜','🟦','🟧'),
    # (53,17,24):('🟨','🟥','🟦'), It is not necessary (math :p)
    (51,26,33):('🟨','🟦','🟧')

}

def check_corner_orientation(cube):
    corner_sum = 0
    for (i,j,l) in _corner_orientation.keys():
        current_corner = (cube[i], cube[j], cube[l])
        for correct_colors in _corner_orientation.values():
            if sorted(current_corner) == sorted(correct_colors):
                orientation_index = correct_colors.index(cube[i])
                corner_sum += orientation_index
                break
    return corner_sum


def phase1_heuristic_value(cube):

    correct_count = 0

    # Check each corner
    for (i,j,l),colors in _correct_corners.items():
        current_corner = (cube[i],cube[j],cube[l])
        if current_corner != colors:
            correct_count += 1

    # Check each edge
    for (i,j),colors in _correct_edges.items():
        current_edge = (cube[i],cube[j])
        if current_edge != colors:
            correct_count += 1

    return correct_count
    


# cb.do_move(1)
# cb.do_move(2)
# cb.print_cube()

# print(phase1_heuristic_value(cb.cube))

def get_succesors_phase1(state:rc.RubiksCube):
    succesors = []
    moves = [0,1,2,3,4,5,6,7,8,9,10,11,(0,0),(2,2),(4,4),(6,6),(8,8),(10,10)]
    for move in moves:
        next_state = deepcopy(state)
        # print("NEXT STATE __________________________________-")
        next_state.do_moves(move)
        cost = 1
        succesors.append((next_state,cost))
    return succesors

def phase1(root,goal,phase1_heuristic_value):
    def search(state:State,g,bound):
        f = g + state.heuristic
        if f > bound:
            return f
        if check_corner_orientation(state.state.cube) == 0:
            return state
        min_treshold = float('inf')
        for succesor, cost in get_succesors_phase1(state.state):
            succesor_state = State(succesor,state,g+cost,phase1_heuristic_value(succesor.cube))
            result = search(succesor_state, g+cost, bound)
            if isinstance(result, State):
                return result
            if result < min_treshold:
                min_treshold = result
        return min_treshold
    
    bound = phase1_heuristic_value(root.state.cube)
    while True:
        result = search(root,20,bound)
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
cb.scramble(100)
# cb.do_moves([1,3])
cb.total_moves=0
cb2 = copy(cb)


root_state = State(cb,heuristic=phase1_heuristic_value(cb.cube))
check_corner_orientation(cb.cube)
# s = get_succesors_phase1(root_state.state)
# for c in s: c[0].print_cube()
# root_state.state.print_cube()

goal_state = phase1(root_state,goal,phase1_heuristic_value)
print(goal_state.state.total_moves)

if goal_state:
    print("MAMY TO")
else:
    print("Szukaj dalej")
