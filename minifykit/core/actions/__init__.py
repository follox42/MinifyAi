"""
Actions module - Contains individual minification actions.
"""

from .base import MinificationAction
from .basic_actions import (
    CommentRemovalAction,
    WhitespaceReductionAction, 
    EmptyLineRemovalAction,
    OperatorSpaceRemovalAction,
    LineJoiningAction,
    CompositeMinificationAction
)
from .factory import create_action