"""
	Authors: Facundo Loucim, Maximo Sanguinetti, Agustin Geonas
	Date: 4/4/2025
"""
from config import BOARD_SIZE, BOAT_AMOUNT, SHOTS, BOAT_SIZES_LIST
from utils.classes import Board, Player, Ship, Coordinate, no_validation_paint_symbols
from utils.helper import *


name_1 = input("Nombre jugador 1: ")
name_2 = input("Nombre jugador 2: ")

playerOne_default_board = Board(BOARD_SIZE)
playerOne_attack_board = Board(BOARD_SIZE)
playerOne = Player(playerOne_default_board, playerOne_attack_board, name_1, clone_boats(), SHOTS)

playerTwo_default_board = Board(BOARD_SIZE)
playerTwo_attack_board = Board(BOARD_SIZE)
playerTwo = Player(playerTwo_default_board, playerTwo_attack_board, name_2, clone_boats(), SHOTS)

boat_list = BOAT_SIZES_LIST


def chooseBoatLocations(player: Player): 

	allBoats: list[Ship] = []
	player.board.display()
	print("----Todas las coordenadas deben estar en formato LETRA NUMERO  (LETRA  espacio   numero)")
	input(f"{player.name}, elige las coordenadas de tus barcos [ENTER]")

	boatIndex = 0
	while boatIndex < BOAT_AMOUNT: 
		print(f"El barco tiene que medir: {boat_list[boatIndex]} casillas!")

		valid_input_1, letter, number = get_coord_input(boatIndex, "-INICIAL-")

		if (not valid_input_1):
			clear_screen()
			continue

		valid_input_2, letter2, number2 = get_coord_input(boatIndex, "-FINAL-")

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

def setup_game():
	chooseBoatLocations(playerOne)
	clear_screen()
	chooseBoatLocations(playerTwo)
	clear_screen()

def valid_boat(boat: Ship, compare_list: list[Ship]):
	for coord in boat.coords:
		if (not is_valid_coordinate(coord, boat, compare_list, BOARD_SIZE)):
			return False
	return True

def main():
	setup_game()
	#no_validation_paint_symbols(playerOne, playerOne.ships)
	#no_validation_paint_symbols(playerTwo, playerTwo.ships)
	
	play_game()



def check_game_over(player: Player) -> bool:

	ships_sunk: int = 0
	player_ships_length: int = player.ships.__len__()

	if (player.shots <= 0):
		print(f"{player.name} se quedo sin tiros!")
		return True

	# check if all the ships are sunk (cant use my func here cuz it detects the same boat > twice)
	for boat in player.ships:
		if (boat.__isSunk__()):
			ships_sunk += 1
		if (ships_sunk == player_ships_length):
			return True

	return False
		

def play_game():
	print("Empezo el juego!")

	win: bool = False
	current_player = playerOne
	opponent = playerTwo

	while not win:
		print(f"{current_player.name}, es tu turno")
		
		current_player.board.display_two_boards(current_player.attack_board)

		valid, letter, number = get_attack_coord_input()

		if (not valid):
			print("Invalido!")
			continue

		coord = Coordinate(letter, number)

		# debug(current_player)
		# debug(opponent)

		if (not valid_shot(coord, current_player.attempts)):
			print("TIRO INVALIDO, vuelve a intentar.")
			continue
		else:
			print("Tiro valido.")
		
		current_player.attempts.append(coord)
		
		hit, target_boat = check_hit(current_player, opponent, coord)
		clear_screen()

		if (hit and target_boat.__isSunk__()):
			input(f"{current_player.name} hundiste un barco!")
		
		if (check_game_over(opponent)):
			print(f"{current_player.name} gano!")
			current_player.board.display_two_boards(opponent.board, f"{opponent.name}")
			win = True
			break

		current_player.shots -= 1
		current_player, opponent = opponent, current_player
		pause_time()
		
if (__name__ == "__main__"):
	main()

