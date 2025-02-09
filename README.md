# RubiksCubeSolver

## Opis projektu

**RubiksCubeSolver** to aplikacja mobilna na urządzenia z systemem Android, której głównym celem jest ułożenie kostki Rubika na podstawie wprowadzonych przez użytkownika danych o aktualnym stanie kostki. Projekt wykorzystuje trzy typy algorytmów:

1. **Algorytmy klasyczne** – takie, których może nauczyć się i używać człowiek (np. LBL).
2. **Algorytmy komputerowe** – wykorzystujące zaawansowane metody przeszukiwania (np. IDA*, Kociemba), aby znaleźć optymalne rozwiązanie.
3. **Algorytmy oparte na uczeniu maszynowym** – w tym podejściu użyto sieci neuronowej wytrenowanej na bazie wielu wygenerowanych stanów kostki. Jej zadaniem jest przewidzieć liczbę ruchów niezbędnych do ułożenia kostki z bieżącego stanu, co przyspiesza wyszukiwanie najkrótszej sekwencji ruchów.

Aplikacja komunikuje się z **API**, działającym na serwerze (folder `server`), gdzie zaimplementowano całą logikę rozwiązywania. Dzięki temu nawet słabsze urządzenia mobilne mogą szybko otrzymać poprawną sekwencję ruchów.

> Projekt został zrealizowany w ramach **pracy inżynierskiej**, a w opracowaniu skupiono się m.in. na porównaniu liczby ruchów, czasu wykonania i efektywności różnych algorytmów.

---

## Struktura repozytorium

W repozytorium znajdują się dwa główne foldery:

- **`mobile_app_new`** – zawiera kod aplikacji mobilnej na platformę Android.
- **`server`** – zawiera kod źródłowy oraz konfigurację serwera API, który przetwarza zapytania i generuje rozwiązania.

---

## Uruchomienie serwera (API)

1. **Sklonuj repozytorium**:
   ```bash
   git clone https://github.com/KukielkaKamil/RubiksCubeSolver.git
   cd RubiksCubeSolver/server
   ```
2. **Zainstaluj wymagane zależności**
   Po pobraniu projektu należy przejść do folderu projektu i stworzyć wirtualne środowisko, które należy uruchomić, można tego dokonać, za pomocą poleceń(dla systemu Windows):
   ```bash
   python -m venv "nazwa_środowiska"
   "nazwa_środowiska/Scripts/activate.bat"
   ```
   Następnie należy pobrać wszystkie niezbędne biblioteki za pomocą:
     ```bash
     pip install -r requirements.txt
     ```
3. **Uruchom serwer**:
   Należy przejść do folderu servera a następnie uruchomić skrypt odpowiadający za jego uruchomienie

     ```bash
     cd server
     python server.py
     ```
4. **Sprawdź działanie API**  
   Serwer zazwyczaj uruchamia się lokalnie pod adresem `http://localhost:5000` oraz pod adresem komputera na którym serwer jest utuchaminay. Dla celów testów adres ten prezentuje się następująco `http://192.168.43.169:5000`. IP to zostało ustalone na stałe w aplikacji, tak aby móc połączyć aplikację z telefonem za pomocą techbologii Hotspot Możesz użyć przeglądarki lub narzędzia typu Postman, by przetestować dostępność endpointów (np. `GET /ping`).

> **Uwaga**: Jeśli chcesz użyć innego IP upewnij się, że adres serwera w aplikacji mobilnej (np. `http://10.0.2.2:5000` dla emulatora Androida) został poprawnie skonfigurowany, aby komunikacja z API działała prawidłowo.

---

## Uruchomienie aplikacji mobilnej (Android)

1. W tym celu należy na telefonie z systemem Android (aplikacja była testowana dla systmu Andorid 10) umieścić plik APK a następnie go zainstalować.
W przypadku użycia skanowania z użyciem kamery aplikajca powinna zapytać o zezwolenie na użycie kamery.

2. Jeśli użytkownik chciałby zmienić domyślny adres serwera należy to zrobić w plik `mobile_app_new/src/scenes/results.py`
a następnie zbudować całą apliację korzystając z polecenia

```bash
flet build apk mobile_app_new --include-packages flet_permission_handler
```

---


**Dziękuję za zainteresowanie i życzę powodzenia w korzystaniu z projektu!**