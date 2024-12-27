from flask import Flask
from flask import jsonify
from flask import request
from kociemba import solve as kb_solve
from IDASolver import IDAStarSolver
from BFS_LBL import solve as lbl_solve

app=Flask(__name__)

@app.route('/kociemba',methods = ["GET"])
def kociemba_solver():
    # request_data = request.get_json()
    cubesting = request.args.get('cubestring')
    r = kb_solve(cubesting)
    return jsonify(result = r)

@app.route('/lbl', methods = ["GET"])
def lbl_solver():
    cubesting = request.args.get('cubestring')
    r = lbl_solve(cubesting)
    return jsonify(result = r)

@app.route('/ml', methods = ["GET"])
def ml_solver():
    solver = IDAStarSolver()
    cubesting = request.args.get('cubestring')
    r = solver.solve(cubesting)
    pass

app.run()