import httpx
import csv
from time import time as tm
import asyncio
import pandas as pd
from tqdm import tqdm

URL_PREFIX = 'http://127.0.0.1:5000'


def read_from_csv(filename):
    with open(filename, mode='r', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]


async def send_request(url, cubestring):
    params = {'cubestring': cubestring}

    try:
        start_tm = tm()
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, params=params)
        end_tm = tm()
        if response.status_code == 200:
            # Ensure JSON response has the expected structure
            response_data = response.json()
            result_text = response_data.get('result', None)

            if result_text:
                response_time = end_tm - start_tm
                solution_len = len(result_text)
                return solution_len, response_time
            else:
                raise ValueError("Invalid response from server: Missing 'result' field")
        else:
            error_message = response.json().get('error', 'An error occurred')
            raise Exception(error_message)

    except httpx.ConnectError:
        print("Connection Error", "Unable to connect to the server. Please check if the server is running.")
    except Exception as e:
        print("Error", str(e))
    return None, None


async def run_test_async(endpoint):
    cubestrings = read_from_csv("db.csv")
    url = f"{URL_PREFIX}/{endpoint}"
    results = []

    for test_num, cubestring in enumerate(tqdm(cubestrings, desc="Tests run"), start=1):
        solution_len, response_time = await send_request(url, cubestring)
        results.append((test_num, solution_len, response_time))

    # Write results to a CSV file
    output_filename = f"results_{endpoint}.csv"
    with open(output_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Test number", "Number of moves", "Time"])
        writer.writerows(results)

    # Convert results to Pandas Series for statistics
    move_results = pd.Series([result[1] for result in results if result[1] is not None])
    time_results = pd.Series([result[2] for result in results if result[2] is not None])

    print("Statystyki dla ruchów")
    print(move_results.describe())
    print("Statystyki dla czasu")
    print(time_results.describe())


def run_test(endpoint):
    asyncio.run(run_test_async(endpoint))


if __name__ == "__main__":
    # print("STATYSTYKI DLA ALGORYTMU kociemba")
    # run_test("kociemba")
    # print("STATYSTYKI DLA ALGORYTMU LBL")
    # run_test("lbl")
    print("STATYSTYKI DLA ALGORYTMU ML")
    run_test("ml")
