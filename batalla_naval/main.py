"""
	Authors: Facundo Loucim, Maximo Sanguinetti, Agustin Geonas
	Date: 4/4/2025
"""
from config import DEBUG_MODE
from utils.classes import Player, Coordinate, no_validation_paint_symbols
from utils.helper import *
from utils.main_funcs import *

name_1 = input("Nombre jugador 1: ")
name_2 = input("Nombre jugador 2: ")

playerOne = setup_player(name_1)
playerTwo = setup_player(name_2)

def setup_game():
	chooseBoatLocations(playerOne)
	chatgpt_clear_screen()
	chooseBoatLocations(playerTwo)
	chatgpt_clear_screen()

def main():
	if DEBUG_MODE: # set this to false when playin the game (los botes default no reflejan la consigna)
		no_validation_paint_symbols(playerOne, playerOne.ships)
		no_validation_paint_symbols(playerTwo, playerTwo.ships)
	else:
		setup_game()
	
	play_game()
		
def play_game():
	print("Empezo el juego!")

	win: bool = False
	current_player: Player = playerOne
	opponent: Player = playerTwo

	while not win:
		print(f"{current_player.name}, es tu turno")
		
		current_player.board.display_two_boards(current_player.attack_board)

		valid, letter, number = get_coord_input(0, "", "ATTACK")

		if (not valid):
			continue

		coord = Coordinate(letter, number)

		# debug(current_player)
		# debug(opponent)

		if (not valid_shot(coord, current_player.attempts)):
			print("TIRO INVALIDO, vuelve a intentar.")
			continue

		current_player.attempts.append(coord)
		hit, target_boat = check_hit(current_player, opponent, coord)

		if (hit):
			clear_screen()
			chatgpt_clear_screen()
			if (target_boat.is_sunk()):
				input(f"{current_player.name} hundiste un barco!")
			win = process_game_state(current_player, opponent)

			if (win):
				break
			
			print("- - - - NO SE ROMPIO, SOLO SE BORRO EL LOG - - - - dont wory be hapy")
			print("Vuelve a disparar!")
			continue
		
		win = process_game_state(current_player, opponent)
		current_player.shots -= 1
		current_player, opponent = opponent, current_player
		chatgpt_clear_screen()
		pause_time()
		print("- - - - NO SE ROMPIO, SOLO SE BORRO EL LOG - - - - dont wory be hapy")
		
if (__name__ == "__main__"):
	main()

