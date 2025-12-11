
from abc import ABC
from abc import abstractmethod
from typing import Callable

from tests.demo.pubsubengine.OrthoMessageType import OrthoMessageType


class IOrthoPubSubEngine(ABC):

    """
    Implement an interface using the standard Python library.  I found zope too abstract
    and python interface could not handle subclasses;
    We will register a topic on a eventType.frameId.DiagramName
    """
    @abstractmethod
    def subscribe(self, messageType: OrthoMessageType, listener: Callable):
        pass

    @abstractmethod
    def sendMessage(self, messageType: OrthoMessageType, **kwargs):
        pass
