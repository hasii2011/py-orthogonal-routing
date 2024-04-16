
from enum import Enum

from wx.lib.newevent import NewEvent

#
# The constructor returns a tuple; The first entry is the event,  The second is the binder
#
ShowRulersEvent,          EVT_SHOW_RULERS           = NewEvent()
ShowMainGridEvent,        EVT_SHOW_MAIN_GRID        = NewEvent()
ShowReferencePointsEvent, EVT_SHOW_REFERENCE_POINTS = NewEvent()
ShowRouteGridEvent,       EVT_SHOW_ROUTE_GRID       = NewEvent()


class DemoEventType(Enum):

    SHOW_RULERS           = 'ShowRulers'
    SHOW_MAIN_GRID        = 'ShowMainGrid'
    SHOW_REFERENCE_POINTS = 'ShowReferencePoints'
    SHOW_ROUTE_GRID       = 'ShowRouteGrid'

    SOURCE_CONNECTION_POSITION_CHANGED      = 'SourceConnectionPositionChanged'
    DESTINATION_CONNECTION_POSITION_CHANGED = 'DestinationConnectionPositionChanged'

    NOT_SET = 'Not Set'
