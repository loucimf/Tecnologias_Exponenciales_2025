
import os, time, sys
from .classes import Ship, Coordinate, Player, Board, DEFAULT_BOATS_COORDINATES
from config import ALPHABET, BOARD_SIZE, SHOTS


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


def pause_time(seconds=3):
	message = "◖■■■◗"
	total_dots = 30
	interval = seconds / total_dots
	print("                             CAMBIA TURNO")
	for i in range(total_dots + 1):
		left_dashes = '~ ' * i
		right_dashes = ' ~' * (total_dots - i)
		sys.stdout.write(f"\r{left_dashes} {message} {right_dashes}")
		sys.stdout.flush()
		time.sleep(interval)

def clear_screen():
	# so ts works on the windows pc too
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')  # this works meh (i need to mess w the scrolling of the terminal)

def chatgpt_clear_screen():
	print("\033c", end="") # what

def setup_player(name: str):
	player_default_board = Board(BOARD_SIZE)
	player_attack_board = Board(BOARD_SIZE)
	new_player = Player(player_default_board, player_attack_board, name, clone_boats(), SHOTS)   
	return new_player

def space_print(amount=2) -> None:
	print("\n" * amount)

def organized_text(text: str): 
	space_print(1)
	print(f"{text}")