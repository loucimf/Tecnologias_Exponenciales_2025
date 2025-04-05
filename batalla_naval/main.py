"""
    Authors: Facundo Loucim, Maximo Sanguinetti, Agustin Geonas
    Date: 4/4/2025
"""

from utils.classes import Board, Player, Ship

boardSize: int = 10

playerOne_default_board = Board(boardSize)
playerOne_attack_board = Board(boardSize)
playerOne = Player(playerOne_default_board, playerOne_attack_board, "Pepe", [], 10)

playerOne.board.place_symbol(1, 2, "▮")
playerOne.board.display()
"""
if __name__ == "__main__":
    juego = Game()
    juego.add_player("Jugador 1", modo='manual')
    juego.add_player("Jugador 2", modo='auto')
    juego.start_game()
    https://chatgpt.com/share/67f14c57-7218-8000-9525-30d3d1ee229e
"""