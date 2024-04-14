
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import BLACK_PEN
from wx import Bitmap
from wx import Brush
from wx import Colour
from wx import DC
from wx import EVT_PAINT
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import FONTWEIGHT_NORMAL
from wx import Font
from wx import LIGHT_GREY
from wx import MemoryDC
from wx import PENSTYLE_DOT
from wx import PaintDC
from wx import PaintEvent
from wx import Pen
from wx import PenInfo
from wx import Rect
from wx import ScrolledWindow
from wx import WHITE
from wx import WHITE_BRUSH
from wx import Window
# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from pyorthogonalrouting.Point import Points
from tests.demo.DemoColorEnum import DemoColorEnum
from tests.demo.DemoShape import DemoShape
from tests.demo.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter

DEFAULT_WIDTH = 6000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20


DEFAULT_PEN:       Pen   = BLACK_PEN
DEFAULT_BRUSH:     Brush = WHITE_BRUSH
DEFAULT_FONT_SIZE: int = 10


class DemoDiagramFrame(ScrolledWindow):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

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

        self._orthogonalConnectorAdapter: OrthogonalConnectorAdapter = cast(OrthogonalConnectorAdapter, None)
        self.Bind(EVT_PAINT, self.onPaint)

    @property
    def orthogonalConnectorAdapter(self) -> OrthogonalConnectorAdapter:
        return self._orthogonalConnectorAdapter

    @orthogonalConnectorAdapter.setter
    def orthogonalConnectorAdapter(self, newValue: OrthogonalConnectorAdapter):
        self._orthogonalConnectorAdapter = newValue

    # noinspection PyUnusedLocal
    def Refresh(self, eraseBackground: bool = True, rect: Rect = None):
        self.onPaint(cast(PaintEvent, None))

    # noinspection PyUnusedLocal
    def onPaint(self, event: PaintEvent):

        dc: PaintDC = PaintDC(self)

        w, h = self.GetSize()

        mem: MemoryDC = self.createDC(w, h)
        mem.SetBackground(Brush(self.GetBackgroundColour()))
        mem.Clear()

        x, y = self.CalcUnscrolledPosition(0, 0)

        self._drawGrid(memDC=mem, width=w, height=h, startX=x, startY=y)

        if self._orthogonalConnectorAdapter is not None:
            self._drawShapes(dc=mem)
            self._drawPath(dc=mem)

        dc.Blit(0, 0, w, h, mem, x, y)

    def createDC(self, w: int, h: int) -> MemoryDC:
        """
        Create a DC,
        Args:
            w:  frame width
            h:  frame height

        Returns: A device context
        """
        dc: MemoryDC = MemoryDC()

        bm = self._workingBitmap
        # cache the bitmap, to avoid creating a new one at each refresh.
        # only recreate it if the size of the window has changed
        if (bm.GetWidth(), bm.GetHeight()) != (w, h):
            bm = self._workingBitmap = Bitmap(w, h)
        dc.SelectObject(bm)

        dc.SetBackground(Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.PrepareDC(dc)

        return dc

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

        pen:           Pen    = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen

    def _textWidth(self, dc: DC, text: str):
        width = dc.GetTextExtent(text)[0]
        return width

    def _textHeight(self, dc: DC, text: str):
        height = dc.GetTextExtent(text)[1]
        return height

    def _drawShapes(self, dc: MemoryDC):
        """

        Args:
            dc:  Make sure this is a memory DC
        """

        sourceShape:      DemoShape = self._orthogonalConnectorAdapter.sourceShape
        destinationShape: DemoShape = self._orthogonalConnectorAdapter.destinationShape

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetBrush(Brush(DemoColorEnum.toWxColor(DemoColorEnum.ALICE_BLUE)))

        self._drawShape(dc, sourceShape)
        self._drawShape(dc, destinationShape)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def _drawShape(self, dc: MemoryDC, demoShape: DemoShape):

        x: int = demoShape.left
        y: int = demoShape.top
        width: int = demoShape.width
        height: int = demoShape.height

        dc.DrawRoundedRectangle(x=x, y=y, width=width, height=height, radius=8.0)

    def _drawPath(self, dc: MemoryDC):

        points: Points = self._orthogonalConnectorAdapter.path

        tupleSequence = []
        for x in range(len(points)):
            currentIdx = x
            nextIdx    = currentIdx + 1
            if nextIdx > len(points) - 1:
                break
            pt1 = points[currentIdx]
            pt2 = points[nextIdx]

            tuplePair = pt1.x, pt1.y,pt2.x, pt2.y
            tupleSequence.append(tuplePair)

        dc.DrawLineList(tupleSequence, BLACK_PEN)

    # def _computeShapeCenter(self, node: Node) -> Point:
    #
    #     centeredPoint: Point = Point(x=node.location.x + (node.size.width // 2), y=node.location.y + (node.size.height // 2))
    #
    #     return centeredPoint
