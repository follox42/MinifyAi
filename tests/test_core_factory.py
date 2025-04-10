"""
Tests for the action factory module.
"""
import unittest
from minifykit.core.actions.factory import create_action
from minifykit.core.actions.basic_actions import (
    CommentRemovalAction,
    WhitespaceReductionAction, 
    EmptyLineRemovalAction,
    OperatorSpaceRemovalAction,
    LineJoiningAction
)


class TestActionFactory(unittest.TestCase):
    """Tests for the action factory function."""
    
    def test_create_whitespace_action(self):
        """Test creating a whitespace reduction action."""
        action = create_action("whitespace")
        self.assertIsInstance(action, WhitespaceReductionAction)
        
        # Test with custom parameters
        action = create_action("whitespace", preserve_newlines=False)
        self.assertIsInstance(action, WhitespaceReductionAction)
        self.assertFalse(action.preserve_newlines)
    
    def test_create_comments_action(self):
        """Test creating a comment removal action."""
        action = create_action("comments")
        self.assertIsInstance(action, CommentRemovalAction)
        
        # Test with custom parameters
        action = create_action("comments", single_line_pattern=r'//.*$', multi_line_pattern=r'/\*.*?\*/')
        self.assertIsInstance(action, CommentRemovalAction)
        self.assertEqual(action.single_line_pattern, r'//.*$')
        self.assertEqual(action.multi_line_pattern, r'/\*.*?\*/')
    
    def test_create_empty_lines_action(self):
        """Test creating an empty line removal action."""
        action = create_action("empty_lines")
        self.assertIsInstance(action, EmptyLineRemovalAction)
    
    def test_create_operators_action(self):
        """Test creating an operator space removal action."""
        action = create_action("operators")
        self.assertIsInstance(action, OperatorSpaceRemovalAction)
        
        # Test with custom parameters
        patterns = [r'\s*=\s*', r'\s*\+\s*']
        action = create_action("operators", patterns=patterns)
        self.assertIsInstance(action, OperatorSpaceRemovalAction)
        self.assertEqual(action.patterns, patterns)
    
    def test_create_line_joining_action(self):
        """Test creating a line joining action."""
        action = create_action("line_joining")
        self.assertIsInstance(action, LineJoiningAction)
        
        # Test with custom separator
        action = create_action("line_joining", separator='>')
        self.assertIsInstance(action, LineJoiningAction)
        self.assertEqual(action.separator, '>')
    
    def test_custom_name(self):
        """Test creating an action with a custom name."""
        action = create_action("whitespace", name="CustomWhitespaceAction")
        self.assertEqual(action.name, "CustomWhitespaceAction")
    
    def test_unknown_action_type(self):
        """Test creating an action with an unknown type."""
        with self.assertRaises(ValueError):
            create_action("unknown_type")


if __name__ == '__main__':
    unittest.main()