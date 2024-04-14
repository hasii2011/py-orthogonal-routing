
from typing import cast

from logging import Logger
from logging import getLogger

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnector import OrthogonalConnector
from pyorthogonalrouting.OrthogonalConnectorByProduct import OrthogonalConnectorByProducts
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rect import Rect

from pyorthogonalrouting.enumerations.Side import Side
from tests.demo.DemoShape import DemoShape


class OrthogonalConnectorAdapter:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._sourceRect:      Rect = cast(Rect, None)
        self._destinationRect: Rect = cast(Rect, None)

        self._byProducts: OrthogonalConnectorByProducts = cast(OrthogonalConnectorByProducts, None)
        self._path:       Points                        = cast(Points, None)

    @property
    def sourceShape(self) -> DemoShape:

        return DemoShape(left=self._sourceRect.left, top=self._sourceRect.top,
                         width=self._sourceRect.width, height=self._sourceRect.height)

    @property
    def destinationShape(self) -> DemoShape:

        return DemoShape(left=self._destinationRect.left, top=self._destinationRect.top,
                         width=self._destinationRect.width, height=self._destinationRect.height)

    @property
    def path(self) -> Points:
        return self._path

    def runDefaultDemo(self):

        self._sourceRect      = Rect(left=50,  top=50,  width=100, height=100)
        self._destinationRect = Rect(left=200, top=200, width=50,  height=100)

        options: OrthogonalConnectorOptions = OrthogonalConnectorOptions()

        options.pointA = ConnectorPoint(shape=self._sourceRect, side=Side.BOTTOM, distance=0.5)
        options.pointB = ConnectorPoint(shape=self._destinationRect, side=Side.RIGHT,  distance=0.5)
        options.shapeMargin        = 10
        options.globalBoundsMargin = 10
        options.globalBounds       = Rect(left=0, top=0, width=500, height=500)

        self._path = OrthogonalConnector.route(options=options)