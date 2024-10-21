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
    orientation_sum = 0
    i = 6  # Starting from 6 for the orientation index
    
    for (x, y, z) in _corner_orientation.keys():
        current_corner = (cube[x], cube[y], cube[z])
        for correct_colors in _corner_orientation.values():
            if sorted(current_corner) == sorted(correct_colors):
                orientation_index = correct_colors.index(cube[x])
                corner_sum += orientation_index
                orientation_sum += orientation_index * (3 ** i)  # Multiply orientation index by 3^i
                i -= 1  # Decrease i after each iteration
                break
    
    return corner_sum, orientation_sum

_edges_orientation = {
    (43,1):('⬜','🟩'),
    (3,32):('🟩','🟧'),
    (5,12):('🟩','🟥'),
    (46,7):('🟨','🟩'),
    (41,10):('⬜','🟥'),
    # (21,14):('🟦','🟥'),
    (50,16):('🟨','🟥'),
    (37,19):('⬜','🟦'),
    (23,30):('🟦','🟧'),
    (52,25):('🟨','🟦'),
    (39,28):('⬜','🟧'),
    (48,34):('🟨','🟧')
}

def check_edges_orientation(cube):
    edge_sum = 0
    orientation_sum = 0
    i = 10  # Starting from 10 for the orientation index

    for (x, y) in _edges_orientation.keys():
        current_edge = (cube[x], cube[y])
        for correct_colors in _edges_orientation.values():
            if sorted(current_edge) == sorted(correct_colors):
                orientation_index = correct_colors.index(cube[x])
                edge_sum += orientation_index
                orientation_sum += orientation_index * (2 ** i)  # Multiply orientation index by 2^i
                i -= 1  # Decrease i after each iteration
                break
    
    return edge_sum, orientation_sum


def factorial(n:int) -> int:
    result = 1
    for i in range(1,n+1):
        result *= i
    return result


def binomal_coefficient(n:int ,k:int) -> int:
    return factorial(n) / (factorial(k)*factorial(n-k))

def get_ud_slice_positions(cube):
    ud_slices=[('🟩','🟥'),('🟥','🟦'),('🟦','🟧'),('🟧','🟩')]
    ud_positions=[(14, 21), (23, 30), (3, 32), (5, 12), (25, 52), (34, 48), (7, 46), (16, 50), (37, 19), (39, 28), (1, 43), (41, 10)]
    ud_points=[]
    index = len(ud_positions)-1
    found=3
    for i,j in ud_positions:
        if found < 0 : return ud_points
        edge = (cube[i],cube[j])
        if any(sorted(edge) == sorted(t) for t in ud_slices):
            found -= 1
            index -= 1
            continue
        if found > 0:
            ud_points.append((index,found))
        index -= 1
    return ud_points

def get_ud_slice_point(cube):
    positions = get_ud_slice_positions(cube)
    if len(positions) <= 0: return 0
    sum = 0
    for n,k in positions:
        sum += binomal_coefficient(n,k)
    return sum
    
