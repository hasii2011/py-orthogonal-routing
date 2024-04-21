
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from wx import DC
from wx import Pen
from wx import RED_PEN

from tests.demo.shapes.RectangleShape import RectangleShape
from tests.demo.shapes.DemoSelectorShape import DemoSelectorShape
from tests.demo.shapes.DemoSelectorShape import DemoSelectorShapes
from tests.demo.shapes.SelectorSide import SelectorSide

ROUNDED_RECTANGLE_RADIUS: int = 8


class DemoShape(RectangleShape):

    nextId: int = 0

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__(left, top, width, height)

        self.logger: Logger = getLogger(__name__)

        self._identifier: int = DemoShape.nextId

        DemoShape.nextId += 1

        self._topSelector:    DemoSelectorShape = cast(DemoSelectorShape, None)
        self._bottomSelector: DemoSelectorShape = cast(DemoSelectorShape, None)
        self._rightSelector:  DemoSelectorShape = cast(DemoSelectorShape, None)
        self._leftSelector:   DemoSelectorShape = cast(DemoSelectorShape, None)

        self._createSelectors()

        self._selectorShapes: DemoSelectorShapes = DemoSelectorShapes([
            self._topSelector, self._bottomSelector, self._rightSelector, self._leftSelector
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
        self._topSelector.draw(dc=dc)
        self._bottomSelector.draw(dc=dc)
        self._rightSelector.draw(dc=dc)
        self._leftSelector.draw(dc=dc)

    def _createSelectors(self):

        width, height = self.size

        x: int = width // 2
        y: int = 0
        self._topSelector = DemoSelectorShape(parent=self, side=SelectorSide.TOP, x=x, y=y)

        x = width // 2
        y = height
        self._bottomSelector = DemoSelectorShape(parent=self, side=SelectorSide.BOTTOM, x=x, y=y)

        x = width
        y = height // 2
        self._rightSelector = DemoSelectorShape(parent=self, side=SelectorSide.RIGHT, x=x, y=y)

        x = 0
        y = height // 2
        self._leftSelector = DemoSelectorShape(parent=self, side=SelectorSide.LEFT, x=x, y=y)

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

    def __repr__(self) -> str:
        return self.__str__()


DemoShapes = NewType('DemoShapes', List[DemoShape])
