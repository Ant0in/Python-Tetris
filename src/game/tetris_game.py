

from src.game.tetramino import Tetramino
from src.game.gameboard import GameBoard
from src.game.bag import Bag
from src.game.factory import TetraminoFactory
from src.game.score import Score

from src.controller import GameController

from src.common import GameMatrix, Shape
from src.common import Position2D, Move, Rotation, ShapeType





class TetrisGame:


    SPEED_TABLE: dict = {
        0: 48, 1: 43, 2: 38, 3: 33, 4: 28, 5: 23, 6: 18, 7: 13, 8: 8, 9: 6,
        10: 5, 11: 5, 12: 5,
        13: 4, 14: 4, 15: 4,
        16: 3, 17: 3, 18: 3,
        19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2, 25: 2, 26: 2, 27: 2, 28: 2,
        29: 1}
    LINES_TO_LEVELUP: int = 10


    def __init__(self,
                 game_board: GameBoard | None = None,
                 factory: TetraminoFactory | None = None,
                 bag: Bag | None = None,
                 score: Score | None = None,
                 controller: GameController | None = None
    ) -> None:
        
        # game features
        self._game_board: GameBoard = game_board if game_board else GameBoard()
        self._factory: TetraminoFactory = factory if factory else TetraminoFactory()
        self._bag: Bag = bag if bag else Bag()
        self._score: Score = score if score else Score()
        self._controller: GameController = controller if controller else GameController()

        # window/instance features
        self._frame: int = 0
        self._level: int = 0
        self._lines_cleared: int = 0

    def getGameBoard(self) -> GameBoard:
        return self._game_board
    
    def getFactory(self) -> TetraminoFactory:
        return self._factory
    
    def getBag(self) -> Bag:
        return self._bag

    def getScore(self) -> Score:
        return self._score
    
    def getController(self) -> GameController:
        return self._controller
    
    def getFrame(self) -> int:
        return self._frame
    
    def setFrame(self, n: int) -> None:
        self._frame = n

    def incrementFrame(self) -> None:
        self.setFrame(self.getFrame() + 1)
    
    def getLevel(self) -> int:
        return self._level
    
    def setLevel(self, n: int) -> None:
        self._level = n

    def incrementLevel(self, q: int = 1) -> None:
        self.setLevel(self.getLevel() + q)

    def getLinesCleared(self) -> int:
        return self._lines_cleared
    
    def setLinesCleared(self, n: int) -> None:
        self._lines_cleared = n

    def incrementLinesCleared(self, q: int) -> None:
        self.setLinesCleared(self.getLinesCleared() + q)
    
    def shouldApplyGravity(self) -> bool:

        frame: int = self.getFrame()
        frame_quantum: int = self.SPEED_TABLE.get(self.getLevel(), 1)
        return (frame % frame_quantum == 0 and frame >= frame_quantum)

    def shouldLevelUp(self) -> bool:
        return self.getLinesCleared() // self.LINES_TO_LEVELUP != self.getLevel()


