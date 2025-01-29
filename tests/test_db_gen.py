from RubiksCube import RubiksCube as rb
import random
import csv

def write_to_csv(filename,data):
    with open(filename,mode='a',newline='',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data])

    
def test_db_gen(db_name="db.csv", size = 100, min_moves = 2, max_moves = 20):
    for i in range(size):
        cb = rb()
        moves_num = random.randint(min_moves,max_moves)
        cb.scramble(moves_num)
        cube_list = cb.encode_to_cubestring()
        cube_string = ''.join(cube_list)
        print(cube_string)
        write_to_csv(db_name, cube_string)

if __name__ == "__main__":
    test_db_gen()
        