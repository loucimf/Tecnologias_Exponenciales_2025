"""
	Authors: Facundo Loucim, Maximo Sanguinetti, Agustin Geonas
	Date: 4/4/2025
"""

from utils.classes import Board, Player, Ship, Coordinate
from utils.helper import set_all_coordinates

BOAT_AMOUNT: int = 5
# max 26 (alfabeto)
BOARD_SIZE: int = 10



def chooseBoatLocations(player: Player): 
	allBoats: list = []
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

	player.ships = allBoats



		


def main():

	playerOne_default_board = Board(BOARD_SIZE)
	playerOne_attack_board = Board(BOARD_SIZE)
	playerOne = Player(playerOne_default_board, playerOne_attack_board, "Pepe", [], 10)



	chooseBoatLocations(playerOne)


	playerTwo_default_board = Board(BOARD_SIZE)
	playerTwo_attack_board = Board(BOARD_SIZE)
	playerTwo = Player (playerTwo_default_board, playerTwo_attack_board, "Josefo", [], 10)

	chooseBoatLocations(playerTwo)


if (__name__ == "__main__"):
	main()

