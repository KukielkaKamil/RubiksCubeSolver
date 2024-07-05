import old_stuff.rubicsCubeOLD as rb
import random as rnd

cube = rb.RubiksCube()
cube.scramble(10)
print(cube)
def hasWhiteCross(cube):
#check for white cross
    if(cube.up[0][1] == cube.up[1][1] and cube.up[1][0] == cube.up[1][1] and cube.up[1][2] == cube.up[1][1]
       and cube.up[2][1] == cube.up[1][1] and cube.right[0][1] == cube.right[1][1] and cube.left[0][1] == cube.left[1][1]
       and cube.front[0][1] == cube.front[1][1] and cube.back[0][1] == cube.back[1][1]):
        # print("HAS CROSS")
        return True
        # print("NO CROSS")

def isWcs1(cube, face_name):
    if face_name == "front":
        return cube.up[2][1] == cube.front[1][1] and cube.front[0][1] == cube.up[1][1]
    elif face_name == "right":
        return cube.up[1][2] == cube.right[1][1] and cube.right[1][0] == cube.up[1][1]
    elif face_name == "back":
        return cube.up[0][1] == cube.back[1][1] and cube.back[2][1] == cube.up[1][1]
    elif face_name == "left":
        return cube.up[1][0] == cube.left[1][1] and cube.left[1][2] == cube.up[1][1]

def doWcs1(cube, face_name):
    if face_name == "front":
        cube.F()
        cube.U_prime()
        cube.R()
        cube.U()
    elif face_name == "right":
        cube.R()
        cube.U_prime()
        cube.B()
        cube.U()
    elif face_name == "back":
        cube.B()
        cube.U_prime()
        cube.L()
        cube.U()
    elif face_name == "left":
        cube.L()
        cube.U_prime()
        cube.F()
        cube.U()

    
while(not hasWhiteCross(cube)):
    if(isWcs1(cube,"front")):
        doWcs1(cube,"front")
    elif(isWcs1(cube,"right")):
        doWcs1(cube,"right")
    elif(isWcs1(cube,"back")):
        doWcs1(cube,"back")
    elif(isWcs1(cube,"left")):
        doWcs1(cube,"left")
    else:
        move = rnd.randint(0,11)
        cube.make_move(move)
print(cube)
