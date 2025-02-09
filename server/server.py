from flask import Flask, jsonify, request
from kociemba import solve as kb_solve
from IDASolver import solve as ida_solver
from BFS_LBL import solve as lbl_solve
from network_discovery import ServerDiscovery
import threading

app = Flask(__name__)
discovery = ServerDiscovery()

# Start discovery server in a separate thread
discovery_thread = threading.Thread(target=discovery.start_discovery_server, daemon=True)
discovery_thread.start()

@app.route('/kociemba', methods=["GET"])
def kociemba_solver():
    try:
        cubestring = request.args.get('cubestring')
        r = kb_solve(cubestring)
        return jsonify(result=r), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/lbl', methods=["GET"])
def lbl_solver():
    try:
        print(request.args)
        cubestring = request.args.get('cubestring')
        r = lbl_solve(cubestring)
        return jsonify(result=r), 200
    except Exception as e:
        import traceback
        return jsonify(error=str(e), traceback=traceback.format_exc()), 500

@app.route('/ml', methods=["GET"])
def ml_solver():
    try:
        cubestring = request.args.get('cubestring')
        r = ida_solver(cubestring)
        return jsonify(result=r), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')  # Allow external connections