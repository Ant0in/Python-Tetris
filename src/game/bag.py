

from src.game.tetramino import Tetramino



class Bag:

    def __init__(self) -> None:
        
        self._stored_piece: Tetramino | None = None

    def __repr__(self) -> str:
        return f'[BAG] contains : {self.getStoredPiece()}' if not self.isEmpty() else '[BAG] empty'

    def getStoredPiece(self) -> Tetramino | None:
        return self._stored_piece

    def setStoredPiece(self, p: Tetramino | None) -> None:
        self._stored_piece = p

    def retrievePiece(self) -> Tetramino | None:
        ret: Tetramino | None = self.getStoredPiece()
        self.setStoredPiece(p=None)
        return ret
    
    def isEmpty(self) -> bool:
        return (self.getStoredPiece() is None)
    

