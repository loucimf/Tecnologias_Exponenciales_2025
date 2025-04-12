import random
import string
from colorama import init, Fore, Style
init(autoreset=True)

class Ship:
    def __init__(self, name, size, coords=[]):
        self.name = name
        self.size = size
        self.coordinates = coords
        self.hits = 0

    def set_coordinates(self, coords):
        self.coordinates = coords

    def is_sunk(self):
        return self.hits >= self.size

    def register_hit(self, x, y):
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
        elif symbol == 'B':
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
                if hide_ships and cell == 'B':
                    display_row.append(self.colorize('~'))
                else:
                    display_row.append(self.colorize(cell))
            print(f"{letter}  " + " ".join(display_row))

    def can_place_ship(self, coords):
        for x, y in coords:
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            if self.grid[y][x] != '~':
                return False
        return True

    def place_ship(self, ship: Ship):
        for x, y in ship.coordinates:
            self.grid[y][x] = 'B'

    def place_symbol(self, x, y, symbol):
        if self.grid[y][x] in ['~', 'B']:
            self.grid[y][x] = symbol

    def has_ship(self, x, y):
        return self.grid[y][x] == 'B'

    def remaining_ships(self):
        return sum(row.count('B') for row in self.grid)


class Player:
    def __init__(self, name, board_size, ship_list):
        self.name = name
        self.board = Board(board_size)
        self.ships = []
        self.aciertos = 0
        self.fallos = 0
        self.attempts = []

        print(f"\n{name}, coloca tus barcos:")
        self.place_ships_manual(ship_list)

    def place_ships_manual(self, ship_list):
        for name, size in ship_list:
            while True:
                try:
                    print(f"\nColocando: {name} ({size} casillas)")
                    letra = input(f"Fila inicial (A-{chr(64+self.board.size)}): ").upper()
                    y = string.ascii_uppercase.index(letra)
                    x = int(input(f"Columna inicial (0-{self.board.size-1}): "))
                    direction = input("Dirección (H/V): ").upper()

                    if direction not in ['H', 'V']:
                        print("Dirección inválida. Usa H o V.")
                        continue

                    coords = [(x + i, y) if direction == 'H' else (x, y + i) for i in range(size)]

                    if not self.board.can_place_ship(coords):
                        print("¡Posición inválida o se sobrepone! Intenta de nuevo.")
                        continue

                    ship = Ship(name, size, coords)
                    self.ships.append(ship)
                    self.board.place_ship(ship)
                    self.board.display()
                    break
                except Exception as e:
                    print(f"Error: {e}. Intenta de nuevo.")


class Game:
    def __init__(self, size=10, ship_def=None, max_attempts=20):
        self.size = size
        self.max_attempts = max_attempts
        self.players = []
        self.ship_def = ship_def or [
            ("Lancha", 1),
            ("Destructor", 2),
            ("Submarino", 3)
        ]

    def add_player(self, name):
        player = Player(name, self.size, self.ship_def)
        self.players.append(player)

    def fire(self, attacker: Player, defender: Player, x, y):
        if (x, y) in attacker.attempts:
            print("Ya disparaste ahí.")
            return False

        attacker.attempts.append((x, y))

        for ship in defender.ships:
            if ship.register_hit(x, y):
                attacker.aciertos += 1
                defender.board.place_symbol(x, y, 'X')
                print(Fore.GREEN + f"{attacker.name} acertó en ({x},{y})")
                return True

        attacker.fallos += 1
        defender.board.place_symbol(x, y, 'O')
        print(Fore.MAGENTA + f"{attacker.name} falló en ({x},{y})")
        return False

    def start(self):
        turno = 0
        total_turnos = self.max_attempts * 2

        while turno < total_turnos:
            attacker = self.players[turno % 2]
            defender = self.players[(turno + 1) % 2]

            print(f"\nTurno {turno + 1} - {attacker.name} dispara:")
            defender.board.display(hide_ships=True)

            try:
                letra = input("Fila (A-J): ").upper()
                y = string.ascii_uppercase.index(letra)
                x = int(input("Columna (0-9): "))

                self.fire(attacker, defender, x, y)

                if all(ship.is_sunk() for ship in defender.ships):
                    print(f"\n🏆 ¡{attacker.name} ha ganado! Hundió todos los barcos de {defender.name}.")
                    break

                turno += 1
            except Exception as e:
                print(f"Error: {e}")

        print("\n=== Fin del Juego ===")
        for player in self.players:
            print(f"\n{player.name} - Aciertos: {player.aciertos}, Fallos: {player.fallos}")
            print("Tablero Final:")
            player.board.display()


# --- EJECUCIÓN DEL JUEGO ---
if __name__ == "__main__":
    juego = Game(
        size=10,
        ship_def=[
            ("Lancha", 1),
            ("Destructor", 2),
            ("Submarino", 3)
        ],
        max_attempts=15
    )
    juego.add_player("Jugador 1")
    juego.add_player("Jugador 2")
    juego.start()
