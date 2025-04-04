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

