
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import BLACK_PEN
from wx import Bitmap
from wx import Brush
from wx import Colour
from wx import DC
from wx import EVT_LEFT_DOWN
from wx import EVT_LEFT_UP
from wx import EVT_MOTION
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import FONTWEIGHT_NORMAL
from wx import Font
from wx import LIGHT_GREY
from wx import MouseEvent
from wx import PENSTYLE_DOT
from wx import Pen
from wx import PenInfo
from wx import Point
from wx import ScrolledWindow
from wx import WHITE
from wx import WHITE_BRUSH
from wx import Window
# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from tests.demo.shapes.BaseShape import BaseShape
from tests.demo.shapes.BaseShape import BaseShapes
from tests.demo.shapes.DemoSelectorShape import DemoSelectorShape
from tests.demo.shapes.DemoShape import DemoShape
from tests.demo.shapes.RectangleShape import RectangleShape
from tests.demo.shapes.SelectorSide import SelectorSide

DEFAULT_WIDTH = 6000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20


DEFAULT_PEN:       Pen   = BLACK_PEN
DEFAULT_BRUSH:     Brush = WHITE_BRUSH
DEFAULT_FONT_SIZE: int = 10

NO_SHAPE: RectangleShape = cast(RectangleShape, None)

MousePosition = NewType('MousePosition', Tuple[int, int])

NO_MOUSE_POSITION = cast(MousePosition, None)


class BaseDiagramFrame(ScrolledWindow):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self._baseLogger: Logger = getLogger(__name__)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        self._setupScrollBars()

        # paint related
        w, h = self.GetSize()
        self._workingBitmap    = Bitmap(w, h)   # double buffering
        self._backgroundBitmap = Bitmap(w, h)

        self.SetBackgroundColour(WHITE)

        self._stroke: Pen   = DEFAULT_PEN
        self._fill:   Brush = DEFAULT_BRUSH

        self._textColor:   Colour = BLACK
        self._defaultFont: Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self._nameFont:    Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)

        self._shapes:           BaseShapes     = BaseShapes([])
        self._lastMousePosition: MousePosition = NO_MOUSE_POSITION

        self.Bind(EVT_LEFT_DOWN, self._onLeftDown)
        self.Bind(EVT_LEFT_UP,   self._onLeftUp)

    # noinspection PyUnusedLocal
    def _shapedMoved(self, shape: BaseShape):
        """
        Superclass needs to implement this;

        Args:
            shape:
        """
        assert False, 'The superclass needs to implement this'

    def _sideSelected(self, shape: BaseShape, side: SelectorSide):
        """
        Superclass needs to implement this;

        Args:
            shape:
            side:
        """
        assert False, 'The superclass needs to implement this'

    def _eventDelegator(self, event: MouseEvent, methodName: str) -> BaseShape:
        """
        This handler finds the shape at the event coordinates and dispatches the event.
        The handler will receive an event with coordinates already scrolled.

        Args:
            event:      The original event
            methodName: Name of the method to invoke in the event handler of the shape

        Returns:  The clicked shape
        """
        x, y = self._getEventPosition(event)

        shape: BaseShape = self._findShape(x, y)

        # event.m_x, event.m_y = x, y

        if shape is not None and isinstance(shape, BaseShape):
            self._baseLogger.debug(f'_eventDelegator - `{shape=}` `{methodName=}` x,y: {x},{y}')
            getattr(shape, methodName)(event)
        else:
            event.Skip()

        return shape

    def _onLeftDown(self, event: MouseEvent):

        shape: BaseShape = self._eventDelegator(event, "onLeftDown")
        # # clicked on Canvas; clear selections
        if shape is None:
            self._deselectAll()
        elif isinstance(shape, DemoShape):
            self._deselectAll()
            shape.selected = True
            if not event.GetSkipped():
                self._baseLogger.info(f'{event.GetSkipped()=}')
                return
            # Manage click and drag
            x, y = event.GetX(), event.GetY()
            self._lastMousePosition = MousePosition((x, y))
            self.Bind(EVT_MOTION, self._onDrag)
        elif isinstance(shape, DemoSelectorShape):
            selectorShape: DemoSelectorShape = cast(DemoSelectorShape, shape)
            self._baseLogger.debug(f'{selectorShape=}')
            self._sideSelected(shape=selectorShape.parent, side=selectorShape.side)

        self.Refresh()

    def _onLeftUp(self, event: MouseEvent):

        shape: BaseShape = self._eventDelegator(event, "onLeftUp")
        self._baseLogger.debug(f'LeftUp - {shape}')
        if shape is not None and isinstance(shape, DemoShape):
            self._shapedMoved(shape)

        self._moving = False
        self._lastMousePosition = NO_MOUSE_POSITION
        self.Unbind(EVT_MOTION)

    def _onMove(self, event: MouseEvent):
        event.m_x, event.m_y = self._getEventPosition(event)
        self._onDrag(event)

    def _onDrag(self, event: MouseEvent):
        """
        Callback to drag the selected shapes.

        Args:
            event:
        """
        from tests.demo.shapes.DemoShape import DemoShape

        x, y = event.GetX(), event.GetY()

        self._baseLogger.debug(f'({x},{y})')

        for s in self._shapes:

            if isinstance(s, DemoShape):
                shape: DemoShape = cast(DemoShape, s)
                if shape.selected is True:
                    ox, oy = self._lastMousePosition    # old position
                    dx, dy = x - ox, y - oy             # delta from current
                    # sx, sy = shape.GetPosition()
                    sx, sy = shape.position

                    newX: int = sx + dx
                    newY: int = sy + dy
                    self._baseLogger.debug(f'New drag position {shape.identifier=} ({newX},{newY})')
                    shape.position = newX, newY
                    self._lastMousePosition = MousePosition((x, y))

        self.Refresh(False)

        self._clickedShape = cast(RectangleShape, None)

    def _drawGrid(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        # self.clsLogger.info(f'{width=} {height=} {startX=} {startY=}')
        savePen = memDC.GetPen()

        newPen: Pen = self._getGridPen()
        memDC.SetPen(newPen)

        self._drawHorizontalLines(memDC=memDC, width=width, height=height, startX=startX, startY=startY)
        self._drawVerticalLines(memDC=memDC,   width=width, height=height, startX=startX, startY=startY)
        memDC.SetPen(savePen)

    def _drawHorizontalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        x1:   int = 0
        x2:   int = startX + width
        stop: int = height + startY
        step: int = 25
        for movingY in range(startY, stop, step):
            memDC.DrawLine(x1, movingY, x2, movingY)

    def _drawVerticalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        y1:   int = 0
        y2:   int = startY + height
        stop: int = width + startX
        step: int = 25

        for movingX in range(startX, stop, step):
            memDC.DrawLine(movingX, y1, movingX, y2)

    def _getGridPen(self) -> Pen:

        gridLineColor: Colour   = LIGHT_GREY
        gridLineStyle: PenStyle = PENSTYLE_DOT
        pen:           Pen      = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen

    def _textWidth(self, dc: DC, text: str):
        width = dc.GetTextExtent(text)[0]
        return width

    def _textHeight(self, dc: DC, text: str):
        height = dc.GetTextExtent(text)[1]
        return height

    def _computeShapeCenter(self, x: int, y: int, width: int, height: int) -> Point:

        centeredPoint: Point = Point(x=x - (width // 2), y=y - (height // 2))

        return centeredPoint

    def _getEventPosition(self, event: MouseEvent):
        """
        Return the position of a click in the diagram.
        Args:
            event:   The mouse event

        Returns: A tuple with x,y coordinates
        """
        x, y = self._convertEventCoordinates(event)
        return x, y

    def _convertEventCoordinates(self, event):

        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return event.GetX() + (xView * xDelta), event.GetY() + (yView * yDelta)

    def _findShape(self, x: int, y: int) -> BaseShape:
        """
        Return the shape at (x, y).

        Args:
            x: coordinate
            y: coordinate

        Returns:  The shape that was found under the coordinates or None
        """
        self._baseLogger.debug(f'FindShape: @{x},{y}')
        found:  BaseShape  = cast(BaseShape, None)
        shapes: BaseShapes = self._shapes

        shapes.reverse()    # to select the one at the top

        for shape in shapes:
            if shape.inside(x, y):
                self._baseLogger.debug(f"Inside: {shape}")
                found = shape
                break   # only select the first one

        shapes.reverse()    # Put them back

        return found

    def _deselectAll(self):

        for s in self._shapes:
            if isinstance(s, RectangleShape):
                cast(RectangleShape, s).selected = False

    def _setupScrollBars(self):

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0

        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)
