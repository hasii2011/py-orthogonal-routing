
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger
from typing import Tuple

from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Rectangle import Rectangle

from tests.demo.ShapeEventHandler import ShapeEventHandler


class BaseShape(Rectangle, ShapeEventHandler):

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__(left, top, width, height)

        self._baseLogger: Logger = getLogger(__name__)

        self.selected: bool = False

    @property
    def position(self) -> Tuple[int, int]:
        return self._left, self._top

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._left = value[0]
        self._top  = value[1]

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
        return self.contains(p=Point(x=x, y=y))


BaseShapes = NewType('BaseShapes', List[BaseShape])
