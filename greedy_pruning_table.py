import kociemba_utils as ku
import RubiksCube as rb
import sqlite3
from collections import deque
from copy import deepcopy
from multiprocessing import Pool, Manager, Lock
from filequeue import FileQueue
import random

MAX_DEPTH = 12
NUM_CORES = 7  # Adjust based on your machine's capabilities
DB_PATH = 'kociemba_pruning_phase1_tests.db'
QUEUE_PATH = 'state_queue'  # Path where the queue will be stored
MOVES = [0,1,2,3,4,5,6,7,8,9,10,11]
OPPOSITE_MOVES = {
    0: 1, 1: 0,
    2: 3, 3: 2,
    4: 5, 5: 4,
    6: 7, 7: 6,
    8: 9, 9: 8,
    10: 11, 11: 10
}

def insert_into_db(lock, edge_state, corner_state, slice_state, depth, db_path):
    with lock:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO pruning_table (edge_state, corner_state, slice_state, depth) VALUES (?,?,?,?)",
                       (edge_state, corner_state, slice_state, depth))
        conn.commit()
        conn.close()

def encode_cube(cube: rb.RubiksCube) -> list:
    return cube.cube

def decode_to_cube(encoded_state: list) -> rb.RubiksCube:
    cube = rb.RubiksCube()
    cube.cube = deepcopy(encoded_state)
    return cube

def state_already_visited(edge_state, corner_state, slice_state, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pruning_table WHERE edge_state = ? AND corner_state = ? AND slice_state = ? LIMIT 1",
                   (edge_state, corner_state, slice_state))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def process_state_chunk(start_state, depth_range, lock, db_path, moves, queue_path):
    start_encoded = encode_cube(start_state)
    
    # Initialize FileQueue, specifying the path where the queue data will be stored
    queue = FileQueue(0)

    # Start by putting the initial state into the file-based queue
    queue.put((start_encoded, 0,None,0))
    
    while not queue.empty():
        state, depth, last_move, consecutive_moves_count = queue.get()  # Get from FileQueue
        decoded_state = decode_to_cube(state)
        
        if depth > MAX_DEPTH:
            continue

        rand = random.randint(0,100)

        if rand < 90 and depth > 2:
            # print(f"OUT {state}")
            continue
        print(f"Processing at depth: {depth}")
        
        _, edge_state = ku.check_edges_orientation(decoded_state.cube)
        _, corner_state = ku.check_corner_orientation(decoded_state.cube)
        slice_state = ku.get_ud_slice_point(decoded_state.cube)
        
        if not state_already_visited(edge_state, corner_state, slice_state, db_path):
            insert_into_db(lock, edge_state, corner_state, slice_state, depth, db_path)
        
        if depth < MAX_DEPTH:
            for move in moves:
                if last_move == move and consecutive_moves_count >= 3:
                    continue

                if last_move is not None and move == OPPOSITE_MOVES.get(last_move, -1):
                    continue
                new_cube = decode_to_cube(state)
                new_cube.do_move(move)
                new_state_encoded = encode_cube(new_cube)
                new_consecutive_moves_count = consecutive_moves_count + 1 if last_move == move else 1
                queue.put((new_state_encoded, depth + 1,move,new_consecutive_moves_count))  # Put new state in FileQueue

    # Close the queue when done
    queue.dispose()

def generate_pruning_table(start_state, max_depth):
    with Manager() as manager:
        lock = manager.Lock()
        chunks = [
            (start_state, (i * (max_depth // NUM_CORES), (i + 1) * (max_depth // NUM_CORES)), lock, DB_PATH, MOVES, f'{QUEUE_PATH}_{i}')
            for i in range(NUM_CORES)
        ]
        with Pool(NUM_CORES) as pool:
            pool.starmap(process_state_chunk, chunks)

if __name__ == '__main__':
    # Connect to (or create) SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pruning_table (
            edge_state INTEGER,
            corner_state INTEGER,
            slice_state INTEGER,
            depth INTEGER,
            PRIMARY KEY (edge_state, corner_state, slice_state)
        )
    ''')

    start_state = rb.RubiksCube()
    generate_pruning_table(start_state, MAX_DEPTH)

    conn.close()
