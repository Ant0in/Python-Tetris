

from enum import Enum
from typing import Any, List


# Alias pour les shapes
GameMatrix = List[List[int]]
Shape = List[List[int]]



class Position2D:

    def __init__(self, _x: int, _y: int) -> None:
        self._x: int = _x
        self._y: int = _y

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
    @property
    def coords(self) -> tuple[int, int]:
        return self.x, self.y
    
    def __repr__(self) -> str:
        return f'{self.coords}'


class ShapeType(Enum):
    O = 1
    L = 2
    S = 3
    T = 4
    Z = 5
    I = 6
    J = 7


class Move(Enum):
    NONE = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Rotation(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


