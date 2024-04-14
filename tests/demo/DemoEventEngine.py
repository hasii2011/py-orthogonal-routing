
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import PostEvent
from wx import PyEventBinder
from wx import Window

from tests.demo.DemoEvents import DemoEventType
from tests.demo.DemoEvents import ShowReferencePointsEvent
from tests.demo.IEventEngine import IEventEngine


class InvalidKeywordException(Exception):
    pass


SHOW_REFERENCE_POINTS_PARAMETER: str = 'showReferencePoints'


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
                case _:
                    self.logger.warning(f'Unknown Ogl Event Type: {eventType}')
        except KeyError as ke:
            eMsg: str = f'Invalid keyword parameter. `{ke}`'
            raise InvalidKeywordException(eMsg)

    def _sendShowReferencePointsEvent(self, **kwargs):

        show: bool = kwargs[SHOW_REFERENCE_POINTS_PARAMETER]

        selectedEvent: ShowReferencePointsEvent = ShowReferencePointsEvent(showReferencePoints=show)

        PostEvent(dest=self._listeningWindow, event=selectedEvent)
