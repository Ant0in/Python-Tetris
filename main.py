

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



if __name__ == '__main__':

    game: TetrisGame = TetrisGame()
    gui: ShellGUI = ShellGUI(tetris_game=game)
    gui.display()