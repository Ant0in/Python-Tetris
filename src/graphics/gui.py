

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

    COLORS_ANSI: dict[int|str: str] = {
        0: '\033[37m',          # blanc
        1: '\033[33m',          # jaune
        2: '\033[38;5;214m',    # orange
        3: '\033[32m',          # vert
        4: '\033[35m',          # mauve
        5: '\033[31m',          # rouge
        6: '\033[36m',          # cyan
        7: '\033[34m',          # bleu foncé
        'end': '\033[0m'        # /end/
    }

    def __init__(self, tetris_game: TetrisGame) -> None:

        self._tetris_game: TetrisGame = tetris_game

    def getTetrisGame(self) -> TetrisGame:
        return self._tetris_game
    
    def flush(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self) -> None:
        
        self.flush()
        print(f'Next Piece : {self.getTetrisGame().getFactory().whatIsNextPiece()}')
        print(f'{self.getTetrisGame().getBag()}')
        self.display_board()

    def display_board(self) -> str:

        board: GameBoard = self.getTetrisGame().getGameBoard()
        mat: GameMatrix = board.getGameMatrixWithCurrentPiece()
        separator: str = '+' + '—' * board.getWidth() * 2 + '+'

        ret: list[str] = [separator]
        for row in mat:
            line: str = ''
            for v in row:
                line += f"{ShellGUI.COLORS_ANSI[v]}{'██' if v!=0 else '  '}{ShellGUI.COLORS_ANSI['end']}" 
            ret.append('|' + line + '|')
        ret.append(separator)

        print('\n'.join(ret))

