

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
    # Pour un level, combien de frame pour 
    # effectuer une logique de gravité
       -1: float('inf'),
        0: 60,
        1: 30,
        2: 15,
        3: 10,
        4:  8,
        5:  6,
        6:  5
    }


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
        self._level: int = 4

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
    
    def shouldApplyGravity(self) -> bool:

        frame: int = self.getFrame()
        frame_quantum: int = self.SPEED_TABLE[self.getLevel()]
        return (frame % frame_quantum == 0 and frame > frame_quantum)


