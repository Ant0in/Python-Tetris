

from src.game.gameboard import GameBoard
from src.game.tetris_game import TetrisGame

from src.graphics.gui import ShellGUI

from src.engine import GameEngine
import time




if __name__ == '__main__':

    gb: GameBoard = GameBoard(tetramino=None, width=10, height=22)
    game: TetrisGame = TetrisGame(game_board=gb)
    gui: ShellGUI = ShellGUI(tetris_game=game)
    REFRESH_RATE: float = 60.0

    while 1:
        
        GameEngine.handling_routine(game=game)
        gui.display()
        time.sleep(1 / REFRESH_RATE)