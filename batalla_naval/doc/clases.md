

Una [clase] sirve como una especie de `blueprint` o `plano`.

Una clase puede tener multiples cosas, como: 

- propiedades
- metodos
- constructores
- y mas.. (no me acuerdo todo)

Las clases se pueden instanciar, es decir, crearlas y acceder a sus metodos y variables o propiedades acordemente, y son independientes.



## Documentacion de las clases:


<Coordinate
    guarda una coord abstracta 
    y tiene un metodo para ubicar la coord abstracta en la matriz
>
[class] Coordinate:
    def __init__(self, letter: str, number: int):
        self.letter = letter
        self.number = number
    
    def getMatrixPosition(self): # 😎 (super jaker)
        return [ALPHABET.index(self.letter), self.number] #

<Ship
    Guarda info sobre el boat
    se explican solas las props. Cuenta con 1 metodo:
    - isSunk
>
[class] Ship:
    def __init__(self, size: int, start_coord: Coordinate, end_coord: Coordinate, coords: list[Coordinate]):
        self.size = size
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.coords = coords
        self.hits = 0

    def __isSunk__(self): 
        return self.hits == self.size


<Board
    Le quite el metodo display() porque lo documente en expresiones.md.
    almacena informacion sobre el board, debido a que con "self" puede manipularse a si mismo con data de la clase
    metodos:
    - place_symbol
    - place_boat
    - display
    place_symbol escribe el arg en la matriz 
    place_boat escribe un barco ayudandose con "place_symbol" con argumentos de "coords", y "valida" las coords antes de poner el barco
>
[class] Board: 
    def __init__(self, size: int):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        
    def place_symbol(self, x: int, y: int, symbol): 
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = symbol

    def place_boat(self, boat: Ship, compare_list: list[Ship]):
        boat_coords = boat.coords

        # !!!IMPORTANT!!!!!! import only when needed  
        from .helper import write_end_characters, is_valid_coordinate
        # medio feo, pero es para evitar el import circular :

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
        
<Player
    guarda propiedades;atributos, se explican solos.
>
[class] Player: 
    def __init__(self, default_board: Board, attack_board: Board, name: str, ships: list[Ship], shots: int): 
        self.name = name
        self.attempts = []
        self.shots = shots
        self.ships = ships
        self.board = default_board
        self.attack_board = attack_board