from flask import Flask
from flask import jsonify
from flask import request
from kociemba import solve as kb_solve
from IDASolver import solve as ida_solver
from BFS_LBL import solve as lbl_solve

app=Flask(__name__)

@app.route('/kociemba',methods = ["GET"])
def kociemba_solver():
    try:
        cubesting = request.args.get('cubestring')
        r = kb_solve(cubesting)
        return jsonify(result = r), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/lbl', methods = ["GET"])
def lbl_solver():
    try:
        print(request.args)
        cubesting = request.args.get('cubestring')
        r = lbl_solve(cubesting)
        return jsonify(result = r), 200
    except Exception as e:
        import traceback
        return jsonify(error=str(e), traceback=traceback.format_exc()), 500


@app.route('/ml', methods = ["GET"])
def ml_solver():
    try:
        cubesting = request.args.get('cubestring')
        r = ida_solver(cubesting)
        return jsonify(result = r), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
if __name__ == "__main__":
    app.run()