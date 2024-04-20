
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger

from tests.demo.ShapeEventHandler import ShapeEventHandler


class BaseShape(ShapeEventHandler):

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__()

        self._baseLogger: Logger = getLogger(__name__)

        self._left:   int = left
        self._top:    int = top
        self._width:  int = width
        self._height: int = height

        self.selected: bool = False

    @property
    def position(self) -> Tuple[int, int]:
        return self._left, self._top

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._left = value[0]
        self._top  = value[1]

    @property
    def bottom(self) -> int:
        return self._top + self._height

    @property
    def left(self) -> int:
        return self._left

    @property
    def top(self) -> int:
        return self._top

    @property
    def right(self) -> int:
        return self._left + self._width

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def size(self) -> Tuple[int, int]:
        return self._width, self._height

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value

    def inside(self, x, y) -> bool:
        """
        Only works for rectangles

        Args:
            x:
            y:

        Returns:  True if (x, y) is inside the rectangle.
        """
        return self.contains(x=x, y=y)

    # noinspection PyChainedComparisons
    def contains(self, x: int, y: int) -> bool:
        return x >= self._left and x <= self.right and y >= self._top and y <= self.bottom


BaseShapes = NewType('BaseShapes', List[BaseShape])
