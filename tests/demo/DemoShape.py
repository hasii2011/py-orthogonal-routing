
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from wx import DC
from wx import Pen
from wx import RED_PEN

from tests.demo.BaseShape import BaseShape
from tests.demo.DemoSelectorShape import DemoSelectorShape
from tests.demo.DemoSelectorShape import DemoSelectorShapes

ROUNDED_RECTANGLE_RADIUS: int = 8


class DemoShape(BaseShape):

    nextId: int = 0

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__(left, top, width, height)

        self.logger: Logger = getLogger(__name__)

        self._identifier: int = DemoShape.nextId

        DemoShape.nextId += 1

        self._northSelector: DemoSelectorShape = cast(DemoSelectorShape, None)
        self._southSelector: DemoSelectorShape = cast(DemoSelectorShape, None)
        self._eastSelector:  DemoSelectorShape = cast(DemoSelectorShape, None)
        self._westSelector:  DemoSelectorShape = cast(DemoSelectorShape, None)

        self._createSelectors()

        self._selectorShapes: DemoSelectorShapes = DemoSelectorShapes([
            self._northSelector, self._southSelector, self._eastSelector, self._westSelector
        ])

    @property
    def identifier(self) -> int:
        return self._identifier

    def draw(self, dc: DC):

        savePen: Pen = dc.GetPen()

        if self.selected is True:
            dc.SetPen(RED_PEN)
        dc.DrawRoundedRectangle(x=self.left, y=self.top, width=self.width, height=self.height, radius=ROUNDED_RECTANGLE_RADIUS)

        if self.selected is True:
            self._drawSelectors(dc=dc)

        dc.SetPen(savePen)

    @property
    def selectors(self) -> DemoSelectorShapes:
        return self._selectorShapes

    def _drawSelectors(self, dc: DC):
        self._northSelector.draw(dc=dc)
        self._southSelector.draw(dc=dc)
        self._eastSelector.draw(dc=dc)
        self._westSelector.draw(dc=dc)

    def _createSelectors(self):

        width, height = self.size

        x: int = width // 2
        y: int = 0
        self._northSelector = DemoSelectorShape(parent=self, x=x, y=y)

        x = width // 2
        y = height
        self._southSelector = DemoSelectorShape(parent=self, x=x, y=y)

        x = width
        y = height // 2
        self._eastSelector = DemoSelectorShape(parent=self, x=x, y=y)

        x = 0
        y = height // 2
        self._westSelector = DemoSelectorShape(parent=self, x=x, y=y)

    def __eq__(self, other) -> bool:

        ans: bool = False
        if isinstance(other, DemoShape) is False:
            pass
        else:
            if self.identifier == other.identifier:
                ans = True

        return ans

    def __str__(self) -> str:

        baseStr: str = super().__str__()
        ourStr:  str = f'identifier={self.identifier} {baseStr}'

        return ourStr


DemoShapes = NewType('DemoShapes', List[DemoShape])
