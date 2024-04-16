
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import Bitmap
from wx import Brush
from wx import Colour
from wx import DC
from wx import EVT_PAINT
from wx import MemoryDC
from wx import PENSTYLE_LONG_DASH
from wx import PaintDC
from wx import PaintEvent
from wx import Pen
from wx import PenInfo
from wx import Rect

from wx import Window
# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from pyorthogonalrouting.Common import Integers
from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rectangle import Rectangle
from pyorthogonalrouting.Rectangle import Rectangles
from pyorthogonalrouting.Rect import Rect as OrthoRect
from tests.demo.BaseDiagramFrame import BaseDiagramFrame

from tests.demo.DemoColorEnum import DemoColorEnum

from tests.demo.DemoEvents import EVT_SHOW_REFERENCE_POINTS
from tests.demo.DemoEvents import EVT_SHOW_ROUTE_GRID
from tests.demo.DemoEvents import EVT_SHOW_RULERS
from tests.demo.DemoEvents import ShowReferencePointsEvent
from tests.demo.DemoEvents import ShowRouteGridEvent
from tests.demo.DemoEvents import ShowRulersEvent
from tests.demo.IEventEngine import IEventEngine

from tests.demo.DemoShape import DemoShape

from tests.demo.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter


REFERENCE_POINT_WIDTH:  int = 8
REFERENCE_POINT_HEIGHT: int = 8
REFERENCE_POINT_RADIUS: int = 4


class DemoDiagramFrame(BaseDiagramFrame):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._orthogonalConnectorAdapter: OrthogonalConnectorAdapter = cast(OrthogonalConnectorAdapter, None)
        self._eventEngine:                IEventEngine               = cast(IEventEngine, None)

        self._showReferencePoints: bool = False
        self._showRouteGrid:       bool = False
        self._showRulers:          bool = False

        self.Bind(EVT_PAINT, self.onPaint)

    @property
    def eventEngine(self):
        return

    @eventEngine.setter
    def eventEngine(self, eventEngine: IEventEngine):

        assert self._eventEngine is None, 'You should only set the event engine once'

        self._eventEngine = eventEngine
        self._eventEngine.registerListener(EVT_SHOW_REFERENCE_POINTS, self._onShowReferencePointsToggled)
        self._eventEngine.registerListener(EVT_SHOW_ROUTE_GRID,       self._onShowRouteGridToggled)
        self._eventEngine.registerListener(EVT_SHOW_RULERS,           self._onShowRulersToggled)

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

        # self._drawGrid(memDC=mem, width=w, height=h, startX=x, startY=y)

        if self._orthogonalConnectorAdapter is not None:

            if self._showRouteGrid is True:
                self._drawRouteGrid(dc=mem)
            if self._showReferencePoints is True:
                self._drawReferencePoints(dc=mem)
            if self._showRulers is True:
                self._drawRulers(dc=mem)

            self._drawShapes(dc=mem)
            self._drawPath(dc=mem)

        dc.Blit(0, 0, w, h, mem, x, y)

    def _onShowReferencePointsToggled(self, event: ShowReferencePointsEvent):

        self._showReferencePoints = event.showReferencePoints
        self.logger.debug(f'{self._showReferencePoints=}')
        self.Refresh()

    def _onShowRouteGridToggled(self, event: ShowRouteGridEvent):

        self._showRouteGrid = event.showRouteGrid
        self.Refresh()

    def _onShowRulersToggled(self, event: ShowRulersEvent):

        self._showRulers = event.showRulers
        self.Refresh()

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

    def _getRulerPen(self) -> Pen:
        gridLineColor: Colour = DemoColorEnum.toWxColor(DemoColorEnum.VIOLET_RED)

        gridLineStyle: PenStyle = PENSTYLE_LONG_DASH
        pen: Pen = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen

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

        x:      int = demoShape.left
        y:      int = demoShape.top
        width:  int = demoShape.width
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

            tuplePair = pt1.x, pt1.y, pt2.x, pt2.y
            tupleSequence.append(tuplePair)

        dc.DrawLineList(tupleSequence, BLACK_PEN)

    def _drawReferencePoints(self, dc: MemoryDC):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(BLACK_PEN)
        dc.SetBrush(Brush(DemoColorEnum.toWxColor(DemoColorEnum.ALICE_BLUE)))

        points: Points = self._orthogonalConnectorAdapter.spots

        for pt in points:
            # point: Point = self._computeShapeCenter(x=pt.x, y=pt.y, width=REFERENCE_POINT_WIDTH, height=REFERENCE_POINT_HEIGHT)
            # dc.DrawEllipse(x=point.x, y=point.y, width=REFERENCE_POINT_WIDTH, height=REFERENCE_POINT_HEIGHT)
            point: Point = cast(Point, pt)
            dc.DrawCircle(x=point.x, y=point.y, radius=REFERENCE_POINT_RADIUS)
        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def _drawRouteGrid(self, dc: MemoryDC):
        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(self._getGridPen())
        rectangles: Rectangles = self._orthogonalConnectorAdapter.routeGrid
        for r in rectangles:
            rectangle: Rectangle = cast(Rectangle, r)

            x:      int = rectangle.left
            y:      int = rectangle.top
            width:  int = rectangle.width
            height: int = rectangle.height

            dc.DrawRectangle(x=x, y=y, width=width, height=height)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def _drawRulers(self, dc: MemoryDC):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(self._getRulerPen())

        horizontalRulers: Integers  = self._orthogonalConnectorAdapter.hRulers
        verticalRulers:   Integers  = self._orthogonalConnectorAdapter.vRulers
        globalBounds:     OrthoRect = self._orthogonalConnectorAdapter.globalBounds()

        for y in horizontalRulers:
            dc.DrawLine(x1=0, y1=y, x2=globalBounds.width, y2=y)

        for x in verticalRulers:
            self.logger.info(f'{x=}')
            dc.DrawLine(x1=x, y1=0, x2=x, y2=globalBounds.height)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)
