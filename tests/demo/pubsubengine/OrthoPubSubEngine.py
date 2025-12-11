
from typing import Callable

from logging import Logger
from logging import getLogger

from codeallybasic.BasePubSubEngine import BasePubSubEngine
from codeallybasic.BasePubSubEngine import Topic

from tests.demo.pubsubengine.IOrthoPubSubEngine import IOrthoPubSubEngine
from tests.demo.pubsubengine.OrthoMessageType import OrthoMessageType


class OrthoPubSubEngine(IOrthoPubSubEngine, BasePubSubEngine):

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def subscribe(self, messageType: OrthoMessageType, listener: Callable):
        self._subscribe(topic=Topic(messageType.value), listener=listener)

    def sendMessage(self, messageType: OrthoMessageType, **kwargs):
        self._sendMessage(topic=Topic(messageType.value), **kwargs)
