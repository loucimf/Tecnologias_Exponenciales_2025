"""
	Authors: Facundo Loucim, Maximo Sanguinetti, Agustin Geonas
	Date: 4/4/2025
"""

from config import BOARD_SIZE, BOAT_AMOUNT, SHOTS
from utils.classes import Board, Player, Ship, Coordinate, DEFAULT_BOATS_COORDINATES, no_validation_paint_symbols
from utils.helper import set_all_coordinates, check_hit


playerOne_default_board = Board(BOARD_SIZE)
playerOne_attack_board = Board(BOARD_SIZE)
playerOne = Player(playerOne_default_board, playerOne_attack_board, "Pepe", DEFAULT_BOATS_COORDINATES, SHOTS)

playerTwo_default_board = Board(BOARD_SIZE)
playerTwo_attack_board = Board(BOARD_SIZE)
playerTwo = Player (playerTwo_default_board, playerTwo_attack_board, "Josefo", DEFAULT_BOATS_COORDINATES, SHOTS)


def chooseBoatLocations(player: Player): 
	allBoats: list[Ship] = []
	input(f"{player.name}, elige las coordenadas de tu barco")

	for boatIndex in range(BOAT_AMOUNT): 
		print("Todas las coordenadas deben estar en formato LETRA;NUMERO")

		letter1, number_raw_1 = input(f"Bote nro {boatIndex + 1}: Introducir coordenada inicial separadas por un espacio: ").split()
		number1 = int(number_raw_1)

		letter2, number_raw_2 = input(f"Bote nro {boatIndex + 1}: Introducir coordenada final separadas por un espacio: ").split()
		number2 = int(number_raw_2)

		start_coord = Coordinate(letter1, number1)
		end_coord = Coordinate(letter2, number2)

		boat = Ship(0, start_coord, end_coord, [])

		# fill the missing props
		set_all_coordinates(boat)
		boat.size = boat.coords.__len__()

		player.board.place_boat(boat, allBoats)

		allBoats.append(boat)
		player.board.display()

	print("All boats: ", allBoats)
	player.ships = allBoats


def main():
	#chooseBoatLocations(playerOne)
	#chooseBoatLocations(playerTwo)
	no_validation_paint_symbols(playerOne, playerOne.ships)
	no_validation_paint_symbols(playerTwo, playerTwo.ships)
	
	play_game()


def play_game():
	print("Welcome to Battleship!")

	win: bool = False
	current_player = playerOne
	opponent = playerTwo

	while not win:
		print(f"{current_player.name}, es tu turno")
		
		current_player.board.display()
		print("ATTACK BOARD")
		current_player.attack_board.display()

		letter, number_raw = input("Introduce la coordenada a atacar: ").split()
		number = int(number_raw)
		coord = Coordinate(letter, number)

		current_player.attempts.append(coord)
		current_player.shots -= 1

		check_hit(current_player, opponent, coord)
		check_ships(opponent)

		current_player, opponent = opponent, current_player

def check_ships(player: Player) -> bool:
	# check if all the ships are sunk
	for boat in player.ships:
		if (boat.__isSunk__()):
			print(f"{player.name} has sunk a ship!")

	if (player.ships.__len__() == 0):
		print(f"{player.name} has lost!")
		return True

	return False


if (__name__ == "__main__"):
	main()

