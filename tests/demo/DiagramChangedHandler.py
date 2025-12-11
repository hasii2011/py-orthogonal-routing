
from typing import cast

from logging import Logger
from logging import getLogger

from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.enumerations.Side import Side
from tests.demo.pubsubengine.IOrthoPubSubEngine import IOrthoPubSubEngine
from tests.demo.pubsubengine.OrthoMessageType import OrthoMessageType

from tests.demo.shapes.DemoShape import DemoShape


from tests.demo.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter
from tests.demo.shapes.SelectorSide import SelectorSide


class DiagramChangedHandler:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._pubSub:                     IOrthoPubSubEngine         = cast(IOrthoPubSubEngine, None)
        self._orthogonalConnectorAdapter: OrthogonalConnectorAdapter = cast(OrthogonalConnectorAdapter, None)

    @property
    def pubSubEngine(self):
        raise AttributeError("Cannot access write-only attribute")

    @pubSubEngine.setter
    def pubSubEngine(self, pubSubEngine: IOrthoPubSubEngine):
        assert self._pubSub is None, 'You should only set the pub sub engine once'
        self._pubSub = pubSubEngine

        self._pubSub.subscribe(OrthoMessageType.SHAPED_MOVED,                self._onShapeMoved)
        self._pubSub.subscribe(OrthoMessageType.CONNECTION_SIDE_CHANGED,     self._onConnectionSideChanged)
        self._pubSub.subscribe(OrthoMessageType.CONNECTION_POSITION_CHANGED, self._onConnectionPositionChanged)

    @property
    def orthogonalConnectorAdapter(self):
        raise AttributeError("Cannot access write-only attribute")

    @orthogonalConnectorAdapter.setter
    def orthogonalConnectorAdapter(self, value: OrthogonalConnectorAdapter):
        self._orthogonalConnectorAdapter = value

    def _onConnectionSideChanged(self, shape: DemoShape, which: str, side: SelectorSide):

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

        self._pubSub.sendMessage(OrthoMessageType.REFRESH_FRAME)

    def _onConnectionPositionChanged(self, shapeName: str, position: float):

        # shapeName: str   = event.shapeName
        # position:  float = event.position

        self.logger.info(f'{shapeName=} {position=}')

        adapter: OrthogonalConnectorAdapter = self._orthogonalConnectorAdapter
        options: OrthogonalConnectorOptions = adapter.options

        sourceConnector:      ConnectorPoint = options.pointA
        destinationConnector: ConnectorPoint = options.pointB

        if shapeName == 'Source':
            sourceConnector.distance = position
        elif shapeName == 'Destination':
            destinationConnector.distance = position
        else:
            assert False, 'Must be one or the other'

        adapter.runConnector(sourceConnectorPoint=sourceConnector, destinationConnectorPoint=destinationConnector, options=options)

        self._pubSub.sendMessage(OrthoMessageType.REFRESH_FRAME)

    def _onShapeMoved(self, shape: DemoShape, which: str):

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

        self._pubSub.sendMessage(OrthoMessageType.REFRESH_FRAME)

    def _shapeToRect(self, shape: DemoShape) -> Rect:

        rect: Rect = Rect()

        rect.top    = shape.top
        rect.left   = shape.left
        rect.width  = shape.width
        rect.height = shape.height

        return rect
