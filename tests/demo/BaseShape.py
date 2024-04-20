
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger
from typing import Tuple
from typing import cast

from wx import DC

from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Rectangle import Rectangle
from pyorthogonalrouting.Size import Size

from tests.demo.DemoSelectorShape import DemoSelectorShape
from tests.demo.DemoSelectorShape import DemoSelectorShapes
from tests.demo.ShapeEventHandler import ShapeEventHandler


class BaseShape(Rectangle, ShapeEventHandler):

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__(left, top, width, height)

        self._baseLogger: Logger = getLogger(__name__)

        self.selected: bool = False

        self._northSelector: DemoSelectorShape = cast(DemoSelectorShape, None)
        self._southSelector: DemoSelectorShape = cast(DemoSelectorShape, None)
        self._eastSelector:  DemoSelectorShape = cast(DemoSelectorShape, None)
        self._westSelector:  DemoSelectorShape = cast(DemoSelectorShape, None)

        self._createSelectors()

        self._selectorShapes: DemoSelectorShapes = DemoSelectorShapes([
            self._northSelector, self._southSelector, self._eastSelector, self._westSelector
        ])

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

    @property
    def selectors(self) -> DemoSelectorShapes:
        return self._selectorShapes

    def drawSelectors(self, dc: DC):
        self._northSelector.draw(dc=dc)
        self._southSelector.draw(dc=dc)
        self._eastSelector.draw(dc=dc)
        self._westSelector.draw(dc=dc)

    def inside(self, x, y) -> bool:
        """
        Only works for rectangles

        Args:
            x:
            y:

        Returns:  True if (x, y) is inside the rectangle.
        """
        return self.contains(p=Point(x=x, y=y))

    def _createSelectors(self):

        shapeSize: Size = self.size

        x: int = shapeSize.width // 2
        y: int = 0
        self._northSelector = DemoSelectorShape(parent=self, x=x, y=y)

        x = shapeSize.width // 2
        y = shapeSize.height
        self._southSelector = DemoSelectorShape(parent=self, x=x, y=y)

        x = shapeSize.width
        y = shapeSize.height // 2
        self._eastSelector = DemoSelectorShape(parent=self, x=x, y=y)

        x = 0
        y = shapeSize.height // 2
        self._westSelector = DemoSelectorShape(parent=self, x=x, y=y)


BaseShapes = NewType('BaseShapes', List[BaseShape])
