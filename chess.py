"""
CMPUT 275 Final Project: pyChess
Mohammad Kebbi; 1496572
Sheetal Gour; 1547017
Main Functon that initializes the User Interface class to run the chess
Game on pygame
"""
import pygame
from board import ChessBoard
from userInterface import UserInterface
if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode([600, 600], 0, 0)
    pygame.display.set_caption('pyChess')
    Board = ChessBoard()
    UI = UserInterface(surface, Board)
    UI.playGame()
    pygame.quit()
