import string
import random
from colorama import init, Fore, Style
init(autoreset=True)

class Ship:
    def __init__(self, size, name):
        self.name = name
        self.hits = 0
        self.size = size
        self.coordinates = []

    def is_sunk(self):
        return self.hits >= self.size

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_hit(self, x, y):
        if (x, y) in self.coordinates:
            self.hits += 1
            return True
        return False

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]

    def colorize(self, symbol):
        if symbol == '~':
            return Fore.CYAN + symbol + Style.RESET_ALL
        elif symbol == 'S':
            return Fore.WHITE + symbol + Style.RESET_ALL
        elif symbol == 'X':
            return Fore.RED + symbol + Style.RESET_ALL
        elif symbol == 'O':
            return Fore.YELLOW + symbol + Style.RESET_ALL
        return symbol

    def display(self, hide_ships=False):
        print("   " + " ".join(str(i) for i in range(self.size)))
        for idx, row in enumerate(self.grid):
            letter = string.ascii_uppercase[idx]
            display_row = []
            for cell in row:
                if hide_ships and cell == 'S':
                    display_row.append(self.colorize('~'))
                else:
                    display_row.append(self.colorize(cell))
            print(f"{letter}  " + " ".join(display_row))

    def place_ships(self, ship: Ship, coordinates: list):
        for (x, y) in coordinates:
            if self.grid[y][x] != '~':
                raise Exception(f"Posición ocupada en ({x}, {y})")
        for (x, y) in coordinates:
            self.grid[y][x] = 'S'
        ship.set_coordinates(coordinates)

    def place_symbol(self, x, y, symbol):
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.grid[y][x] in ['~', 'S']:
                self.grid[y][x] = symbol
            else:
                raise Exception('Posición ocupada')

class Player:
    def __init__(self, default_board: Board, attack_board: Board, name: str):
        self.name = name
        self.attempts = []
        self.ships = []
        self.board = default_board
        self.attack_board = attack_board

    def place_ship(self, ship: Ship, coords: list):
        self.board.place_ships(ship, coords)
        self.ships.append(ship)

    def place_ships_manual(self):
        ships_to_place = [
            ("Destructor", 2),
            ("Submarino", 3),
            ("Acorazado", 4)
        ]

        for name, size in ships_to_place:
            while True:
                try:
                    print(f"\n{name} ({size} espacios)")
                    letra = input("Fila inicial (A-J): ").upper()
                    y = string.ascii_uppercase.index(letra)
                    x = int(input("Columna inicial (0-9): "))
                    direction = input("Dirección (H/V): ").upper()

                    if direction not in ['H', 'V']:
                        print("Dirección inválida. Usa H o V.")
                        continue

                    if direction == 'H':
                        if x + size > self.board.size:
                            print("¡No cabe horizontalmente!")
                            continue
                        coords = [(x + i, y) for i in range(size)]
                    else:
                        if y + size > self.board.size:
                            print("¡No cabe verticalmente!")
                            continue
                        coords = [(x, y + i) for i in range(size)]

                    ship = Ship(size, name)
                    self.place_ship(ship, coords)
                    self.board.display()
                    break
                except Exception as e:
                    print(f"Error: {e}. Intenta de nuevo.")

    def place_ships_auto(self):
        ships_to_place = [
            ("Destructor", 2),
            ("Submarino", 3),
            ("Acorazado", 4)
        ]

        for name, size in ships_to_place:
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])
                x = random.randint(0, self.board.size - (size if direction == 'H' else 1))
                y = random.randint(0, self.board.size - (size if direction == 'V' else 1))
                coords = [(x + i, y) if direction == 'H' else (x, y + i) for i in range(size)]
                try:
                    ship = Ship(size, name)
                    self.place_ship(ship, coords)
                    placed = True
                except:
                    continue

class Game:
    def __init__(self):
        self.players = []

    def add_player(self, name, modo='manual'):
        if len(self.players) >= 2:
            raise Exception('Solo se permiten dos jugadores')

        board = Board(10)
        attack_board = Board(10)
        player = Player(board, attack_board, name)

        if modo == 'manual':
            print(f"\n{name}, coloca tus barcos:")
            player.place_ships_manual()
        elif modo == 'auto':
            player.place_ships_auto()
            print(f"\n{name} ha colocado sus barcos automáticamente.")

        self.players.append(player)
        return player

    def fire(self, attacker: Player, defender: Player, x: int, y: int):
        if (x, y) in attacker.attempts:
            print('Ya disparaste ahí.')
            return False

        attacker.attempts.append((x, y))

        for ship in defender.ships:
            if (x, y) in ship.coordinates:
                ship.set_hit(x, y)
                attacker.attack_board.place_symbol(x, y, 'X')
                defender.board.place_symbol(x, y, 'X')
                print(f"{attacker.name} acertó en ({x},{y})")
                return True

        attacker.attack_board.place_symbol(x, y, 'O')
        defender.board.place_symbol(x, y, 'O')
        print(f"{attacker.name} falló en ({x},{y})")
        return False

    def start_game(self):
        if len(self.players) != 2:
            raise Exception('Se necesitan dos jugadores')

        attacker, defender = self.players
        turno = 1

        while True:
            print(f"\nTurno {turno}: {attacker.name} dispara.")
            print("\n== Tablero de Ataques ==")
            attacker.attack_board.display(hide_ships=True)

            print("\n== Tu Tablero de Defensa ==")
            attacker.board.display()

            try:
                letra = input("Fila (A-J): ").upper()
                y = string.ascii_uppercase.index(letra)
                x = int(input("Columna (0-9): "))

                self.fire(attacker, defender, x, y)

                if all(ship.is_sunk() for ship in defender.ships):
                    print(f"\n{attacker.name} ha ganado. ¡Todos los barcos de {defender.name} han sido hundidos!")
                    break

                attacker, defender = defender, attacker
                turno += 1

            except ValueError:
                print("Coordenadas inválidas.")
            except Exception as e:
                print(f"Error: {e}")
