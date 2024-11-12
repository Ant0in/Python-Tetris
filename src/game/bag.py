

from src.game.tetramino import Tetramino



class Bag:

    def __init__(self) -> None:
        
        self._stored_piece: Tetramino | None = None
        self._isUsable: bool = True

    def __repr__(self) -> str:
        return f'[BAG] contains : {self.getStoredPiece()}'

    def getStoredPiece(self) -> Tetramino | None:
        return self._stored_piece

    def setStoredPiece(self, p: Tetramino | None) -> None:
        self._stored_piece = p

    def retrievePiece(self) -> Tetramino | None:
        ret: Tetramino | None = self.getStoredPiece()
        self.setStoredPiece(p=None)
        ret.reset()
        return ret
    
    def isEmpty(self) -> bool:
        return (self.getStoredPiece() is None)
    
    def isUsable(self) -> bool:
        return self._isUsable
    
    def setUsableFlag(self, flag: bool) -> None:
        self._isUsable = flag
    

