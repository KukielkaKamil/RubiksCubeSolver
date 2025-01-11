import numpy as np
import joblib
import tensorflow as tf

# Zakładam, że masz osobny plik / moduł z klasą RubiksCube
# i funkcjami make_prediction(...) / preprocess_state(...) / create_model(...) itp.
# Na potrzeby przykładu poniżej importujemy bezpośrednio:
from RubiksCube import RubiksCube  # import Twojej klasy kostki      # w razie potrzeby
  # import funkcji predykcji
# Upewnij się, że:
#  - "training_script.py" zawiera zaimportowany, wczytany model (globalny lub w funkcji),
#    lub zdefiniowany `make_prediction(state)` tak, jak w kodzie, który podesłałeś.
#  - Model rubiks_cube_model.h5 i scaler.pkl są w ścieżkach, gdzie python je znajdzie.

# -------------------------------------------------------
# IDA* – parametry i narzędzia pomocnicze
# -------------------------------------------------------



MAX_DEPTH = 17  # maksymalna głębokość (w praktyce i tak przerwiemy wcześniej, 
                # gdy h+g przewyższy bound)

# Ruchy (lista liczb 0..11) – patrz rubiks_cube_class: do_move():
MOVES = [0,1,2,3,4,5,6,7,8,9,10,11]
OPPOSITE_MOVE = {
    0:1,   # R  -> R'
    1:0,   # R' -> R
    2:3,   # L  -> L'
    3:2,   # L' -> L
    4:5,   # F  -> F'
    5:4,   # F' -> F
    6:7,   # B  -> B'
    7:6,   # B' -> B
    8:9,   # D  -> D'
    9:8,   # D' -> D
    10:11, # U  -> U'
    11:10, # U' -> U
}


model = tf.keras.models.load_model("rubiks_cube_model.h5")
try:
    scaler = joblib.load("scaler.pkl")
except:
    scaler = None

def make_prediction(state_encoded):
    """
    Przekształca stan (54 intów) -> ewentualne skalowanie -> model -> wynik * 12
    Zakładamy, że w treningu depth było normowane do [0..1].
    """
    arr = np.array(state_encoded).reshape(1, -1).astype(np.float32)
    if scaler is not None:
        arr = scaler.transform(arr)
    pred = model.predict(arr, verbose=0)
    return pred[0][0] * 12

def heuristic(cube: RubiksCube) -> float:
    """
    Zwraca liczbę ruchów (w przybliżeniu) do rozwiązania,
    korzystając z modelu neuronowego (nasza heurystyka).
    """
    # Zakładamy, że encode_state() zwraca listę 54 intów (0..5)
    state_encoded = cube.encode_state()
    predicted = make_prediction(state_encoded)
    return predicted  # float: np. 7.2 -> interpretujemy to jako ~7 ruchów

def ida_search(cube: RubiksCube, bound, depth=0, path=None, prev_move=None):
    """
    Właściwa rekurencyjna część IDA*. 
    Zwraca tuple (status, cost):
      - status = True/False (czy rozwiązane)
      - cost = jeśli False – minimalna wartość f, do jakiej moglibyśmy zejść,
               jeśli True – docelowa ścieżka (lista ruchów).
    """
    if path is None:
        path = []

    # Sprawdź, czy kostka jest rozwiązana:
    if cube.is_solved():
        return (True, path)

    # Oblicz f = g + h:
    g = depth
    h = heuristic(cube)
    f = g + h

    if f > bound:
        # nie mieścimy się w aktualnym bound
        return (False, f)

    # Jeśli przekroczyliśmy pewien sensowny limit (żeby nie iść zbyt głęboko):
    if depth > MAX_DEPTH:
        return (False, float('inf'))

    min_cost = float('inf')

    # Wygeneruj wszystkie możliwe ruchy z tego stanu:
    for move in MOVES:
        # Unikaj bezpośredniego cofania poprzedniego ruchu (optymalizacja),
        # tzn. jeśli poprzedni move był 0 (R), to teraz nie bierzemy 1 (R').
        if prev_move is not None and move == OPPOSITE_MOVE[prev_move]:
            continue

        # Kopiujemy kostkę i wykonujemy ruch:
        new_cube = RubiksCube()
        new_cube.cube = cube.cube[:]  # shallow copy listy 54 elementów
        new_cube.do_move(move)

        # Rekurencja:
        status, cost = ida_search(new_cube, bound, depth + 1, path + [move], move)
        if status:
            # Jeśli znaleźliśmy rozwiązanie:
            return (True, cost)
        if cost < min_cost:
            min_cost = cost

    return (False, min_cost)

def ida_star_solve(cube: RubiksCube):
    """
    Główna funkcja rozwiązująca – pętla z kolejnymi bound.
    """
    # Początkowy bound:
    bound = heuristic(cube)
    print(f"Początkowy bound = {bound:.2f} (heurystyka)")

    # Iterujemy, aż do skutku:
    while True:
        print(f"\n[IDA*] Start z bound={bound:.2f}")
        status, result = ida_search(cube, bound)
        if status:
            # Mamy rozwiązanie:
            return result
        if result == float('inf'):
            # Oznacza, że nie znaleźliśmy nic poniżej MAX_DEPTH
            print(f"Niestety, przekroczyliśmy limit głębokości {MAX_DEPTH}.\n"
                  "Algorytm nie znalazł rozwiązania w tym zakresie.")
            return None
        bound += 0.5   # kolejna iteracja – podnieś próg

# -------------------------------------------------------
# Uruchomienie na przykładzie
# -------------------------------------------------------
if __name__ == "__main__":
    # 1. Tworzymy kostkę i tasujemy ją
    cube = RubiksCube()
    cube.scramble(10)  # np. 5 losowych ruchów

    cube2 = RubiksCube()
    cube2.cube = cube.cube

    print("Scrambled cube state:")
    cube.print_cube()

    # 2. Szukamy rozwiązania z użyciem IDA*
    solution_moves = ida_star_solve(cube)

    if solution_moves is not None:
        print("\nZnaleziono sekwencję ruchów (długość: {}):".format(len(solution_moves)))
        print(solution_moves)
        cube2.do_moves(solution_moves)
        cube2.print_cube()
        # Możemy wyświetlić, co każdy indeks oznacza (np. R=0, R'=1 itd.)
    else:
        print("\nNie znaleziono rozwiązania w dopuszczalnej głębokości.")
