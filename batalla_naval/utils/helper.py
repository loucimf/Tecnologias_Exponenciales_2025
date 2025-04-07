
from .classes import Ship, Coordinate, ALPHABET

def get_numbers_between(num1: int, num2: int):
    lower = min(num1, num2)
    upper = max(num1, num2)
    
    numbers_in_between = list(range(lower + 1, upper))
    
    return numbers_in_between

def set_all_coordinates(boat: Ship):
    allCoordinates: list = []
    startCoord: Coordinate = boat.start_coord
    endCoord: Coordinate = boat.end_coord

    allCoordinates.append(startCoord)
    if (startCoord.letter == endCoord.letter): 
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
        if (currentCoord.letter == coordIndex.letter and currentCoord.number == coordIndex.number):
            return True
        return False
    
def isOverlappingBoats(coord: Coordinate, player_boats: list[Ship]) -> bool:
    for otherBoat in player_boats:
        print("size", otherBoat.size)
        for other_boat_coord in otherBoat.coords:
            print("other boat coord", other_boat_coord.letter, other_boat_coord.number)
            print("current coord", coord.letter, coord.number)
            if ((coord.letter == other_boat_coord.letter) and (coord.number == other_boat_coord.number)):
                print("Overlapping detected")
                return True
    return False


# main funcs

def is_valid_coordinate(currentCoord: Coordinate, boat: Ship, allBoats: list[Ship]) -> bool:    
    allCoords: list[Coordinate] = boat.coords

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

def write_end_characters(board, x, y, boat: Ship) -> list:
    raw_end_coords: list = boat.end_coord.getMatrixPosition()
    raw_start_coords: list = boat.start_coord.getMatrixPosition()

    if (isVertical(boat)):
        # just circle when vertical (no hay characters estilo upper semicircle)
        board.place_symbol(x, y, '●')
    else: 
        #chekc if the current x is one of the ends
        if (x < raw_end_coords[0]):
            board.place_symbol(x, y, '◖')
        else:
            board.place_symbol(x, y, '◗')