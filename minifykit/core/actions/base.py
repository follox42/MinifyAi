"""
Base class for minification actions.
"""

from abc import ABC, abstractmethod

class MinificationAction(ABC):
    """
    Abstract Action interface for a minification algorithm.
    
    Each Action implements a specific minification technique
    like comment removal, whitespace reduction, etc.
    """
    
    @abstractmethod
    def apply(self, code: str) -> str:
        """
        Apply the minification action to the given code.
        
        Args:
            code (str): The code to minify.
            
        Returns:
            str: The minified code.
        """
        pass
    
    @property
    def name(self) -> str:
        """
        Get the name of the action.
        
        Returns:
            str: The name of the action.
        """
        return self.__class__.__name__