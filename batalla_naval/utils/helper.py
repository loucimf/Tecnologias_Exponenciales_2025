
from .classes import Ship, Coordinate, ALPHABET

def isOnTop(elements: list, currentCoord: list):
    for i in elements:
        if (currentCoord == elements[i]):
            return True
        return False



def isADiagonal(elements: list, currentCoord: list):
    for i in elements:
        if ((currentCoord[0] != elements[i - 1][0]) or (currentCoord[1] != elements[i - 1][1])):
            return True
        return False
    

def is_valid_coordinate(elements: list, currentCoord: list):    
    if (isOnTop(elements, currentCoord) or isADiagonal(elements, currentCoord)): 
        return False
    return True


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

    if (startCoord[0] == endCoord[0]): 

        missingCoords: list = get_numbers_between(startCoord[1], endCoord[1])
        for yCoords in missingCoords: 
            coordinate: Coordinate = Coordinate(startCoord[0], missingCoords[yCoords])
            allCoordinates.append(coordinate)
        allCoordinates.append(endCoord)

    else: 
        # make em like 0; 2 (no letters)
        raw_start_coords: list = startCoord.getMatrixPosition()
        raw_end_coords: list = endCoord.getMatrixPosition()
    
        # get the missing coordinates
        missingCoords: list = get_numbers_between(raw_start_coords[0], raw_end_coords[0])

        for xCoords in missingCoords: 
            coordinate: Coordinate = Coordinate(ALPHABET[missingCoords[xCoords]], startCoord[1])
            allCoordinates.append(coordinate)

        allCoordinates.append(endCoord)
    
    boat.coords = allCoordinates



    