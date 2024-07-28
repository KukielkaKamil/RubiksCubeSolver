import RubiksCube as rb
import random as rnd

cube = rb.RubiksCube()
faces = rb.FACE
cube.scramble(100)
cube.total_moves=0

fl_cross_edges={
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

fl_corners={
    (0,42,29):(2,8,3),
    (2,44,9):(1,9,0,8),
    (6,45,35):(8,),
    (8,47,15):(),
    (18,38,11):(7,9,6),
    (20,36,27):(3,8,8,2),
    (24,53,17):(9,),
    (26,51,33):(8,8)

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
        for (i, j), values in fl_cross_edges.items():
            if (cube.cube[i], cube.cube[j]) in [('⬜', color), (color, '⬜')]:
                cube.do_moves(values)
                # cube.print_cube()

                if cube.cube[46] == '⬜':
                    cube.do_moves((4, 4))
                else:
                    cube.do_moves((1, 8, 0,  5))
                    
                cube.make_move(11)
                # cube.print_cube()
                break

def correct_corner(i, j, l, color1, color2):
    corner = {cube.cube[i], cube.cube[j], cube.cube[l]}
    colors = {'⬜', color1, color2}
    return corner == colors


def solve_corners(cube):
    colors = [('🟩', '🟥'), ('🟩', '🟧'), ('🟧', '🟦'), ('🟦', '🟥')]
    for color1, color2 in colors:
        for (i, j, l), values in fl_corners.items():
            if correct_corner(i, j, l, color1, color2):
                print(f"Found corner at positions {i}, {j}, {l} with colors: {cube.cube[i]}, {cube.cube[j]}, {cube.cube[l]}")
                cube.do_moves(values)

                if cube.cube[8] == '⬜':
                    cube.do_moves((4, 8, 5))
                elif cube.cube[47] == '⬜':
                    cube.do_moves((1, 8, 8, 0, 8, 1, 9, 0))
                else:
                   print("mamy elsea")
                   while cube.cube[44] != '⬜' or cube.cube[1] != cube.cube[2] or cube.cube[9] != cube.cube[10]:
                        cube.do_moves((1, 9, 0, 8))
                        print("Performing a cycle")
                        cube.print_cube()

                break  # Move to the next set of colors once the current corner is solved
        cube.print_cube()
        cube.make_move(11)

        
print("START")
solve_cross(cube)
solve_corners(cube)
print("KONIEC")
cube.print_cube()

print("Wszystkie ruchy: ",cube.total_moves)