from flask import Flask
from flask import jsonify
from flask import request
from kociemba import solve

app=Flask(__name__)

@app.route('/kociemba',methods = ["GET"])
def kociemba_solver():
    # request_data = request.get_json()
    cubesting = request.args.get('cubestring')
    r = solve(cubesting)
    return jsonify(result = r)

app.run()