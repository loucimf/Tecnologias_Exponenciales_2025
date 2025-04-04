

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []
        self.hits = 0

    def __isSunk__(self): 
        return self.hits == self.size
    

class Player: 
    def __init__(self, board, name, ships, shots): 
        self.name = name
        self.attempts = []
        self.shots = shots
        self.ships = ships
        self.board = board


class Board: 
    def __init__(self, size):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
    
    def display(self): 
        #ts crea una sequencia de 0 a (size - 1) y "transforma" todo a string (las columnas), todo neatly spaced
        print("  " + " ".join(str(i) for i in range(self.size)))
        #ts enumera el iterable GRID, y con su indice crea una lista de las filas
        for idx, row in enumerate(self.grid):
            print(f"{idx} " + " ".join(row))

