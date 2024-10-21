import twophase.solver as sv

# cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
def solve(cubestring):
    solution = sv.solve(cubestring,19,0)
    return solution