import rubicsCubeOLD as rb

cube = rb.RubiksCube()
cube.up[2][1] = '🟩'
cube.front[0][1] = '⬜'
cube.up[0][1] = '🟦'
cube.back[0][1] = '⬜'
print(cube)
def hasWhiteCross(cube):
#check for white cross
    if(cube.up[0][1] == cube.up[1][1] and cube.up[1][0] == cube.up[1][1] and cube.up[1][2] == cube.up[1][1]
       and cube.up[2][1] == cube.up[1][1] and cube.right[0][1] == cube.right[1][1] and cube.left[0][1] == cube.left[1][1]
       and cube.front[0][1] == cube.front[1][1] and cube.back[0][1] == cube.back[1][1]):
        print("HAS CROSS")
        return True
    else:
        print("NO CROSS")

def isWcs1(cube,face):
    if(face[2][1] == cube.front[1][1] and face[0][1] == cube.up[1][1]):
        return True
    
def doWcs1Front(cube):
    cube.F()
    cube.U_prime()
    cube.R()
    cube.U()

def doWcs1Right(cube):
    cube.R()
    cube.U_prime()
    cube.B()
    cube.U()

def doWcs1Back(cube):
    cube.B()
    cube.U_prime()
    cube.L()
    cube.U()

def doWcs1Left(cube):
    cube.L()
    cube.U_prime()
    cube.F()
    cube.U()
    

# while(not hasWhiteCross(cube)):
#     if(isWcs1(cube,cube.front)):
#         doWcs1Front(cube)
if(isWcs1(cube,cube.back)):
    print("TAK")
# print(cube)
