

from src.game.tetramino import Tetramino

from src.common import GameMatrix, Shape, EMPTY_TILE
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
    
    def setGameOver(self, flag: bool) -> None:
        self._isGameOver = flag

    def getCurrent(self) -> Tetramino | None:
        return self._current
    
    def setCurrent(self, new_tetramino: Tetramino) -> None:
        self._current = new_tetramino

    def deleteCurrent(self) -> None:
        self.setCurrent(new_tetramino=None)

    @staticmethod
    def createGameMatrix(width: int, height: int) -> GameMatrix:
        return [[EMPTY_TILE for _ in range(width)] for _ in range(height)]
    
    def getGameMatrix(self) -> GameMatrix:
        return self._gameMatrix

    def setGameMatrix(self, new_matrix: GameMatrix) -> None:
        self._gameMatrix = new_matrix

    def getGameMatrixWithCurrentPiece(self) -> GameMatrix:

        ret: GameMatrix = copy.deepcopy(self.getGameMatrix())
        current_piece: Tetramino = self.getCurrent()

        if current_piece:
            cp_positions: list[Position2D] = current_piece.getAbsoluteCoordinates()
            for p in cp_positions:
                ret[p.y][p.x] = current_piece.getType().value

        return ret

    def getRow(self, row: int) -> list[int]:
        if 0 <= row < self.getHeight():
            return self.getGameMatrix()[row]
        else: raise ValueError(f'[E] Invalid row number (row={row})')

    def resetGameMatrix(self) -> None:
        self.setGameMatrix(new_matrix=self.createGameMatrix(width=self.getWidth(), height=self.getHeight()))

    def isPositionInMatrix(self, pos: Position2D) -> bool:
        return (0 <= pos.x < self.getWidth()) and (0 <= pos.y < self.getHeight())



    # Piece management (Move/Rotation/Spawn) + collision methods

    def isColliding(self, pos: Position2D, shape: Shape, move: Move | None = None, rotation: Rotation | None = None) -> bool:
        
        # On check si la pièce est à une position satisfaisante.

        if not self.getCurrent():
            return False

        move = move if move else Move.NONE
        rotation = rotation if rotation else Rotation.NONE

        temp: Tetramino = Tetramino(shapeType=None, pos=pos)
        temp.setShape(new_shape=shape)

        for p in temp.getAbsoluteCoordinates(topleft=temp.getMovePosition(move=move), shape=temp.getRotateShape(rotation=rotation)):

            # On vérifie que la position existe
            if not self.isPositionInMatrix(pos=p):
                return True
                    
            # On vérifie que si la pièce possède un bloc à la position relative, alors la
            # grid possède une place à la position absolue.
            if self.getTile(pos=p) != 0:
                return True
                    
        return False

    def canMove(self, piece: Tetramino, move: Move) -> bool:
        return not self.isColliding(pos=piece.getPosition(), shape=piece.getShape(), move=move, rotation=None)
    
    def canRotate(self, piece: Tetramino, rotation: Rotation) -> bool:
        return not self.isColliding(pos=piece.getPosition(), shape=piece.getShape(), move=None, rotation=rotation)
    
    def tryMoveCurrent(self, move: Move) -> bool:

        current_piece: Tetramino = self.getCurrent()
        
        # Si aucune pièce alors on ne peut rien faire, on return False.
        if not current_piece:
            return False
        
        # On regarde si on peut move
        canMove: bool = self.canMove(piece=current_piece, move=move)

        # Si c'est le cas, alors on récupère la nouvelle position et on set.
        if canMove:
            current_piece.setPosition(new_pos=current_piece.getMovePosition(move=move))

        return canMove

    def tryRotateCurrent(self, rotation: Rotation) -> bool:

        current_piece: Tetramino = self.getCurrent()

        # Si aucune pièce alors on ne peut rien faire, on return False.
        if not current_piece:
            return False
        
        # On regarde si on peut rotate
        canRotate: bool = self.canRotate(piece=current_piece, rotation=rotation)

        # Si c'est le cas, alors on récupère la nouvelle position et on set.
        if canRotate:
            current_piece.setShape(new_shape=current_piece.getRotateShape(rotation=rotation))

        return canRotate

    def getRowsToObstacle(self, piece: Tetramino) -> int:
        
        temp: Tetramino = Tetramino(shapeType=None, pos=piece.getPosition())
        temp.setShape(new_shape=piece.getShape())
        rowc: int = -1

        while not self.isColliding(pos=temp.getPosition(), shape=temp.getShape(), move=None, rotation=None):
            rowc += 1
            p: Position2D = temp.getPosition()
            temp.setPosition(new_pos=Position2D(p.x, p.y+1))

        del temp
        return rowc

    def tryMakeCurrentPieceInstantFall(self) -> bool:
        
        # On calcule le nombre de rows pour toucher un obstacle, puis on descend de ce nombre de rows.
        rows_to_obstacle: int = self.getRowsToObstacle(piece=self.getCurrent())
        for _ in range(rows_to_obstacle):
            self.tryApplyGravityOnCurrentPiece()
        return rows_to_obstacle > 0
    
    def placePiece(self, piece: Tetramino) -> bool:

        doesCollide: bool = self.isColliding(pos=piece.getPosition(), shape=piece.getShape(), move=None, rotation=None)
        
        # Si aucune collision alors on peut placer la pièce.
        if not doesCollide:

            for p in piece.getAbsoluteCoordinates(): 
                self.setTile(pos=p, value=piece.getType().value)

        return (not doesCollide)
    
    def tryPlaceCurrentPiece(self) -> bool:

        # On tente de placer la pièce.
        could_place: bool = self.placePiece(piece=self.getCurrent())
        self.deleteCurrent()  # Puis on la delete.
        return could_place

    def spawnPiece(self, t: Tetramino, tl_spawnbox: Position2D) -> bool:
          
        t.setPosition(new_pos=tl_spawnbox)  # On met la pièce dans la spawnbox
        does_collide: bool = self.isColliding(pos=t.getPosition(), shape=t.getShape(), move=None, rotation=None)
        
        # Si on collide alors que dans la spawnbox, alors gameover. Sinon, la current piece devient t.

        if not does_collide:
            self.setCurrent(new_tetramino=t)
        
        else:
            self.setGameOver(flag=True)

        return (not does_collide)

    def tryApplyGravityOnCurrentPiece(self) -> bool:
        
        if not self.getCurrent():
            return False
        
        could_fall: bool = self.tryMoveCurrent(move=Move.DOWN)

        return could_fall
            

    # Matrix management / Line clear

    def getTile(self, pos: Position2D) -> int:
        return self.getGameMatrix()[pos.y][pos.x]

    def setTile(self, pos: Position2D, value: int) -> None:
        self.getGameMatrix()[pos.y][pos.x] = value

    def clearSingleLine(self, row_id: int) -> None:

        row: list[int] = self.getRow(row=row_id)

        for i in range(self.getWidth()): 
            row[i] = EMPTY_TILE

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

        for j in range(row_id, -1, -1):
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
            full_lines_count += 1
            self.applyGravity(row_id=j-1)

        return full_lines_count


