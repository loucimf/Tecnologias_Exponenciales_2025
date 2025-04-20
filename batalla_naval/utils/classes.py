import random
import string
from colorama import init, Fore, Style

# Inicializa colorama para permitir colores en consola
init(autoreset=True)

class Ship:
    def __init__(self, name, size, coords=[]):
        self.name = name            # Nombre del barco
        self.size = size            # Tamaño en casillas
        self.coordinates = coords   # Lista de coordenadas ocupadas
        self.hits = 0               # Impactos recibidos

    def set_coordinates(self, coords):
        self.coordinates = coords   # Asigna manualmente las coordenadas

    def is_sunk(self):
        return self.hits >= self.size  # True si está hundido

    def register_hit(self, x, y):
        # Si la coordenada está en el barco, cuenta como impacto
        if (x, y) in self.coordinates:
            self.hits += 1
            return True
        return False

# Representa el tablero de juego
class Board:
    def __init__(self, size):
        # Constructor: crea un tablero de tamaño `size` x `size`
        # Cada celda comienza con '~', que representa agua
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]

    def colorize(self, symbol):
        # Aplica colores a los símbolos del tablero para que se vean mejor en consola:
        # '~' = agua (color cian), 'B' = barco (blanco), 'X' = impacto (rojo), 'O' = agua fallada (amarillo)
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
        # Muestra el tablero en pantalla
        # Si `hide_ships` es True, oculta los barcos mostrando '~' en su lugar
        print("   " + " ".join(str(i) for i in range(self.size))) # Cabecera con números de columna
        for idx, row in enumerate(self.grid):
            letter = string.ascii_uppercase[idx] # Letras de fila (A, B, C...)
            display_row = []
            for cell in row:
                # Si hay que ocultar los barcos ('B'), se reemplazan por agua '~'
                if hide_ships and cell == 'B':
                    display_row.append(self.colorize('~'))
                else:
                    display_row.append(self.colorize(cell))
            print(f"{letter}  " + " ".join(display_row)) # Muestra fila con letra y contenido

    def can_place_ship(self, coords):
        # Verifica si un barco puede colocarse en las coordenadas dadas:
        # - No puede salirse del tablero
        # - No puede solaparse con otro barco
        for x, y in coords:
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False # Coordenada fuera de los límites
            if self.grid[y][x] != '~':
                return False # Ya hay algo en esa posición (otro barco)
        return True # Todo correcto, se puede colocar

    def place_ship(self, ship: Ship):
        # Coloca un barco en el tablero usando sus coordenadas
        # Marca cada celda con una 'B'
        for x, y in ship.coordinates:
            self.grid[y][x] = 'B'

    def place_symbol(self, x, y, symbol):
        # Marca un disparo en el tablero:
        # - Si era agua ('~') o barco ('B'), se puede reemplazar con 'X' o 'O'
        if self.grid[y][x] in ['~', 'B']:
            self.grid[y][x] = symbol

    def has_ship(self, x, y):
        # Devuelve True si en la coordenada hay un barco
        return self.grid[y][x] == 'B'

    def remaining_ships(self):
        # Cuenta cuántas celdas con barcos ('B') quedan en el tablero
        return sum(row.count('B') for row in self.grid)


class Player:
    def __init__(self, name, board_size, ship_list):
        # Constructor de la clase Player (jugador)
        
        self.name = name  # Nombre del jugador
        self.board = Board(board_size)  # Crea el tablero propio del jugador
        self.ships = []  # Lista donde se almacenarán los barcos colocados
        self.aciertos = 0  # Contador de disparos que acertaron
        self.fallos = 0  # Contador de disparos que fallaron
        self.attempts = []  # Historial de intentos de disparo (para evitar repetir)

        # Mensaje de inicio de colocación de barcos
        print(f"\n{name}, coloca tus barcos:")
        # Llama al método para colocar los barcos manualmente
        self.place_ships_manual(ship_list)

    def place_ships_manual(self, ship_list):
        # Método para colocar los barcos en el tablero de forma manual (uno por uno)
        for name, size in ship_list:
            while True:
                try:
                    # Muestra el nombre y tamaño del barco a colocar
                    print(f"\nColocando: {name} ({size} casillas)")

                    # Pide al jugador la fila inicial usando letras (A-J, etc.)
                    letra = input(f"Fila inicial (A-{chr(64+self.board.size)}): ").upper()
                    y = string.ascii_uppercase.index(letra)  # Convierte la letra a índice numérico

                    # Pide la columna inicial (número)
                    x = int(input(f"Columna inicial (0-{self.board.size-1}): "))

                    # Pide dirección: Horizontal (H) o Vertical (V)
                    direction = input("Dirección (H/V): ").upper()

                    # Verifica que la dirección ingresada sea válida
                    if direction not in ['H', 'V']:
                        print("Dirección inválida. Usa H o V.")
                        continue  # Vuelve a pedir datos

                    # Calcula las coordenadas que ocupará el barco según dirección y tamaño
                    coords = [(x + i, y) if direction == 'H' else (x, y + i) for i in range(size)]

                    # Verifica que las coordenadas sean válidas y no haya superposición
                    if not self.board.can_place_ship(coords):
                        print("¡Posición inválida o se sobrepone! Intenta de nuevo.")
                        continue  # Pide otra ubicación

                    # Crea el barco con sus coordenadas y lo agrega al jugador
                    ship = Ship(name, size, coords)
                    self.ships.append(ship)

                    # Coloca el barco en el tablero
                    self.board.place_ship(ship)

                    # Muestra el tablero actualizado
                    self.board.display()
                    break  # Sale del bucle y pasa al siguiente barco

                except Exception as e:
                    # Captura errores como coordenadas fuera de rango, letras inválidas, etc.
                    print(f"Error: {e}. Intenta de nuevo.")


class Game:
    def __init__(self, size=10, ship_def=None, max_attempts=20):
        # Inicializa el juego con tamaño del tablero, lista de barcos y disparos máximos por jugador
        self.size = size
        self.max_attempts = max_attempts
        self.players = []  # Lista de jugadores
        self.ship_def = ship_def or [  # Definición de barcos por defecto
            ("Lancha", 1),
            ("Destructor", 2),
            ("Submarino", 3)
        ]

    def add_player(self, name):
        # Crea un nuevo jugador con su tablero y barcos definidos, y lo agrega a la lista
        player = Player(name, self.size, self.ship_def)
        self.players.append(player)

    def fire(self, attacker: Player, defender: Player, x, y):
        # Lógica de disparo de un jugador a otro
        if (x, y) in attacker.attempts:
            print("Ya disparaste ahí.")  # Evita disparos repetidos
            return False

        attacker.attempts.append((x, y))  # Registra intento

        for ship in defender.ships:
            # Verifica si el disparo le da a algún barco
            if ship.register_hit(x, y):
                attacker.aciertos += 1
                defender.board.place_symbol(x, y, 'X')  # Marca impacto con X
                print(Fore.GREEN + f"{attacker.name} acertó en ({x},{y})")
                return True

        # Si no le da a ningún barco, se cuenta como fallo
        attacker.fallos += 1
        defender.board.place_symbol(x, y, 'O')  # Marca fallo con O
        print(Fore.MAGENTA + f"{attacker.name} falló en ({x},{y})")
        return False

    def start(self):
        # Comienza la partida y gestiona los turnos
        turno = 0
        total_turnos = self.max_attempts * 2  # Cada jugador tiene max_attempts disparos

        while turno < total_turnos:
            attacker = self.players[turno % 2]  # Alterna entre jugadores
            defender = self.players[(turno + 1) % 2]

            print(f"\nTurno {turno + 1} - {attacker.name} dispara:")
            defender.board.display(hide_ships=True)  # Muestra el tablero ocultando barcos

            try:
                # Toma coordenadas del disparo
                letra = input("Fila (A-J): ").upper()
                y = string.ascii_uppercase.index(letra)
                x = int(input("Columna (0-9): "))

                self.fire(attacker, defender, x, y)  # Ejecuta disparo

                # Verifica si todos los barcos del oponente están hundidos
                if all(ship.is_sunk() for ship in defender.ships):
                    print(f"\n ¡{attacker.name} ha ganado, hundió todos los barcos de {defender.name}.")
                    break

                turno += 1  # Pasa al siguiente turno
            except Exception as e:
                print(f"Error: {e}")  # Manejo de errores de entrada

        # Fin del juego: muestra resultados
        print("\n=== Fin del Juego ===")
        for player in self.players:
            print(f"\n{player.name} - Aciertos: {player.aciertos}, Fallos: {player.fallos}")
            print("Tablero Final:")
            player.board.display()  # Muestra el tablero completo del jugador


if __name__ == "__main__":
    # Punto de entrada principal del programa.
    # Este bloque se ejecuta solo si el archivo se corre directamente (no si se importa desde otro).

    juego = Game(
        size=10,  # Tamaño del tablero (10x10)
        ship_def=[  # Lista de barcos que se usarán en la partida
            ("Lancha", 1),     # Barco de 1 casilla
            ("Destructor", 2), # Barco de 2 casillas
            ("Submarino", 3)   # Barco de 3 casillas
        ],
        max_attempts=15  # Cada jugador tiene 15 disparos en total
    )

    # Agrega dos jugadores al juego. Cada uno coloca sus barcos manualmente.
    juego.add_player("Jugador 1")
    juego.add_player("Jugador 2")

    # Inicia la partida: los jugadores se turnan para disparar hasta que se hundan todos los barcos
    # o se terminen los turnos máximos.
    juego.start()
    
# https://chatgpt.com/share/68057db4-93c8-8000-823a-bfffa3ee3991