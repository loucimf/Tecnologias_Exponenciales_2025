
# clases escalables

ALPHABET: list = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", 
    "U", "V", "W", "X", "Y", "Z"
]

class Coordinate:
    def __init__(self, letter: str, number: int):
        self.letter = letter
        self.number = number
    
    def getMatrixPosition(self): # 😎 (super jaker)
        return [ALPHABET.index(self.letter), self.number]



class Ship:
    def __init__(self, size: int, start_coord: Coordinate, end_coord: Coordinate, coords: list[Coordinate]):
        self.size = size
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.coords = coords
        self.hits = 0

    def __isSunk__(self): 
        return self.hits == self.size


# import HERE, cuz this is a circular import
from .helper import get_numbers_between, write_end_characters, is_valid_coordinate

class Board: 
    def __init__(self, size: int):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
    
    def display(self): 
        #ts crea una sequencia de 0 a (size - 1) y "transforma" todo a string (las columnas), todo neatly spaced
        print("   " + " ".join(ALPHABET[i] for i in range(self.size)))
        #ts enumera el iterable GRID, y con su indice crea una lista de las filas
        for idx, row in enumerate(self.grid):
            print(f"{idx:>2} " + " ".join(row))
        
    def place_symbol(self, x: int, y: int, symbol): 
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = symbol

    def place_boat(self, boat: Ship, compare_list: list[Ship]):
        boat_coords = boat.coords
        
        for coord in boat_coords:
            if (is_valid_coordinate(coord, boat, compare_list)):

                print("Placing boat at: ", coord.letter, coord.number)
                x, y = coord.getMatrixPosition()

                if (coord == boat.start_coord or coord == boat.end_coord):
                    write_end_characters(self, x, y, boat)
                    continue

                self.place_symbol(x, y, '■')
            else:
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
