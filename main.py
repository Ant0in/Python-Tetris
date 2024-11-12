

from src.game.tetris_game import TetrisGame
from src.graphics.gui import ShellGUI
from src.engine import GameEngine

import time




if __name__ == '__main__':

    game: TetrisGame = TetrisGame()
    gui: ShellGUI = ShellGUI(tetris_game=game)
    REFRESH_RATE: float = 60.0

    while not game.getGameBoard().isGameOver():
        
        GameEngine.handling_routine(game=game)
        gui.display()
        time.sleep(1 / REFRESH_RATE)