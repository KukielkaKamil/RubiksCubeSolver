import RubiksCube as rb
import random as rnd

cube = rb.RubiksCube()
faces = rb.FACE
cube.scramble(100)
available_moves = [0,1,2,3,4,5,6,7,8,9]
block_moves = {
        '🟩': (4,5),
        '🟥':(0,1),
        '🟦':(6,7),
        '🟧':(2,3)
    }
# Checking if cube has white cross
def hasWhiteCross(cube):
    patter_positions = [(37,19,'🟦'),(41,10,'🟥'),(43,1,'🟩'),(39,28,'🟧')]

    for up_pos, adj_pos, adj_col in patter_positions:
        if cube.cube[up_pos] != '⬜' or cube.cube[adj_pos] != adj_col:
            return False
    return True

# Check and solves a scenario needed for solving white crosss
def wc_simple_patterns(cube):
    patter_positions =[(12,5,'🟩'),(46,7,'🟩'),(32,3,'🟩'),(21,14,'🟥'),(50,16,'🟥'),(5,12,'🟥'),
                       (30,23,'🟦'),(52,25,'🟦'),(14,21,'🟦'),(3,32,'🟧'),(48,34,'🟧'),(23,30,'🟧')]
    moves = [(5,),(4,4),(4,),(1,),(0,0),(0,),(7,),(6,6),(6,),(3,),(2,2),(2,)]

    for index, (white_pos, adj_pos, adj_col) in enumerate(patter_positions):
        if cube.cube[white_pos] == '⬜' and cube.cube[adj_pos] == adj_col:
            for move in moves[index]:
                cube.make_move(move)
            for bmove in block_moves[adj_col]:
                if bmove in available_moves:
                    available_moves.remove(bmove)
                return True
    return False

def wc_pattern_1(cube):
    patter_positions =[(43,1,'🟩'),(41,10,'🟥'),(37,19,'🟦'),(39,28,'🟧')]
    moves = [(4,11,0,10),(0,11,6,10),(6,11,2,10),(4,11,0,10)]

    for index, (up_pos, adj_pos, up_col) in enumerate(patter_positions):
        if cube.cube[up_pos] == up_col and cube.cube[adj_pos] == '⬜':
            for move in moves[index]:
                cube.make_move(move)
            for bmove in block_moves[up_col]:
                if bmove in available_moves:
                    available_moves.remove(bmove)
            return True
    return False

def wc_pattern_2(cube):
    patter_positions =[(16,50,'🟩'),(25,52,'🟥'),(34,48,'🟦'),(7,46,'🟧')]
    moves = [(0,5,1),(6,1,7),(2,7,3),(4,3,5)]

    for index, (up_pos, adj_pos, adj_col) in enumerate(patter_positions):
        if cube.cube[adj_pos] == adj_col and cube.cube[up_pos] == '⬜':
            for move in moves[index]:
                cube.make_move(move)
            for bmove in block_moves[adj_col]:
                if bmove in available_moves:
                    available_moves.remove(bmove)
            return True
    return False

def wc_pattern_3(cube):
    patter_positions =[(34,48,'🟩'),(7,46,'🟥'),(16,50,'🟦'),(25,48,'🟧')]
    moves = [(3,4,2),(5,0,4),(1,6,0),(7,2,6)]

    for index, (up_pos, adj_pos, adj_col) in enumerate(patter_positions):
        if cube.cube[adj_pos] == adj_col and cube.cube[up_pos] == '⬜':
            for move in moves[index]:
                cube.make_move(move)
            for bmove in block_moves[adj_col]:
                if bmove in available_moves:
                    available_moves.remove(bmove)
            return True
    return False
##More Patterns/better logic to be added

max = 100
moves = 0
while not hasWhiteCross(cube):
    moves += 1
    if moves >= max:
        cube.print_cube()
        print("Nie udało się")
        break
    elif wc_pattern_1(cube):
        continue
    elif wc_pattern_2(cube):
        continue
    elif wc_pattern_3(cube):
        continue
    elif wc_simple_patterns(cube):
        continue
    else:
        x = rnd.randint(0,len(available_moves)-1)
        cube.make_move(available_moves[x])
        # cube.scramble(1)

cube.print_cube()