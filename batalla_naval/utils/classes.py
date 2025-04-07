
# clases escalables
from .helper import get_numbers_between

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
    def __init__(self, size: int, start_coord: Coordinate, end_coord: Coordinate, coords: list):
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
    
    def display(self): 
        #ts crea una sequencia de 0 a (size - 1) y "transforma" todo a string (las columnas), todo neatly spaced
        print("   " + " ".join(ALPHABET[i] for i in range(self.size)))
        #ts enumera el iterable GRID, y con su indice crea una lista de las filas
        for idx, row in enumerate(self.grid):
            print(f"{idx:>2} " + " ".join(row))
        
    def place_symbol(self, x: int, y: int, symbol): 
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = symbol

    def place_boat(self, boat: Ship):
        
        start_coord = boat.start_coord.getMatrixPosition()
        end_coord= boat.end_coord.getMatrixPosition()

        if (start_coord[0] == end_coord[0] and start_coord[1] == end_coord[1]):
            self.place_symbol(start_coord[0], start_coord[1], "▯")

        if (start_coord[0] == end_coord[0]):
            # y coords son las mismas asi q esta vertical
            yCoords = get_numbers_between(start_coord[1], end_coord[1])
            for y in yCoords:
                self.place_symbol(start_coord[0], y, "▯")

        elif (start_coord[1] == end_coord[1]):
            # x coords son las mismas asi que esta horziaotala
            xCoords = get_numbers_between(start_coord[0], end_coord[0])
            for x in xCoords:
                self.place_symbol(x, start_coord[1], "▯")





class Player: 
    def __init__(self, default_board: Board, attack_board: Board, name: str, ships: list[Ship], shots: int): 
        self.name = name
        self.attempts = []
        self.shots = shots
        self.ships = ships
        self.board = default_board
        self.attack_board = attack_board
