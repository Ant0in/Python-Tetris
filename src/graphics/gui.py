

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
        self.flush()  # init flush

    def getTetrisGame(self) -> TetrisGame:
        return self._tetris_game

    @staticmethod
    def flush() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self) -> None:
        
        print('\033[H', end='')

        board: list[str] = self.get_board_display()
        bag: list[str] = self.get_single_piece_display(title='HOLD', piece=self.getTetrisGame().getBag().getStoredPiece())
        next_piece: list[str] = self.get_single_piece_display(title='NEXT', piece=self.getTetrisGame().getFactory().whatIsNextPiece())
        score: list[str] = self.get_score_display()

        space: int = 6
        bag_start: int = 7
        next_start: int = 1
        score_start: int = 14

        for i in range(len(board)):
            print(board[i], end=' '*space)
            if bag_start <= i < bag_start + len(bag): print(bag[i - bag_start], end='')
            if next_start <= i < next_start + len(next_piece): print(next_piece[i - next_start], end='')
            if score_start <= i < score_start + len(score): print(score[i - score_start], end='')
            print('')

    def get_board_display(self, piece_thickness: int = 2) -> str:

        board: GameBoard = self.getTetrisGame().getGameBoard()
        mat: GameMatrix = board.getGameMatrixWithCurrentPiece()
        separator: str = '+' + '—' * board.getWidth() * piece_thickness + '+'

        ret: list[str] = list()
        
        for row in mat:
            line = '|' + ''.join([f"{ShellGUI.COLORS_ANSI[v]}{('█' if v != 0 else ' ')*piece_thickness}{ShellGUI.COLORS_ANSI['end']}" for v in row]) + '|'
            ret.append(line)

        return [separator] + ret + [separator]
    
    def get_single_piece_display(self, title: str, piece: Tetramino | None, piece_thickness: int = 2) -> str:
        
        ret: list = list()
    
        canvas: GameMatrix = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        if piece:
            pshape: Shape = piece.getShape()
            for y, row in enumerate(pshape):
                for x, val in enumerate(row):
                    canvas[y][x] = val

        piece_type: int = piece.getType().value if piece else 0

        title: str = '|' + ' '*piece_thickness + title + ' '*piece_thickness + '|'
        border: str = '+' + '—'*piece_thickness*len(canvas) + '+'

        for row in canvas[:-1:]:
            line: str = ''.join([f"{ShellGUI.COLORS_ANSI[piece_type]}{('█' if v != 0 else ' ')*piece_thickness}{ShellGUI.COLORS_ANSI['end']}" for v in row])
            line = '|' + line + '|'
            ret.append(line)

        return [border, title] + ret + [border]

    def get_score_display(self) -> list[str]:

        return [
            '== SCORE ==',
            f'>> {self.getTetrisGame().getScore().getScore()}'
        ]

