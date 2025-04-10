"""
Base classes and implementations for language-specific minifiers.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..core.actions.base import MinificationAction
from ..core.actions.basic_actions import (
    CommentRemovalAction,
    WhitespaceReductionAction,
    EmptyLineRemovalAction,
    OperatorSpaceRemovalAction,
    CompositeMinificationAction
)


class LanguageMinifier(ABC):
    """
    Abstract base class for language-specific minifiers.
    
    Each language minifier implements minification strategies
    specific to a programming language.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the language.
        
        Returns:
            str: The name of the language.
        """
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """
        Get the file extensions supported by this minifier.
        
        Returns:
            List[str]: List of file extensions (with dot).
        """
        pass
    
    @abstractmethod
    def minify(self, code: str) -> str:
        """
        Minify the given code.
        
        Args:
            code (str): The code to minify.
                
        Returns:
            str: The minified code.
        """
        pass


class PythonMinifier(LanguageMinifier):
    """
    Minifier for Python code.
    """
    
    def __init__(self, preserve_newlines: bool = True, preserve_docstrings: bool = False):
        """
        Initialize the Python minifier.
        
        Args:
            preserve_newlines (bool): Whether to preserve newlines in the output.
            preserve_docstrings (bool): Whether to preserve docstrings.
        """
        self._preserve_newlines = preserve_newlines
        self._preserve_docstrings = preserve_docstrings
        self._action = self._create_action()
    
    @property
    def name(self) -> str:
        return "python"
    
    @property
    def file_extensions(self) -> List[str]:
        return [".py"]
    
    def _create_action(self) -> MinificationAction:
        """Create the minification action based on current settings."""
        actions = []
        
        # Add comment removal action
        if self._preserve_docstrings:
            # Only remove single-line comments, keep docstrings
            actions.append(CommentRemovalAction(single_line_pattern=r'#.*$'))
        else:
            # Remove all comments
            actions.append(CommentRemovalAction(
                single_line_pattern=r'#.*$',
                multi_line_pattern=r'""".*?"""|\'\'\'.*?\'\'\''
            ))
        
        # Add whitespace reduction action
        actions.append(WhitespaceReductionAction(preserve_newlines=self._preserve_newlines))
        
        # Add empty line removal action
        actions.append(EmptyLineRemovalAction())
        
        # If not preserving newlines, add operator space removal
        if not self._preserve_newlines:
            actions.append(OperatorSpaceRemovalAction())
        
        return CompositeMinificationAction(actions)
    
    def set_preserve_newlines(self, preserve: bool) -> None:
        """
        Set whether to preserve newlines.
        
        Args:
            preserve (bool): Whether to preserve newlines.
        """
        if self._preserve_newlines != preserve:
            self._preserve_newlines = preserve
            self._action = self._create_action()
    
    def set_preserve_docstrings(self, preserve: bool) -> None:
        """
        Set whether to preserve docstrings.
        
        Args:
            preserve (bool): Whether to preserve docstrings.
        """
        if self._preserve_docstrings != preserve:
            self._preserve_docstrings = preserve
            self._action = self._create_action()
    
    def minify(self, code: str) -> str:
        """
        Minify Python code.
        
        Args:
            code (str): The code to minify.
                
        Returns:
            str: The minified code.
        """
        return self._action.apply(code)


class JavaScriptMinifier(LanguageMinifier):
    """
    Minifier for JavaScript code.
    """
    
    def __init__(self, preserve_newlines: bool = True, aggressive: bool = False):
        """
        Initialize the JavaScript minifier.
        
        Args:
            preserve_newlines (bool): Whether to preserve newlines in the output.
            aggressive (bool): Whether to use aggressive minification.
        """
        self._preserve_newlines = preserve_newlines
        self._aggressive = aggressive
        self._action = self._create_action()
    
    @property
    def name(self) -> str:
        return "javascript"
    
    @property
    def file_extensions(self) -> List[str]:
        return [".js"]
    
    def _create_action(self) -> MinificationAction:
        """Create the minification action based on current settings."""
        actions = [
            # Remove comments
            CommentRemovalAction(
                single_line_pattern=r'//.*$',
                multi_line_pattern=r'/\*.*?\*/'
            ),
            
            # Reduce whitespace
            WhitespaceReductionAction(preserve_newlines=self._preserve_newlines),
            
            # Remove empty lines
            EmptyLineRemovalAction(),
        ]
        
        # Add operator space removal for aggressive mode
        if self._aggressive or not self._preserve_newlines:
            actions.append(OperatorSpaceRemovalAction())
        
        return CompositeMinificationAction(actions)
    
    def set_preserve_newlines(self, preserve: bool) -> None:
        """
        Set whether to preserve newlines.
        
        Args:
            preserve (bool): Whether to preserve newlines.
        """
        if self._preserve_newlines != preserve:
            self._preserve_newlines = preserve
            self._action = self._create_action()
    
    def set_aggressive(self, aggressive: bool) -> None:
        """
        Set whether to use aggressive minification.
        
        Args:
            aggressive (bool): Whether to use aggressive minification.
        """
        if self._aggressive != aggressive:
            self._aggressive = aggressive
            self._action = self._create_action()
    
    def minify(self, code: str) -> str:
        """
        Minify JavaScript code.
        
        Args:
            code (str): The code to minify.
                
        Returns:
            str: The minified code.
        """
        return self._action.apply(code)


class CSSMinifier(LanguageMinifier):
    """
    Minifier for CSS code.
    """
    
    def __init__(self):
        """Initialize the CSS minifier."""
        self._action = CompositeMinificationAction([
            CommentRemovalAction(multi_line_pattern=r'/\*.*?\*/'),
            WhitespaceReductionAction(preserve_newlines=False),
            EmptyLineRemovalAction(),
            OperatorSpaceRemovalAction()
        ])
    
    @property
    def name(self) -> str:
        return "css"
    
    @property
    def file_extensions(self) -> List[str]:
        return [".css"]
    
    def minify(self, code: str) -> str:
        """
        Minify CSS code.
        
        Args:
            code (str): The code to minify.
                
        Returns:
            str: The minified code.
        """
        return self._action.apply(code)


class HTMLMinifier(LanguageMinifier):
    """
    Minifier for HTML code.
    """
    
    def __init__(self, preserve_newlines: bool = True):
        """
        Initialize the HTML minifier.
        
        Args:
            preserve_newlines (bool): Whether to preserve newlines in the output.
        """
        self._preserve_newlines = preserve_newlines
        self._action = self._create_action()
    
    @property
    def name(self) -> str:
        return "html"
    
    @property
    def file_extensions(self) -> List[str]:
        return [".html", ".htm"]
    
    def _create_action(self) -> MinificationAction:
        """Create the minification action based on current settings."""
        return CompositeMinificationAction([
            CommentRemovalAction(multi_line_pattern=r'<!--.*?-->', single_line_pattern=r'\/*.*?\*/|//.*'),
            WhitespaceReductionAction(preserve_newlines=self._preserve_newlines),
            EmptyLineRemovalAction()
        ])
    
    def set_preserve_newlines(self, preserve: bool) -> None:
        """
        Set whether to preserve newlines.
        
        Args:
            preserve (bool): Whether to preserve newlines.
        """
        if self._preserve_newlines != preserve:
            self._preserve_newlines = preserve
            self._action = self._create_action()
    
    def minify(self, code: str) -> str:
        """
        Minify HTML code.
        
        Args:
            code (str): The code to minify.
                
        Returns:
            str: The minified code.
        """
        return self._action.apply(code)


# Create a custom minifier by combining actions
def create_custom_minifier(name: str, extensions: List[str], actions: List[MinificationAction]) -> LanguageMinifier:
    """
    Create a custom minifier with specific actions.
    
    Args:
        name (str): The name of the minifier.
        extensions (List[str]): List of file extensions this minifier supports.
        actions (List[MinificationAction]): List of actions to apply.
        
    Returns:
        LanguageMinifier: A custom minifier.
    """
    
    class CustomMinifier(LanguageMinifier):
        @property
        def name(self) -> str:
            return name
        
        @property
        def file_extensions(self) -> List[str]:
            return extensions
        
        def minify(self, code: str) -> str:
            action = CompositeMinificationAction(actions)
            return action.apply(code)
    
    return CustomMinifier()