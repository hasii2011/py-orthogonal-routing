
from logging import Logger
from logging import getLogger
from typing import cast

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.enumerations.Side import Side
from tests.demo.DemoEvents import ConnectionPositionChangedEvent

from tests.demo.DemoEvents import DemoEventType
from tests.demo.DemoEvents import EVT_CONNECTION_POSITION_CHANGED
from tests.demo.DemoEvents import EVT_SHAPE_MOVED
from tests.demo.DemoEvents import ShapeMovedEvent

from tests.demo.shapes.DemoShape import DemoShape

from tests.demo.IEventEngine import IEventEngine

from tests.demo.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter
from tests.demo.shapes.SelectorSide import SelectorSide


class DiagramChangedHandler:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._eventEngine:                IEventEngine               = cast(IEventEngine, None)
        self._orthogonalConnectorAdapter: OrthogonalConnectorAdapter = cast(OrthogonalConnectorAdapter, None)

    @property
    def eventEngine(self):
        raise AttributeError("Cannot access write-only attribute")

    @eventEngine.setter
    def eventEngine(self, eventEngine: IEventEngine):
        assert self._eventEngine is None, 'You should only set the event engine once'
        self._eventEngine = eventEngine

        self._eventEngine.registerListener(EVT_SHAPE_MOVED,                 self._onShapeMoved)
        self._eventEngine.registerListener(EVT_CONNECTION_POSITION_CHANGED, self._onConnectionPositionChanged)

    @property
    def orthogonalConnectorAdapter(self):
        raise AttributeError("Cannot access write-only attribute")

    @orthogonalConnectorAdapter.setter
    def orthogonalConnectorAdapter(self, value: OrthogonalConnectorAdapter):
        self._orthogonalConnectorAdapter = value

    def _onConnectionPositionChanged(self, event: ConnectionPositionChangedEvent):

        shape: DemoShape    = event.shape
        which: str          = event.which
        side:  SelectorSide = event.side

        self.logger.debug(f'Connection Changed - {shape=} {which=} {side=}')

        adapter: OrthogonalConnectorAdapter = self._orthogonalConnectorAdapter
        options: OrthogonalConnectorOptions = adapter.options

        sourceConnector:      ConnectorPoint = options.pointA
        destinationConnector: ConnectorPoint = options.pointB

        newRect:    Rect = self._shapeToRect(shape)
        engineSide: Side = Side(side.value)

        if which == 'source':
            sourceConnector.shape = newRect
            sourceConnector.side = engineSide
        elif which == 'destination':
            destinationConnector.shape = newRect
            destinationConnector.side = engineSide
        else:
            assert False, 'Hmm, developer error'

        adapter.runConnector(sourceConnectorPoint=sourceConnector, destinationConnectorPoint=destinationConnector, options=options)

        self._eventEngine.sendEvent(DemoEventType.REFRESH_FRAME)

    def _onShapeMoved(self, event: ShapeMovedEvent):

        shape: DemoShape = event.shape
        which: str       = event.which

        adapter: OrthogonalConnectorAdapter = self._orthogonalConnectorAdapter
        options: OrthogonalConnectorOptions = adapter.options

        self.logger.debug(f'{which=} {shape=}')

        sourceConnector:      ConnectorPoint = options.pointA
        destinationConnector: ConnectorPoint = options.pointB

        newRect: Rect = self._shapeToRect(shape)

        if which == 'source':
            sourceConnector.shape = newRect
        elif which == 'destination':
            destinationConnector.shape = newRect
        else:
            assert False, 'Hmm, developer error'

        adapter.runConnector(sourceConnectorPoint=sourceConnector, destinationConnectorPoint=destinationConnector, options=options)

        self._eventEngine.sendEvent(DemoEventType.REFRESH_FRAME)

    def _shapeToRect(self, shape: DemoShape) -> Rect:

        rect: Rect = Rect()

        rect.top    = shape.top
        rect.left   = shape.left
        rect.width  = shape.width
        rect.height = shape.height

        return rect
