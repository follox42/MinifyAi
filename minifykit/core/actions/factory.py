from typing import Dict, Optional, Any
import re
from .base import MinificationAction
from .basic_actions import (
    CommentRemovalAction,
    WhitespaceReductionAction, 
    EmptyLineRemovalAction,
    OperatorSpaceRemovalAction,
    LineJoiningAction
)

def create_action(action_type: str, name: Optional[str] = None, **kwargs) -> MinificationAction:
    """
    Factory function to create a minification action based on the type.
    
    Args:
        action_type (str): The type of action to create.
        name (Optional[str]): Custom name for the action.
        **kwargs: Additional keyword arguments to pass to the action constructor.
        
    Returns:
        MinificationAction: The created minification action.
        
    Raises:
        ValueError: If the action type is not recognized.
    """
    # Dictionary mapping action types to their classes
    action_classes: Dict[str, type] = {
        "whitespace": WhitespaceReductionAction,
        "comments": CommentRemovalAction,
        "empty_lines": EmptyLineRemovalAction,
        "operators": OperatorSpaceRemovalAction,
        "line_joining": LineJoiningAction,
    }
    
    # Check if the action type exists
    if action_type not in action_classes:
        raise ValueError(f"Unknown action type: {action_type}")
    
    # Create the action with the provided parameters
    action_class = action_classes[action_type]
    action = action_class(**kwargs)
    
    # If a custom name is provided, create a wrapper to override the name
    if name:
        class NamedAction(MinificationAction):
            def apply(self, code: str) -> str:
                return action.apply(code)
            
            @property
            def name(self) -> str:
                return name
        
        return NamedAction()
    
    return action