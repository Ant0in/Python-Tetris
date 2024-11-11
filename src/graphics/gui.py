

from src.game.tetramino import Tetramino
from src.game.gameboard import GameBoard
from src.game.bag import Bag
from src.game.factory import TetraminoFactory
from src.game.score import Score
from src.game.tetris_game import TetrisGame

from src.controller import GameController

from src.common import GameMatrix, Shape
from src.common import Position2D, Move, Rotation, ShapeType


import os



class ShellGUI:

    def __init__(self, tetris_game: TetrisGame) -> None:

        self._tetris_game: TetrisGame = tetris_game

    def getTetrisGame(self) -> TetrisGame:
        return self._tetris_game
    
    def flush(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self) -> None:
        
        self.flush()
        ...
