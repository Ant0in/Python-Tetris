

from src.game.tetramino import Tetramino
from src.game.gameboard import GameBoard
from src.game.bag import Bag
from src.game.factory import TetraminoFactory
from src.game.score import Score
from src.game.tetris_game import TetrisGame

from src.controller import GameController

from src.common import GameMatrix, Shape
from src.common import Position2D, Move, Rotation, ShapeType

from src.graphics.gui import ShellGUI


import time




if __name__ == '__main__':

    game: TetrisGame = TetrisGame()
    gc: GameController = GameController()