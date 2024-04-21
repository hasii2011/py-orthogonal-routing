
from typing import cast

from logging import Logger
from logging import getLogger

from pyorthogonalrouting.Common import Integers
from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnector import OrthogonalConnector
from pyorthogonalrouting.OrthogonalConnectorByProduct import OrthogonalConnectorByProduct
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions

from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.Rectangle import Rectangles

from pyorthogonalrouting.enumerations.Side import Side

from tests.demo.shapes.DemoShape import DemoShape


class OrthogonalConnectorAdapter:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._sourceRect:      Rect = cast(Rect, None)
        self._destinationRect: Rect = cast(Rect, None)

        self._byProducts:   OrthogonalConnectorByProduct = cast(OrthogonalConnectorByProduct, None)
        self._path:         Points                       = cast(Points, None)

        self._options:          OrthogonalConnectorOptions = cast(OrthogonalConnectorOptions, None)
        self._sourceShape:      DemoShape                  = cast(DemoShape, None)
        self._destinationShape: DemoShape                  = cast(DemoShape, None)

    @property
    def sourceShape(self) -> DemoShape:

        return self._sourceShape

    @property
    def destinationShape(self) -> DemoShape:
        return self._destinationShape

    @property
    def path(self) -> Points:
        return self._path

    @property
    def spots(self) -> Points:
        return self._byProducts.spots

    @property
    def routeGrid(self) -> Rectangles:
        return self._byProducts.grid

    @property
    def hRulers(self) -> Integers:
        return self._byProducts.hRulers

    @property
    def vRulers(self) -> Integers:
        return self._byProducts.vRulers

    @property
    def globalBounds(self) -> Rect:
        return self._options.globalBounds

    @property
    def options(self) -> OrthogonalConnectorOptions:
        return self._options

    def runDefaultDemo(self):

        self._sourceRect      = Rect(left=50,  top=50,  width=100, height=100)
        self._destinationRect = Rect(left=200, top=200, width=50,  height=100)

        self._sourceShape = DemoShape(left=self._sourceRect.left, top=self._sourceRect.top,
                                      width=self._sourceRect.width, height=self._sourceRect.height)

        self._destinationShape = DemoShape(left=self._destinationRect.left, top=self._destinationRect.top,
                                           width=self._destinationRect.width, height=self._destinationRect.height)

        options: OrthogonalConnectorOptions = OrthogonalConnectorOptions()

        options.shapeMargin        = 20
        options.globalBoundsMargin = 50
        options.globalBounds       = Rect(left=0, top=0, width=500, height=500)

        self.runConnector(options=options,
                          sourceConnectorPoint=ConnectorPoint(shape=self._sourceRect, side=Side.BOTTOM, distance=0.5),
                          destinationConnectorPoint=ConnectorPoint(shape=self._destinationRect, side=Side.BOTTOM,  distance=0.5)
                          )

    def runConnector(self, sourceConnectorPoint: ConnectorPoint, destinationConnectorPoint: ConnectorPoint, options: OrthogonalConnectorOptions):

        options.pointA = sourceConnectorPoint
        options.pointB = destinationConnectorPoint

        self._options = options
        self._path    = OrthogonalConnector.route(options=options)

        self._byProducts = OrthogonalConnector.byProduct
