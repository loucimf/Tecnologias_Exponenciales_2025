"""
	Authors: Facundo Loucim, Maximo Sanguinetti, Agustin Geonas
	Date: 4/4/2025
"""
from config import BOARD_SIZE, BOAT_AMOUNT, SHOTS
from utils.classes import Board, Player, Ship, Coordinate, no_validation_paint_symbols
from utils.helper import set_all_coordinates, check_hit, clone_boats, valid_shot

playerOne_default_board = Board(BOARD_SIZE)
playerOne_attack_board = Board(BOARD_SIZE)
playerOne = Player(playerOne_default_board, playerOne_attack_board, "Pepe", clone_boats(), SHOTS)

playerTwo_default_board = Board(BOARD_SIZE)
playerTwo_attack_board = Board(BOARD_SIZE)
playerTwo = Player (playerTwo_default_board, playerTwo_attack_board, "Josefo", clone_boats(), SHOTS)

player_one_name = input("Introduce el nombre del jugador 1: ")
player_two_name = input("Introduce el nombre del jugador 2: ")

playerOne.name = player_one_name
playerTwo.name = player_two_name


def chooseBoatLocations(player: Player): 
	allBoats: list[Ship] = []
	input(f"{player.name}, elige las coordenadas de tu barco")

	for boatIndex in range(BOAT_AMOUNT): 
		print("Todas las coordenadas deben estar en formato LETRA;NUMERO")

		letter1, number_raw_1 = input(f"Bote nro {boatIndex + 1}: Introducir coordenada inicial separadas por un espacio: ").split()
		number1 = int(number_raw_1) - 1

		letter2, number_raw_2 = input(f"Bote nro {boatIndex + 1}: Introducir coordenada final separadas por un espacio: ").split()
		number2 = int(number_raw_2) - 1

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
		

	return ships_sunk == player_ships_length

def play_game():
	print("Empezo el juego!")

	win: bool = False
	current_player = playerOne
	opponent = playerTwo

	while not win:
		print(f"{current_player.name}, es tu turno")
		
		current_player.board.display()
		print("ATTACK BOARD")
		current_player.attack_board.display()

		letter, number_raw = input("Introduce la coordenada a atacar: ").split()
		number = int(number_raw) - 1
		coord: Coordinate = Coordinate(letter, number)
		# debug(current_player)
		# debug(opponent)
		if (not valid_shot(current_player.attempts, coord)):
			continue

		hit, target_boat = check_hit(current_player, opponent, coord)
		current_player.shots -= 1
		current_player.attempts.append(coord)

		if (hit and target_boat.__isSunk__()):
			input(f"{current_player.name} hundiste un barco!")

		if (check_game_over(opponent)):
			print(f"{current_player.name} gano!")
			current_player.board.display()
			opponent.board.display()
			win = True
			continue

		current_player, opponent = opponent, current_player
		
if (__name__ == "__main__"):
	main()

