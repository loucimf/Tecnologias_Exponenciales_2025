
from .classes import Ship, Coordinate, Player, Board, DEFAULT_BOATS_COORDINATES
from config import ALPHABET


def get_numbers_between(num1: int, num2: int):
    lower = min(num1, num2)
    upper = max(num1, num2)
    
    numbers_in_between = list(range(lower + 1, upper))
    
    return numbers_in_between

# helps with redundancy
def isSameAbstractCoord(coord1: Coordinate, coord2: Coordinate) -> bool:
    if (coord1.letter == coord2.letter and coord1.number == coord2.number):
        return True
    return False

def check_hit(player: Player, opponent: Player, coord: Coordinate):
    # check if the coordinate is in any of the boats
    x, y = coord.getMatrixPosition()

    for boat in opponent.ships:
        for boat_coord in boat.coords:

            if (isSameAbstractCoord(boat_coord, coord)):
                input("HIT---")
                # print("Adding 1 hit to", boat.hits, "hits to the boats of:", opponent.name)
                boat.hits += 1

                player.attack_board.place_symbol(x, y, 'X')
                opponent.board.place_symbol(x, y, '⨷')
                return True, boat
            
    player.attack_board.place_symbol(x, y, 'O')
    opponent.board.place_symbol(x, y, 'O')
            
    input("MISS...")
    return False, None

def set_all_coordinates(boat: Ship):
    allCoordinates: list = []
    startCoord: Coordinate = boat.start_coord
    endCoord: Coordinate = boat.end_coord

    allCoordinates.append(startCoord)
    
    if (not isVertical(boat)): 
        # get the missing numbers in the Y axis (number axis)
        missingCoords: list = get_numbers_between(startCoord.number, endCoord.number)
        for yCoords in missingCoords: 
            coordinate: Coordinate = Coordinate(startCoord.letter, yCoords)
            allCoordinates.append(coordinate)
        allCoordinates.append(endCoord)

    else: 
        # get raw coords for alphabet identification
        raw_start_coords: list = startCoord.getMatrixPosition()
        raw_end_coords: list = endCoord.getMatrixPosition()
    
        # get the missing numbers in the X axis (letter axis)
        missingCoords: list = get_numbers_between(raw_start_coords[0], raw_end_coords[0])
        for xCoords in missingCoords: 
            coordinate: Coordinate = Coordinate(ALPHABET[xCoords], startCoord.number)
            # append the coords (processed) to allCoordinates 
            allCoordinates.append(coordinate)

        allCoordinates.append(endCoord)
    # set the coordinates to the boat
    boat.coords = allCoordinates


# helper functions (for the validation)
def isVertical(boat: Ship) -> bool:
    isVertical: bool = boat.start_coord.letter == boat.end_coord.letter
    return isVertical

def isHorizontal(boat: Ship) -> bool:
    isHorizontal: bool = boat.start_coord.number == boat.end_coord.number
    return isHorizontal

def isADiagonal(boat: Ship):
    if (isVertical(boat) or isHorizontal(boat)):
        return False 
    return True
    
def isOnTop(allCoords: list[Coordinate], currentCoord: Coordinate):
    for coordIndex in allCoords:
        if (isSameAbstractCoord(coordIndex, currentCoord)):
            return True
        return False
    
def isOverlappingBoats(coord: Coordinate, player_boats: list[Ship]) -> bool:
    # iterate over each boat player has
    for otherBoat in player_boats:
        for other_boat_coord in otherBoat.coords:
            # and compare each coordinate of the current boat iteration with the current coord
            if (isSameAbstractCoord(coord, other_boat_coord)):
                print("Overlapping is: ", coord.letter, coord.number , " ;  ", other_boat_coord.letter, other_boat_coord.number)
                return True
    return False

def isInBounds(coord: Coordinate, board_size: int) -> bool:
    # this weird syntax, creates a sublist of the alphabet with the size of the board
    ALPHABET_SECTOR = ALPHABET[:board_size]

    # y ahora checkea el rango entre el alphabeto en base a boardsize y boardsize
    if ((coord.letter in ALPHABET_SECTOR) and (coord.number in range(board_size))):
        return True
    return False


# main funcs
def is_valid_coordinate(currentCoord: Coordinate, boat: Ship, allBoats: list[Ship], BOARD_SIZE: int) -> bool:    
    allCoords: list[Coordinate] = boat.coords

    if (allCoords[0] == currentCoord):
        print("Start coord detected")  
        return True  

    if (not isInBounds(currentCoord, BOARD_SIZE)):
        print("Out of bounds detected")
        return False

    if (isOverlappingBoats(currentCoord, allBoats)):
        print("Overlapping detected")
        return False
    
    if (allCoords[0] == currentCoord):
        print("Start coord detected")
        return True
    
    if isOnTop(allCoords, currentCoord):
        print("On Top detected")
        return False
    
    if isADiagonal(boat):
        print("Diagonal detected")
        return False
    
    return True

def debug_boat(boat: Ship):
    print("Ship size:", boat.size)
    print("Ship hits:", boat.hits)
    print("Ship coordinates:")
    for coords in boat.coords: 
        print("- ", coords.letter, coords.number)

def debug_player(player: Player):
    print("Player name:", player.name)
    print("Player shots:", player.shots)
    print("Player attempts:")
    for attempt in player.attempts:
        print("- ", attempt.letter, attempt.number)

def debug_board(board: Board):
    print("Board size:", board.size)
    print("board display:", board.display())

def debug(player: Player):
    debug_player(player)
    for boat in player.ships:
        debug_boat(boat)
    debug_board(player.board)


def write_end_characters(board, x, y, boat: Ship) -> list:
    raw_end_coords: list = boat.end_coord.getMatrixPosition()

    if (isVertical(boat)):
        # just circle when vertical (no hay characters estilo upper semicircle)
        board.place_symbol(x, y, '●')
    else: 
        #chekc if the current x is one of the ends
        if (x < raw_end_coords[0]):
            board.place_symbol(x, y, '◖')
        else:
            board.place_symbol(x, y, '◗')
        

def clone_boats():
    # clone the boats in default
    new_boats = []
    for boat in DEFAULT_BOATS_COORDINATES:
        new_boat = Ship(boat.size, boat.start_coord, boat.end_coord, boat.coords) # create new instance for each boat in the list
        new_boats.append(new_boat)

    return new_boats    

