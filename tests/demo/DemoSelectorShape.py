
from typing import List
from typing import NewType
from typing import Tuple
from typing import cast
from typing import TYPE_CHECKING

from wx import Colour
from wx import DC
from wx import MouseEvent
from wx import Pen

from tests.demo.DemoColorEnum import DemoColorEnum
from tests.demo.ShapeEventHandler import ShapeEventHandler

if TYPE_CHECKING:
    from tests.demo.RectangleShape import RectangleShape


class DemoSelectorShape(ShapeEventHandler):

    SELECTION_ZONE: int = 8
    """
    A circle drawn on a shape
    """
    def __init__(self, parent: 'RectangleShape', x: int, y: int):
        """
        x and y are relative to parent

        Args:
            parent:  parent shape
            x:  x position of the point
            y:  y position of the point
        """
        super().__init__()
        self._parent: 'RectangleShape' = parent
        self._x:      int = x
        self._y:      int = y

        self._selectZone: int = DemoSelectorShape.SELECTION_ZONE

        self._penSaveColor: Colour = cast(Colour, None)

    @property
    def position(self) -> Tuple[int, int]:
        """
        Return the absolute position of the shape.
        It is in the diagram's coordinate system.

        Returns: An x,y tuple

        """
        if self._parent is not None:
            x, y = self._parent.position
            return self._x + x, self._y + y
        else:
            return self._x, self._y

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._x = value[0]
        self._y = value[1]

    @property
    def selectionZone(self) -> int:
        """
        Get the selection tolerance zone, in pixels.

        Returns: half of the selection zone.
        """

        return self._selectZone

    @selectionZone.setter
    def selectionZone(self, halfWidth: int):
        """
        Set the selection tolerance zone, in pixels.

        Args:
            halfWidth: half of the selection zone.
        """
        self._selectZone = halfWidth

    def onLeftDown(self, event: MouseEvent):
        """
        Args:
            event:
        """
        print(f'Clicked on me')
        event.Skip()    # Let other behavior happen

    def draw(self, dc: DC):
        """
        Draw the point on the dc.

        Args:
            dc:
        """
        self._penSaveColor = dc.GetPen().GetColour()
        self._setPenColor(dc)
        x, y = self.position

        dc.DrawCircle(x, y, DemoSelectorShape.SELECTION_ZONE)

        self._resetPenColor(dc)

    def inside(self, x: int, y: int) -> bool:
        """

        Args:
            x: x coordinate
            y: y coordinate

        Returns:          `True` if (x, y) is inside the shape.

        """
        ax, ay = self.position     # GetPosition always returns absolute position
        zone = self._selectZone
        return (ax - zone < x < ax + zone) and (ay - zone < y < ay + zone)

    def _setPenColor(self, dc: DC):
        pen: Pen = dc.GetPen()
        pen.SetColour(DemoColorEnum.toWxColor(DemoColorEnum.MEDIUM_SLATE_BLUE))
        dc.SetPen(pen)

    def _resetPenColor(self, dc: DC):
        pen: Pen = dc.GetPen()
        pen.SetColour(self._penSaveColor)
        dc.SetPen(pen)


DemoSelectorShapes = NewType('DemoSelectorShapes', List[DemoSelectorShape])
