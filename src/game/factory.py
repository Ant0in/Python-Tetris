

from src.game.tetramino import Tetramino
from src.common import ShapeType, Position2D

import random



class TetraminoFactory:


    default_pos: Position2D = Position2D(0, 0)
    possible_pieces: list[ShapeType] = [ShapeType.J, ShapeType.L, ShapeType.O, ShapeType.S, ShapeType.Z, ShapeType.T, ShapeType.I]


    def __init__(self) -> None:
        
        self._pool: list[Tetramino | None] = list()
        self.fillPool()

    def getPool(self) -> list[Tetramino | None]:
        return self._pool
    
    def pushPiece(self, p: Tetramino) -> None:
        self.getPool().append(p)

    def popPiece(self) -> Tetramino:
        
        next: Tetramino | None = None

        if not self.isPoolEmpty():
            next = self.getPool().pop(-1)

        if self.isPoolEmpty():
            self.fillPool()

        return next

    def whatIsNextPiece(self) -> Tetramino:

        next: Tetramino | None = None

        if not self.isPoolEmpty():
            next = self.getPool()[-1]

        return next

    def getPoolSize(self) -> int:
        return len(self.getPool())

    def isPoolEmpty(self) -> bool:
        return self.getPoolSize() == 0

    def fillPool(self) -> None:
        
        if self.isPoolEmpty():
            
            for p in random.sample(TetraminoFactory.possible_pieces, len(TetraminoFactory.possible_pieces)):
                self.pushPiece(p=Tetramino(shapeType=p, pos=TetraminoFactory.default_pos))


