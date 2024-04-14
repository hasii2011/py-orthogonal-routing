
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import PyEventBinder

from tests.demo.DemoEventType import DemoEventType
from tests.demo.IEventEngine import IEventEngine


class DemoEventEngine(IEventEngine):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def sendEvent(self, eventType: DemoEventType, **kwargs):
        pass

    def registerListener(self, event: PyEventBinder, callback: Callable):
        pass
