
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import PostEvent
from wx import PyEventBinder
from wx import Window

from tests.demo.DemoEvents import ConnectionPositionChangedEvent
from tests.demo.DemoEvents import DemoEventType
from tests.demo.DemoEvents import RefreshFrameEvent
from tests.demo.DemoEvents import ShapeMovedEvent
from tests.demo.DemoEvents import ShowReferencePointsEvent
from tests.demo.DemoEvents import ShowRouteGridEvent
from tests.demo.DemoEvents import ShowRulersEvent

from tests.demo.shapes.DemoShape import DemoShape
from tests.demo.IEventEngine import IEventEngine
from tests.demo.shapes.SelectorSide import SelectorSide


class InvalidKeywordException(Exception):
    pass


SHOW_REFERENCE_POINTS_PARAMETER: str = 'showReferencePoints'
SHOW_ROUTE_GRID_PARAMETER:       str = 'showRouteGrid'
SHOW_RULERS_PARAMETER:           str = 'showRulers'
SHAPE_PARAMETER:                 str = 'shape'
WHICH_PARAMETER:                 str = 'which'
SIDE_PARAMETER:                  str = 'side'


class DemoEventEngine(IEventEngine):

    def __init__(self, listeningWindow: Window):

        self.logger:           Logger = getLogger(__name__)
        self._listeningWindow: Window = listeningWindow

    def registerListener(self, event: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(event, callback)

    def sendEvent(self, eventType: DemoEventType, **kwargs):

        try:
            match eventType:
                case DemoEventType.SHOW_REFERENCE_POINTS:
                    self._sendShowReferencePointsEvent(**kwargs)
                case DemoEventType.SHOW_ROUTE_GRID:
                    self._sendShowRouteGridEvent(**kwargs)
                case DemoEventType.SHOW_RULERS:
                    self._sendShowRulersEvent(**kwargs)
                case DemoEventType.SHAPED_MOVED:
                    self._sendShapeMovedEvent(**kwargs)
                case DemoEventType.CONNECTION_POSITION_CHANGED:
                    self._sendConnectionPositionChangedEvent(**kwargs)
                case DemoEventType.REFRESH_FRAME:
                    self._sendRefreshFrameEvent(**kwargs)
                case _:
                    self.logger.warning(f'Unknown Ogl Event Type: {eventType}')
        except KeyError as ke:
            eMsg: str = f'Invalid keyword parameter. `{ke}`'
            raise InvalidKeywordException(eMsg)

    def _sendShowReferencePointsEvent(self, **kwargs):

        show: bool = kwargs[SHOW_REFERENCE_POINTS_PARAMETER]
        showReferencePointsEvent: ShowReferencePointsEvent = ShowReferencePointsEvent(showReferencePoints=show)
        PostEvent(dest=self._listeningWindow, event=showReferencePointsEvent)

    def _sendShowRouteGridEvent(self, **kwargs):

        show:  bool               = kwargs[SHOW_ROUTE_GRID_PARAMETER]
        event: ShowRouteGridEvent = ShowRouteGridEvent(showRouteGrid=show)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendShowRulersEvent(self, **kwargs):

        show:  bool            = kwargs[SHOW_RULERS_PARAMETER]
        event: ShowRulersEvent = ShowRulersEvent(showRulers=show)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendShapeMovedEvent(self, **kwargs):

        shape: DemoShape       = kwargs[SHAPE_PARAMETER]
        which: str             = kwargs[WHICH_PARAMETER]

        event: ShapeMovedEvent = ShapeMovedEvent(shape=shape, which=which)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendConnectionPositionChangedEvent(self, **kwargs):

        shape: DemoShape    = kwargs[SHAPE_PARAMETER]
        side:  SelectorSide = kwargs[SIDE_PARAMETER]
        which: str          = kwargs[WHICH_PARAMETER]

        event: ConnectionPositionChangedEvent = ConnectionPositionChangedEvent(shape=shape, which=which, side=side)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendRefreshFrameEvent(self, **kwargs):

        event: RefreshFrameEvent = RefreshFrameEvent()
        PostEvent(dest=self._listeningWindow, event=event)
