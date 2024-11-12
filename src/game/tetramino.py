

from src.common import Position2D, Rotation, Move, ShapeType
from src.common import Shape



class Tetramino:

    def __init__(self, shapeType: ShapeType, pos: Position2D) -> None:
        
        self._position: Position2D = pos
        self._shapeType: ShapeType = shapeType
        self._shape: Shape = self.generateShapeByType(shapeType=shapeType)

    def __repr__(self) -> str:
        return f'Tetramino {self.getType().name} @ {self.getPosition()}'
    
    def __eq__(self, other: 'Tetramino') -> bool:
        return self.getPosition() == other.getPosition() and self.getShape() == other.getShape()

    def getPosition(self) -> Position2D:
        return self._position
    
    def setPosition(self, new_pos: Position2D) -> None:
        self._position = new_pos

    def getType(self) -> ShapeType:
        return self._shapeType
    
    def setType(self, new_type: ShapeType | None) -> None:
        self._shapeType = new_type

    def getShape(self) -> Shape:
        return self._shape

    def setShape(self, new_shape: Shape) -> None:
        self._shape = new_shape

    @staticmethod
    def generateShapeByType(shapeType: ShapeType | None) -> Shape | None:
        
        match shapeType:

            case ShapeType.O:
                return [
                    [1, 1],
                    [1, 1]
                ]
            
            case ShapeType.L:
                return [
                    [0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]
                ]
            
            case ShapeType.S:
                return [
                    [0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]
                ]
            
            case ShapeType.T:
                return [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ]
            
            case ShapeType.Z:
                return [
                    [1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]
                ]
            
            case ShapeType.I:
                return [
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            
            case ShapeType.J:
                return [
                    [1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ]
            
            case None:
                return None

            case _:
                raise NotImplementedError(f'[E] Unknown piece type ({shapeType}).')

    def reset(self) -> None:
        self.setPosition(new_pos=Position2D(0, 0))
        self.setShape(new_shape=self.generateShapeByType(shapeType=self.getType()))

    def getMovePosition(self, move: Move) -> Position2D:

        current_pos: Position2D = self.getPosition()

        match move:
            case Move.LEFT: return Position2D(current_pos.x - 1, current_pos.y)
            case Move.RIGHT: return Position2D(current_pos.x + 1, current_pos.y)
            case Move.DOWN: return Position2D(current_pos.x, current_pos.y + 1)
            case Move.NONE: return Position2D(current_pos.x, current_pos.y)
            case _: raise NotImplementedError(f'[E] Unknown direction type ({move}).')
    
    def getRotateShape(self, rotation: Rotation) -> Shape:
        
        shape: Shape = self.getShape()

        match rotation:
            case Rotation.RIGHT: return [list(row)[::-1] for row in zip(*shape)]
            case Rotation.LEFT: return [list(row) for row in zip(*shape)][::-1]
            case Rotation.NONE: return shape
            case _: raise NotImplementedError(f'[E] Unknown rotation type ({rotation}).')

    def getAbsoluteCoordinates(self, topleft: Position2D | None = None, shape: Shape | None = None) -> list[Position2D]:

        topleft = topleft if topleft else self.getPosition()
        shape = shape if shape else self.getShape()

        ret: list[Position2D] = list()

        for rel_y, row in enumerate(shape):
            for rel_x, v in enumerate(row):

                if v != 0:
                    abs_x: int = rel_x + topleft.x
                    abs_y: int = rel_y + topleft.y
                    abs_pos: Position2D = Position2D(abs_x, abs_y)
                    ret.append(abs_pos)

        return ret
