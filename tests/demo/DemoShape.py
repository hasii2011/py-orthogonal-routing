
from logging import Logger
from logging import getLogger
from typing import List
from typing import NewType

from wx import DC
from wx import Pen
from wx import RED_PEN

from tests.demo.BaseShape import BaseShape

ROUNDED_RECTANGLE_RADIUS: int = 8


class DemoShape(BaseShape):

    nextId: int = 0

    def __init__(self, left: int, top: int, width: int, height: int):

        super().__init__(left, top, width, height)

        self.logger: Logger = getLogger(__name__)

        self._identifier: int = DemoShape.nextId

        DemoShape.nextId += 1

    def draw(self, dc: DC):

        savePen: Pen = dc.GetPen()

        if self.selected is True:
            dc.SetPen(RED_PEN)
        dc.DrawRoundedRectangle(x=self.left, y=self.top, width=self.width, height=self.height, radius=ROUNDED_RECTANGLE_RADIUS)

        dc.SetPen(savePen)

    @property
    def identifier(self) -> int:
        return self._identifier


Shapes = NewType('Shapes', List[DemoShape])
