

from src.game.tetramino import Tetramino
from src.game.gameboard import GameBoard
from src.game.bag import Bag
from src.game.factory import TetraminoFactory
from src.game.score import Score

from src.controller import GameController

from src.common import GameMatrix, Shape
from src.common import Position2D, Move, Rotation, ShapeType





class TetrisGame:

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