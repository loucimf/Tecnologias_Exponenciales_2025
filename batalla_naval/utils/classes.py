class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []
        self.hits = 0

    def __isSunk__(self): 
        return self.hits == self.size
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def set_hit(self, x , y):
        if (x, y) in self.coordinates:
            self.hits += 1
            return True
        return False

class Board: 
    def __init__(self, size):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]

    def display(self): 
        print("  " + " ".join(str(i) for i in range(self.size)))
        for idx, row in enumerate(self.grid):
            print(f"{idx} " + " ".join(row))

    def place_symbol(self, x, y, symbol): 
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.grid[y][x] == '~':
                self.grid[y][x] = symbol
            else:
                raise Exception('Pocision ocupada')
    
    def place_ship(self, ship: Ship, coordinates: list):
        for (x, y) in coordinates:
            if self.grid[y][x] != '~':
                raise Exception(f"Posición ocupada en ({x}, {y})")
        for (x, y) in coordinates:
            self.grid[y][x] == 'S'
        ship.set_coordinates(coordinates)
    

class Player: 
    def __init__(self, default_board: Board, attack_board: Board, name: str, ships: list, shots: int): 
        self.name = name
        self.attempts = []
        self.shots = shots
        self.ships = ships
        self.board = default_board
        self.attack_board = attack_board

class Game:
    def __init__(self):
        self.players  = []

    def add_player(self, name):
        if len(self.players) >= 2:
            raise Exception('Solo se permite dos jugadores')

        board = Board(10)
        attack_board = Board(10)
        ships = []
        player =  Player(board, attack_board, name, ships, 0)
        self.players.append(player)
        return player

    def fire(self, attacker: Player, defender: Player, x: int, y: int):
        if (x, y) in attacker.attempts:
            print("Ya disparaste ahí.")
            return False
        
        attacker.attempts.append((x, y))

        for ship in defender.ships:
            if (x, y) in ship.coordinates:
                ship.set_hit(x, y)
                attacker.attack_board.place_symbol(x, y, 'X')
                defender.board.place_symbol(x, y, 'X')
                print(f"¡{attacker.name} acertó en ({x},{y})!")
                return True
        
        attacker.attack_board.place_symbol(x, y, 'O')
        defender.board.place_symbol(x, y, 'O')
        print(f"{attacker.name} falló en ({x},{y}).")
        return False
        
    def start_game(self):
        if len(self.players) != 2:
            raise Exception('Se requieren dos jugadores')
        
        attacker, defender = self.players
        turno = 1
        
        while True:
            print(f"\nTurno {turno}: {attacker.name} dispara.")
            
            try:
                x = int(input("Ingrese la coordenada x: "))
                y = int(input("Ingrese la coordenada y: "))
                
                hit = self.fire(attacker, defender, x, y)

                if all(ship.__isSunk__() for ship in defender.ships):
                    print(f"\n🎉 {attacker.name} ha ganado la partida. ¡Todos los barcos de {defender.name} han sido hundidos!")
                    break

                attacker, defender = defender, attacker
                turno += 1

            except ValueError:
                print("Por favor, ingresa coordenadas válidas.")
            except Exception as e:
                print(f"Error: {e}")
        
        attacker, defender = defender, attacker
        turno += 1