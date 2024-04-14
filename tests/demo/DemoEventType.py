
from enum import Enum


class DemoEventType(Enum):

    SHOW_RULERS           = 'ShowRulers'
    SHOW_MAIN_GRID        = 'ShowMainGrid'
    SHOW_REFERENCE_POINTS = 'ShowReferencePoints'
    SHOW_ROUTE_GRID       = 'ShowRouteGrid'

    SOURCE_CONNECTION_POSITION_CHANGED      = 'SourceConnectionPositionChanged'
    DESTINATION_CONNECTION_POSITION_CHANGED = 'DestinationConnectionPositionChanged'

    NOT_SET = 'Not Set'
