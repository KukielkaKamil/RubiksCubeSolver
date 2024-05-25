import RubiksCube as rb

cube = rb.RubiksCube()
faces = rb.FACE

# Checking if cube has white cross
def hasWhiteCross(cube):
    patter_positions = [(37,19,'🟦'),(41,10,'🟥'),(43,1,'🟩'),(39,28,'🟧')]

    for up_pos, adj_pos, adj_col in patter_positions:
        print(cube.cube[up_pos])
        print(cube.cube[adj_pos])
        print(adj_col)
        if cube.cube[up_pos] != '⬜' or cube.cube[adj_pos] != adj_col:
            return False
    return True

# Check and solves a scenario needed for solving white crosss
def wc_patter_1(cube):
    patter_positions =[(37,19,'🟦'),(41,10,'🟥'),(43,1,'🟩'),(39,28,'🟧')]
    moves = [(6,11,2,10),(0,11,6,10),(4,11,0,10),(4,11,0,10)]

    for index, (up_pos, adj_pos, up_col) in enumerate(patter_positions):
        if cube.cube[up_pos] == up_col or cube.cube[adj_pos] == '⬜':
            for move in moves[index]:
                cube.make_move(move)
            return True
    return False

# Testin

cube.cube[43] = '🟩'
cube.cube[1] = '⬜'

print(cube.face(faces.TOP))
print(cube.face(faces.FRONT))

wc_patter_1(cube)

print(cube.face(faces.TOP))
print(cube.face(faces.FRONT))
