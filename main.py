

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


    gb: GameBoard = GameBoard(tetramino=None, width=10, height=22)
    fac: TetraminoFactory = TetraminoFactory()
    bag: Bag = Bag()
    score: Score = Score()
    gc: GameController = GameController(config=None)

    game: TetrisGame = TetrisGame(game_board=gb, factory=fac, bag=bag, score=score, controller=gc)
    gui: ShellGUI = ShellGUI(tetris_game=game)

    while 1:
        gui.display()
        time.sleep(1/60)