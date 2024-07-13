import RubiksCube as rb
import random as rnd

cube = rb.RubiksCube()
faces = rb.FACE
cube.scramble(100)
cube.total_moves=0

cross_edges={
    (7,46): (),
    (34,48):(8,),
    (16,50):(9,),
    (25,52):(8,8),
    (5,12):(1,9,0),
    (3,32):(2,8,3),
    (23,30):(3,8,2),
    (21,14):(0,9,1),
    (39,28):(3,3,8),
    (41,10):(1,1,9),
    (37,19):(6,6,8,8),
    (43,1):(4,4)
}


# Checking if cube has white cross
def hasWhiteCross(cube):
    patter_positions = [(37,19,'🟦'),(41,10,'🟥'),(43,1,'🟩'),(39,28,'🟧')]

    for up_pos, adj_pos, adj_col in patter_positions:
        if cube.cube[up_pos] != '⬜' or cube.cube[adj_pos] != adj_col:
            return False
    return True

def solve_cross(cube):
    colors = ['🟩', '🟧', '🟦','🟥']

    for color in colors:
        for (i, j), values in cross_edges.items():
            if (cube.cube[i], cube.cube[j]) in [('⬜', color), (color, '⬜')]:
                cube.do_moves(values)
                # cube.print_cube()

                if cube.cube[46] == '⬜':
                    cube.do_moves((4, 4))
                else:
                    cube.do_moves((1, 8, 0, 5))
                    
                cube.make_move(11)
                cube.print_cube()
                break
        
print("START")
solve_cross(cube)
print("KONIEC")
cube.print_cube()

print("Wszystkie ruchy: ",cube.total_moves)