
ALPHABET: list = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z"
]

BOAT_AMOUNT: int = 5
BOARD_SIZE: int= 10
MINIMUM_SHOTS: int = 5
MINIMUM_BOATS: int = 4

MAX_BOATS: int = 10
MAX_SHOTS: int = 26 * 26 - 50 #max possible shots, - 50


def calculate_shots(BOARD_SIZE: int, MINIMUM_SHOTS: int, MAX_SHOTS: int, SCALE_FACTOR: float) -> int:
    additional_shots = int(BOARD_SIZE ** 2 * SCALE_FACTOR)
    # Total shots is the sum of base shots and additional calculated shots
    total_shots = MINIMUM_SHOTS + additional_shots
    
    # Ensure total shots do not exceed the maximum allowed
    return min(total_shots, MAX_SHOTS)

def calculate_boats(BOARD_SIZE: int, MINIMUM_BOATS: int, SCALE_FACTOR: float, MAX_BOATS: int):

    additional_boats = int(BOARD_SIZE ** 2 * SCALE_FACTOR)
    total_boats = MINIMUM_BOATS + additional_boats
    return min(total_boats, MAX_BOATS)


SHOTS: int = calculate_shots(BOARD_SIZE, MINIMUM_SHOTS, MAX_SHOTS, 0.15)
BOATS_AMOUNT: int = calculate_boats(BOARD_SIZE, MINIMUM_BOATS, 0.05, MAX_BOATS)