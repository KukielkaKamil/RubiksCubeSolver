import RubiksCube as rb
import sqlite3
from multiprocessing import Pool, Manager, Lock
from queue import Queue
from copy import deepcopy
import random

MAX_DEPTH = 12
NUM_THREADS = 4  # Adjust based on available cores
DB_PATH = 'cube_states.db'
MOVES = list(range(12))  # 12 moves available

# Create the database and table if it doesn't exist
def create_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cube_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                encoded_state TEXT UNIQUE,
                depth INTEGER
            )
        ''')
        conn.commit()

# Function to encode the cube
# def encode_cube(cube: rb.RubiksCube) -> list:
#     return cube.cube

# Decode a list back to a RubiksCube instance
def decode_to_cube(encoded_state: list) -> rb.RubiksCube:
    cube = rb.RubiksCube()
    result = cube.decode_state_num(encoded_state.copy())
    return result


# Insert the encoded state and depth into the database
def insert_encoded_cube(lock, encoded_state, depth, db_path):
    with lock:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO cube_states (encoded_state, depth) 
            VALUES (?, ?)
            """,
            (str(encoded_state), depth)
        )
        conn.commit()
        conn.close()

# Check if the encoded state is already in the database
def state_already_visited(encoded_state, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM cube_states WHERE encoded_state = ? LIMIT 1",
        (str(encoded_state),)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to encode the cube
def encode_cube(cube: rb.RubiksCube) -> list:
    return cube.encode_state()  # Assuming your RubiksCube class has this method

# Process a chunk of states using a shared queue
def process_states(queue, lock, db_path, max_depth):
    while not queue.empty():
        try:
            current_state, depth = queue.get_nowait()
        except Exception:  # In case of a race condition
            break

        if depth > max_depth:
            continue

        print(f'Current depth: {depth}')
        # Encode the current state
        encoded_state = encode_cube(current_state)

        # Random exclusion of states (e.g., 10% chance of skipping after depth 2)
        if depth > 4 and random.randint(0, 100) < 85:
            continue

        # Skip already visited states
        if state_already_visited(encoded_state, db_path):
            continue

        # Insert into the database
        insert_encoded_cube(lock, encoded_state, depth, db_path)

        # Generate new states for the next depth
        if depth < max_depth:
            for move in MOVES:
                new_cube = decode_to_cube(encoded_state)
                new_cube.do_move(move)
                queue.put((new_cube, depth + 1))


# Generate pruning table using multiple threads
def generate_pruning_table(start_state, max_depth):
    manager = Manager()
    queue = manager.Queue()
    lock = manager.Lock()

    # Initialize the queue with the start state
    queue.put((start_state, 0))

    # Create thread pool
    with Pool(NUM_THREADS) as pool:
        # Pass the queue and other arguments to the workers
        pool.starmap(
            process_states,
            [(queue, lock, DB_PATH, max_depth) for _ in range(NUM_THREADS)]
        )

if __name__ == '__main__':
    # Initialize the database
    create_db()

    # Start with the solved Rubik's Cube state
    start_state = rb.RubiksCube()

    # Generate the pruning table
    generate_pruning_table(start_state, MAX_DEPTH)
