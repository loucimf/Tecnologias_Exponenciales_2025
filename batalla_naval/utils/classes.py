
# classes that depend de helper.py
from config import ALPHABET, BOARD_SIZE, MINIMUM_BOATS

class Coordinate:
    def __init__(self, letter: str, number: int):
        self.letter = letter
        self.number = number
    
    def getMatrixPosition(self): # 😎😎😎 (super jaker)
        return [ALPHABET.index(self.letter), self.number] #

class Ship:
    def __init__(self, size: int, start_coord: Coordinate, end_coord: Coordinate, coords: list[Coordinate]):
        self.size = size
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.coords = coords
        self.hits = 0

    def is_sunk(self): 
        return self.hits == self.size

class Board: 
    def __init__(self, size: int):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
    
    def display(self): 
        #ts crea una sequencia de 0 a (size - 1) y crea expresiones string con cada elemento de alphabet y "transforma" todo a string (las columnas), todo neatly spaced
        print("   " + " ".join(ALPHABET[i] for i in range(self.size)))
        #ts enumera el iterable GRID, y con su indice crea una lista de las filas
        for idx, row in enumerate(self.grid):
            # so the rows dont start at 0, 1, 2, 3
            print(f"{idx + 1:>2} " + " ".join(row))

    # same logic as display(), but instead prints both rows in the same string w correct spacing
    def display_two_boards(self, other_board, label_right="ATTACK"):
        size = self.size
        column_labels = "   " + " ".join(ALPHABET[i] for i in range(size))
        print(f"{column_labels}     {column_labels}  <-- {label_right}")
        
        for i in range(size):
            row_num = f"{i + 1:2}"
            row_self = " ".join(self.grid[i])
            row_other = " ".join(other_board.grid[i])
            print(f"{row_num} {row_self}     {row_num} {row_other}")

        
    def place_symbol(self, x: int, y: int, symbol): 
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = symbol

    def place_boat(self, boat: Ship):

        # !!!IMPORTANT!!!!!! import only when needed  
        from .helper import write_end_characters

        for coord in boat.coords:
            x, y = coord.getMatrixPosition()

            if (coord == boat.start_coord or coord == boat.end_coord):
                write_end_characters(self, x, y, boat)
                continue

            self.place_symbol(x, y, '■')
        return True
    
class Player: 
    def __init__(self, default_board: Board, attack_board: Board, name: str, ships: list[Ship], shots: int): 
        self.name = name
        self.attempts = []
        self.shots = shots
        self.ships = ships
        self.board = default_board
        self.attack_board = attack_board


# ERR
DEFAULT_BOATS_COORDINATES: list[Ship] = []

# while this does generate default boat coordinates it actually does not 💀💀. 
# this both generates coordinates for boats and creates the boats and appends it to the default_boat..., so the default list itself, is composed of many classes of boat, that are the same for both players
for i in range(MINIMUM_BOATS):
    from .main_funcs import set_all_coordinates
    # Create a ship with size 1 and coordinates
    start_coord: Coordinate = Coordinate(ALPHABET[i], 0)
    end_coord: Coordinate = Coordinate(ALPHABET[i], 2)
    
    ship = Ship(1, start_coord, end_coord, [])


    set_all_coordinates(ship)
    ship.size = len(ship.coords)

    DEFAULT_BOATS_COORDINATES.append(ship)

# same as paint_symbols but w/o validation
def no_validation_paint_symbols(player: Player, allBoats: list[Ship]):
    for boat in allBoats:
        for coord in boat.coords:
            
            from .main_funcs import write_end_characters

            x, y = coord.getMatrixPosition()

            if (coord == boat.start_coord or coord == boat.end_coord):
                write_end_characters(player.board, x, y, boat)
                continue

            player.board.place_symbol(x, y, '■')
