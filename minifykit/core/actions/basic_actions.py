from typing import List, Optional
import re
from .base import MinificationAction

class CommentRemovalAction(MinificationAction):
    """Action for removing comments from code."""
    
    def __init__(self, single_line_pattern: Optional[str] = None, 
                multi_line_pattern: Optional[str] = None):
        """
        Initialize the comment removal action.
        
        Args:
            single_line_pattern (Optional[str]): Regular expression pattern for single-line comments.
            multi_line_pattern (Optional[str]): Regular expression pattern for multi-line comments.
        """
        self.single_line_pattern = single_line_pattern
        self.multi_line_pattern = multi_line_pattern
    
    def apply(self, code: str) -> str:
        """
        Remove comments from the code.
        
        Args:
            code (str): The code to process.
            
        Returns:
            str: The code without comments.
        """
        # Remove multi-line comments if pattern is provided
        if self.multi_line_pattern:
            code = re.sub(self.multi_line_pattern, '', code, flags=re.DOTALL)
        
        # Remove single-line comments if pattern is provided
        if self.single_line_pattern:
            code = re.sub(self.single_line_pattern, '', code, flags=re.MULTILINE)
        
        return code

class WhitespaceReductionAction(MinificationAction):
    """Action for reducing whitespace in code."""
    
    def __init__(self, preserve_newlines: bool = False):
        """
        Initialize the whitespace reduction action.
        
        Args:
            preserve_newlines (bool): Whether to preserve newlines.
        """
        self.preserve_newlines = preserve_newlines
    
    def apply(self, code: str) -> str:
        """
        Reduce whitespace in the code.
        
        Args:
            code (str): The code to process.
            
        Returns:
            str: The code with reduced whitespace.
        """
        if self.preserve_newlines:
            # Process each line separately to preserve newlines
            lines = code.split('\n')
            processed_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
            return '\n'.join(processed_lines)
        else:
            # Replace all whitespace with a single space
            return re.sub(r'\s+', ' ', code).strip()

class EmptyLineRemovalAction(MinificationAction):
    """Action for removing empty lines from code."""
    
    def apply(self, code: str) -> str:
        """
        Remove empty lines from the code.
        
        Args:
            code (str): The code to process.
            
        Returns:
            str: The code without empty lines.
        """
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        return '\n'.join(non_empty_lines)

class OperatorSpaceRemovalAction(MinificationAction):
    """Action for removing spaces around operators and punctuation."""
    
    def __init__(self, patterns: List[str] = None):
        """
        Initialize the operator space removal action.
        
        Args:
            patterns (List[str]): List of regex patterns for operators and punctuation.
        """
        self.patterns = patterns or [
            r'\s*([()])\s*',     # Spaces around parentheses
            r'\s*([{}])\s*',     # Spaces around braces
            r'\s*([[\]])\s*',    # Spaces around brackets
            r'\s*([+%\-*/=<>!&|:,])\s*'  # Spaces around operators and colons and commas
        ]
            
    def apply(self, code: str) -> str:
        """
        Remove spaces around operators and punctuation.
        
        Args:
            code (str): The code to process.
            
        Returns:
            str: The code without spaces around operators and punctuation.
        """
        for pattern in self.patterns:
            code = re.sub(pattern, r'\1', code)
        return code

class LineJoiningAction(MinificationAction):
    """Action for joining lines in code."""
    
    def __init__(self, separator: str = ';'):
        """
        Initialize the line joining action.
        
        Args:
            separator (str): The separator to use when joining lines.
        """
        self.separator = separator
    
    def apply(self, code: str) -> str:
        """
        Join lines in the code.
        
        Args:
            code (str): The code to process.
            
        Returns:
            str: The code with lines joined.
        """
        lines = code.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]

        result = ""
        for i, line in enumerate(non_empty_lines):
            if i > 0:
                result += self.separator
            # Supprimez le point-virgule final s'il existe déjà
            if line.endswith(self.separator):
                result += line[:-1]
            else:
                result += line
        
        return result

class CompositeMinificationAction(MinificationAction):
    """
    Composite Action that applies multiple minification strategies in sequence.
    
    This allows combining different actions to create custom minification pipelines.
    """
    
    def __init__(self, actions: List[MinificationAction] = None):
        """
        Initialize the composite minification action.
        
        Args:
            actions (List[MinificationAction]): List of actions to apply in sequence.
        """
        self.actions = actions or []
    
    def add_action(self, action: MinificationAction) -> None:
        """
        Add a action to the composite.
        
        Args:
            action (MinificationAction): The action to add.
        """
        self.actions.append(action)
    
    def apply(self, code: str) -> str:
        """
        Apply all actions in sequence.
        
        Args:
            code (str): The code to process.
            
        Returns:
            str: The code after applying all actions.
        """
        result = code
        for action in self.actions:
            result = action.apply(result)
        return result
    
    @property
    def name(self) -> str:
        """
        Get the name of the composite action.
        
        Returns:
            str: The name of the composite action.
        """
        action_names = [action.name for action in self.actions]
        return f"Composite({'+'.join(action_names)})"