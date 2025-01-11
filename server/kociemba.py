import twophase.solver as sv
import re

# cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
cubestring2 = 'RRRGGGGGGBBBRRRRRROOOBBBBBBGGGOOOOOOWWWWWWWWWYYYYYYYYY'
def solve(cubestring):
    cubestring = kociemba_cube(cubestring)
    solution = sv.solve(cubestring,19,0)
    moves_list = moves_to_list(solution)
    return moves_list

moves_translations ={
    'R': 'F',
    'R`': 'F`',
    'L': 'B',
    'L`': 'B`',
    'F': 'R',
    'F`': 'R`',
    'B': 'L',
    'B`': 'L`',
    'U' : 'D`',
    'U`': 'D',
    'D': 'U`',
    'D`': 'U'
}

def moves_to_list(moves):
    # print(moves)
    moves = re.sub(r"\(.*?\)", "", moves).strip()
    moves = moves.split()

    result = []

    for move in moves:
        move_name = move[0]
        move_count = int(move[1]) if len(move) > 1 else 1
        result.extend([move_name] * move_count)
    return result

#converts the default cube str to one that this algorithm accepts
def kociemba_cube(input_str):

    starting_indexes=[36,9,0,45,27,18]
    #Step 1 reorder faces
    new_str=''
    for i in range(6):
        start = starting_indexes[i]
        end = start+9
        # print(input_str[start:end])
        new_str += input_str[start:end]

    print(new_str)
    
    # Step 2: Transform the string
    transform_dict = {'G': 'F', 'R': 'R', 'B': 'B', 'O': 'L', 'W': 'U', 'Y': 'D'}
    transformed_str = ''.join([transform_dict[char] for char in new_str])
    print(transformed_str)
    
    return transformed_str

if __name__ == '__main__':

    moves_to_do = 'U3 (1f)'
    # print(moves_to_list(moves_to_do))

    import RubiksCube as rb
    from copy import deepcopy
    moves_to_do = 'U3 (1f)'
    # print(moves_to_list(moves_to_do))
    tc = rb.RubiksCube()
    tc.scramble(20)
    solve_cube = deepcopy(tc)
    test2 = "".join(tc.encode_to_cubestring())
    print(test2)
    moves = solve(test2)
    print(moves)

    move_table={
    'R': 0,
    'R`': 1,
    'L': 2,
    'L`': 3,
    'F': 4,
    'F`': 5,
    'B': 6,
    'B`': 7,
    'D' : 8,
    'D`': 9,
    'U': 10,
    'U`': 11
}
    solve_cube.print_cube()
    for m in moves:
        solve_cube.do_move(move_table[m])
        print(m)
    solve_cube.print_cube()