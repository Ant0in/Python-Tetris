

from src.game.tetramino import Tetramino

from src.common import GameMatrix, Shape
from src.common import Position2D, Move, Rotation, ShapeType

import copy



class GameBoard:

    def __init__(self, tetramino: Tetramino | None = None, width: int = 10, height: int = 22) -> None:
        
        self._isGameOver: bool = False
        self._current: Tetramino | None = tetramino
        self._width: int = width
        self._height: int = height
        self._gameMatrix: GameMatrix = self.createGameMatrix(width=self.getWidth(), height=self.getHeight())


    # getters/setters/reset

    def getWidth(self) -> int:
        return self._width
    
    def getHeight(self) -> int:
        return self._height

    def isGameOver(self) -> bool:
        return self._isGameOver
    
    def getCurrent(self) -> Tetramino | None:
        return self._current
    
    def setCurrent(self, new_tetramino: Tetramino) -> None:
        self._current = new_tetramino

    def deleteCurrent(self) -> None:
        self.setCurrent(new_tetramino=None)

    @staticmethod
    def createGameMatrix(width: int, height: int) -> GameMatrix:
        return [[0 for _ in range(width)] for _ in range(height)]
    
    def getGameMatrix(self) -> GameMatrix:
        return self._gameMatrix

    def setGameMatrix(self, new_matrix: GameMatrix) -> None:
        self._gameMatrix = new_matrix

    def getRow(self, row: int) -> list[int]:
        if 0 <= row < self.getHeight():
            return self.getGameMatrix()[row]
        else: raise ValueError(f'[E] Invalid row number (row={row})')

    def resetGameMatrix(self) -> None:
        self.setGameMatrix(new_matrix=self.createGameMatrix(width=self.getWidth(), height=self.getHeight()))

    def isPositionInMatrix(self, pos: Position2D) -> bool:
        return (0 <= pos.x < self.getWidth()) and (0 <= pos.y < self.getHeight())



    # Move/Rotation + collision methods

    def isColliding(self, pos: Position2D, shape: Shape, move: Move | None = None, rotation: Rotation | None = None) -> bool:
        # On check si la pièce est à une position satisfaisante.
        
        move = move if move else Move.NONE
        rotation = rotation if rotation else Rotation.NONE

        t: Tetramino = Tetramino(shapeType=None, pos=pos)
        t.setShape(new_shape=shape)

        for p in t.getAbsoluteCoordinates(topleft=t.getMovePosition(move=move), shape=t.getRotateShape(rotation=rotation)):

            # On vérifie que la position existe
            if not self.isPositionInMatrix(pos=p):
                return False
                    
            # On vérifie que si la pièce possède un bloc à la position relative, alors la
            # grid possède une place à la position absolue.
            if self.getTile(pos=p) != 0:
                return False
                    
        return True

    def canMove(self, piece: Tetramino, move: Move) -> bool:
        return self.isColliding(pos=piece.getPosition(), shape=piece.getShape(), move=move, rotation=None)
    
    def canRotate(self, piece: Tetramino, rotation: Rotation) -> bool:
        return self.isColliding(pos=piece.getPosition(), shape=piece.getShape(), move=None, rotation=rotation)
    
    def tryMoveCurrent(self, move: Move) -> bool:
        current_piece: Tetramino = self.getCurrent()    
        possible: bool = self.canMove(piece=current_piece, move=move)
        if possible: current_piece.setPosition(new_pos=current_piece.getMovePosition(move=move))
        return possible

    def tryRotateCurrent(self, rotation: Rotation) -> bool:
        current_piece: Tetramino = self.getCurrent()    
        possible: bool = self.canRotate(piece=current_piece, rotation=rotation)
        if possible: current_piece.setShape(new_shape=current_piece.getRotateShape(rotation=rotation))
        return possible

    def getRowsToObstacle(self, piece: Tetramino) -> int:
        
        rows_count: int = 0
        shape: Shape = piece.getShape()
        pos: Position2D = piece.getPosition()

        while not self.isColliding(pos=pos, shape=shape, move=None, rotation=None):
            rows_count += 1
            pos = Position2D(pos.x, pos.y + 1)

        return rows_count
    
    def placePiece(self, piece: Tetramino) -> bool:

        can_place: bool = (not self.isColliding(pos=piece.getPosition(), shape=piece.getShape(), move=None, rotation=None))
        
        if can_place:
            for p in piece.getAbsoluteCoordinates(topleft=piece.getPosition(), shape=piece.getShape()): 
                self.setTile(pos=p, value=1)

        return can_place
    
    def tryPlaceCurrentPiece(self) -> bool:
        s: bool = self.placePiece(piece=self.getCurrent())
        self.deleteCurrent()
        return s


    # Matrix management / Line clear

    def getTile(self, pos: Position2D) -> int:
        return self.getGameMatrix()[pos.y][pos.x]

    def setTile(self, pos: Position2D, value: int) -> None:
        self.getGameMatrix()[pos.y][pos.x] = value

    def clearSingleLine(self, row_id: int) -> None:

        row: list[int] = self.getRow(row=row_id)

        for i in range(self.getWidth()): 
            row[i] = 0

    def applyGravityToSingleLine(self, row_id: int) -> None:
        
        # La ligne du bas ne peut pas subir de gravité
        if row_id == self.getHeight() - 1:
            return
        
        # On clear en premier lieu la ligne du dessous.
        self.clearSingleLine(row_id=row_id+1)
        # Puis on clone chaque valeur de la ligne sur la ligne du dessous.
        for i, v in enumerate(self.getRow(row=row_id)):
            p: Position2D = Position2D(i, row_id+1)  # Ligne du dessous
            self.setTile(pos=p, value=v)
        # Puis enfin on clear la ligne en row_id, qui est l'ancienne position de notre row.
        self.clearSingleLine(row_id=row_id)

    def applyGravity(self, row_id: int) -> None:
        
        # On a besoin d'une fonction qui applique la gravité à la ligne row_id, ce qui
        # implique d'appliquer la gravités à toutes les lignes du dessus.

        for j in range(0, row_id, -1):
            self.applyGravityToSingleLine(row_id=j)

    def isLineFull(self, row_id: int) -> bool:
        
        row: list[int] = self.getRow(row=row_id)
        # all renvoie True si toutes les valeurs d'un itérable sont True.
        return all(row)
    
    def clearFullLines(self) -> int:

        # On veut compter le nombre de lignes full, les clear puis renvoyer ce nombre.
        full_lines_count: int = 0
        cleared_lines_row: list[int] = []

        for row_id in range(self.getHeight()):

            # La ligne est remplie
            if self.isLineFull(row_id=row_id):
                self.clearSingleLine(row_id=row_id)  # On supprime la ligne
                cleared_lines_row.append(row_id)

        for j in cleared_lines_row:
            # On applique la gravité correctement, en commençant des lignes les plus basses vers les plus hautes.
            self.applyGravity(row_id=j)

        return full_lines_count

