from utils.helper import *
from config import *

boat_list = BOAT_SIZES_LIST

def chooseBoatLocations(player: Player) -> None: 

	allBoats: list[Ship] = []
	player.board.display()
	print("----Todas las coordenadas deben estar en formato LETRA NUMERO  (LETRA  espacio   numero)")
	input(f"{player.name}, elige las coordenadas de tus barcos [ENTER]")

	boatIndex = 0
	while boatIndex < BOAT_AMOUNT: 
		print(f"El barco tiene que medir: {boat_list[boatIndex]} casillas!")

		valid_input_1, letter, number = get_coord_input(boatIndex, "-INICIAL-", "BOAT")

		if (not valid_input_1):
			clear_screen()
			continue

		valid_input_2, letter2, number2 = get_coord_input(boatIndex, "-FINAL-", "BOAT")

		if (not valid_input_2):
			clear_screen()
			continue

		start_coord = Coordinate(letter, number)
		end_coord = Coordinate(letter2, number2)

		boat = Ship(0, start_coord, end_coord, [])

		# fill the missing props

		set_all_coordinates(boat)
		boat.size = boat.coords.__len__()

		if (boat.size != boat_list[boatIndex]):
			clear_screen()
			input(f"TAMAÑO INVALIDO DE BARCO, TIENE QUE MEDIR: {boat_list[boatIndex]} CASILLAS. [enter]")
			continue

		if not valid_boat(boat, allBoats):
			continue

		boat_placed = player.board.place_boat(boat)

		if (not boat_placed):
			continue
		
		allBoats.append(boat)
		player.board.display()
		boatIndex += 1

	player.ships = allBoats

def is_valid_coordinate(currentCoord: Coordinate, boat: Ship, allBoats: list[Ship], BOARD_SIZE: int) -> bool:    

	if (not isInBounds(currentCoord, BOARD_SIZE)):
		clear_screen()
		print("Out of bounds detected")
		return False

	if (isOverlappingBoats(currentCoord, allBoats)):
		clear_screen()
		print("Overlapping detected")
		return False
	
	if isADiagonal(boat):
		clear_screen()
		print("Diagonal detected")
		return False
	
	return True

def check_hit(player: Player, opponent: Player, coord: Coordinate) -> tuple:
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

def valid_shot(coord: Coordinate, player_attempts: list[Coordinate]) -> bool:

	if (not isInBounds(coord, BOARD_SIZE)):
		print("Fuera de los limites del tablero!")
		return False
	
	if (isOnTop(player_attempts, coord)):
		print("Ya disparaste ahi!")
		return False
	
	return True

def valid_boat(boat: Ship, compare_list: list[Ship]) -> bool:
	for coord in boat.coords:
		if (not is_valid_coordinate(coord, boat, compare_list, BOARD_SIZE)):
			return False
	return True

def get_coord_input(boatNumber: int, text: str, type: str) -> tuple:
	letter: str
	number: int
	try:
		if (type == "ATTACK"):
			parts = input(f"Introducir coordenada a atacar separadas por un espacio: ").split()
			letter: str = parts[0].upper()
			number = int(parts[1]) - 1
		else:
			parts = input(f"Bote nro {boatNumber + 1}: Introducir coordenada {text} separadas por un espacio: ").split()
			letter: str = parts[0].upper()
			number = int(parts[1]) - 1
	
		if len(parts) != 2:
			raise ValueError()

		return True, letter, number
	
	except ValueError:
		clear_screen()
		print("Se escribieron los valores de manera INVALIDA, reintentar. ej: A 1")
		return False, None, None
	
	except IndexError:
		clear_screen()
		print(f"Se escribio la coordenada de manera INVALIDA, reintentar. ej: A 1")
		return False, None, None
	except KeyboardInterrupt:
		print("Saliendo...")
		exit    
	
def set_all_coordinates(boat: Ship) -> None:
	allCoordinates: list[Coordinate] = []
	startCoord: Coordinate = boat.start_coord
	endCoord: Coordinate = boat.end_coord

	allCoordinates.append(startCoord)
	
	if (isVertical(boat)): 
		# get the missing numbers in the Y axis (number axis)
		missingCoords: list = get_numbers_between(startCoord.number, endCoord.number)
		for yCoords in missingCoords: 
			coordinate: Coordinate = Coordinate(startCoord.letter, yCoords)
			allCoordinates.append(coordinate)

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
	boat.coords = allCoordinates

def is_game_over(player: Player) -> bool:

	ships_sunk: int = 0
	player_ships_length: int = len(player.ships)

	if (player.shots <= 0):
		print(f"{player.name} se quedo sin tiros!")
		return True

	# check if all the ships are sunk (cant use my func here cuz it detects the same boat > twice)
	for boat in player.ships:
		if (boat.is_sunk()):
			ships_sunk += 1
	
	if (ships_sunk == player_ships_length):
		print(f"{player.name} se quedo sin barcos!")
		return True
	
	return False

def process_game_state(current_player: Player, opponent: Player): 
	if is_game_over(opponent):
		print(f"{current_player.name} gano!")
		current_player.board.display_two_boards(opponent.board, f"{opponent.name}")
		return True
	return False