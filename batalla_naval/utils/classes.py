
# classes that depend de helper.py
from config import ALPHABET, BOARD_SIZE, MINIMUM_BOATS

class Coordinate:
    def __init__(self, letter: str, number: int):
        self.letter = letter
        self.number = number
    
    def getMatrixPosition(self): # 😎 (super jaker)
        return [ALPHABET.index(self.letter), self.number] #

class Ship:
    def __init__(self, size: int, start_coord: Coordinate, end_coord: Coordinate, coords: list[Coordinate]):
        self.size = size
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.coords = coords
        self.hits = 0

    def __isSunk__(self): 
        return self.hits == self.size

class Board: 
    def __init__(self, size: int):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
    
    # overall weird syntax but simple
    def display(self): 
        #ts crea una sequencia de 0 a (size - 1) y crea expresiones string con cada elemento de alphabet y "transforma" todo a string (las columnas), todo neatly spaced
        print("   " + " ".join(ALPHABET[i] for i in range(self.size)))
        #ts enumera el iterable GRID, y con su indice crea una lista de las filas
        for idx, row in enumerate(self.grid):
            # so the rows dont start at 0, 1, 2, 3
            print(f"{idx + 1:>2} " + " ".join(row))
        
    def place_symbol(self, x: int, y: int, symbol): 
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = symbol

    def place_boat(self, boat: Ship, compare_list: list[Ship]):
        boat_coords = boat.coords

        # !!!IMPORTANT!!!!!! import only when needed  
        from .helper import write_end_characters, is_valid_coordinate
        # medio feo, pero es para evitar el import circular :)

        for coord in boat_coords:
            if (is_valid_coordinate(coord, boat, compare_list, BOARD_SIZE)):

                print("Placing boat at: ", coord.letter, coord.number)
                x, y = coord.getMatrixPosition()

                if (coord == boat.start_coord or coord == boat.end_coord):
                    write_end_characters(self, x, y, boat)
                    continue

                self.place_symbol(x, y, '■')
            else:
                compare_list.remove(boat)
                print("INVALID_COORDINATE")
                input("Porfavor, volver a intentar")
                break
        
class Player: 
    def __init__(self, default_board: Board, attack_board: Board, name: str, ships: list[Ship], shots: int): 
        self.name = name
        self.attempts = []
        self.shots = shots
        self.ships = ships
        self.board = default_board
        self.attack_board = attack_board



# for testing THIS WAS THE ERRORRR
DEFAULT_BOATS_COORDINATES: list[Ship] = []

# while this does generate default boat coordinates it actually does not. 
# this both generates coordinates for boats and creates the boats and appends it to the default_boat..., so the default list itself, is composed of many classes of boat, that are the same for both players
for i in range(MINIMUM_BOATS):
    from .helper import set_all_coordinates, debug_boat
    # Create a ship with size 1 and coordinates
    start_coord: Coordinate = Coordinate(ALPHABET[i], 0)
    end_coord: Coordinate = Coordinate(ALPHABET[i], 2)

    ship = Ship(1, start_coord, end_coord, [])

    set_all_coordinates(ship)
    ship.size = ship.coords.__len__()

    # debug_boat(ship)

    DEFAULT_BOATS_COORDINATES.append(ship)

# same as paint_symbols but w/o validation
def no_validation_paint_symbols(player: Player, allBoats: list[Ship]):

    from .helper import debug_boat, write_end_characters

    print(player.name)
    for _boats in allBoats:
        print("Boat: ", _boats.start_coord.letter, _boats.start_coord.number, " - ", _boats.end_coord.letter, _boats.end_coord.number)

    for boat in allBoats:
        for coord in boat.coords:
            
            x, y = coord.getMatrixPosition()

            # debug_boat(boat)

            if (coord == boat.start_coord or coord == boat.end_coord):
                write_end_characters(player.board, x, y, boat)
                continue
            
            player.board.place_symbol(x, y, '■')
