"""
Tests for the core actions module.
"""
import unittest
from minifykit.core.actions.basic_actions import (
    CommentRemovalAction,
    WhitespaceReductionAction,
    EmptyLineRemovalAction,
    OperatorSpaceRemovalAction,
    LineJoiningAction,
    CompositeMinificationAction
)


class TestCommentRemovalAction(unittest.TestCase):
    """Test the CommentRemovalAction class."""
    
    def test_single_line_comments(self):
        """Test removing single line comments."""
        code = "var x = 5; // This is a comment\nvar y = 10; // Another comment"
        action = CommentRemovalAction(single_line_pattern=r'//.*$')
        result = action.apply(code)
        expected = "var x = 5; \nvar y = 10; "
        self.assertEqual(result, expected)
    
    def test_multi_line_comments(self):
        """Test removing multi-line comments."""
        code = "var x = 5;\n/* Multi-line\ncomment */\nvar y = 10;"
        action = CommentRemovalAction(multi_line_pattern=r'/\*.*?\*/')
        result = action.apply(code)
        expected = "var x = 5;\n\nvar y = 10;"
        self.assertEqual(result, expected)
    
    def test_both_comment_types(self):
        """Test removing both single and multi-line comments."""
        code = "var x = 5; // Single line\n/* Multi-line\ncomment */\nvar y = 10;"
        action = CommentRemovalAction(
            single_line_pattern=r'//.*$',
            multi_line_pattern=r'/\*.*?\*/'
        )
        result = action.apply(code)
        expected = "var x = 5; \n\nvar y = 10;"
        self.assertEqual(result, expected)


class TestWhitespaceReductionAction(unittest.TestCase):
    """Test the WhitespaceReductionAction class."""
    
    def test_whitespace_reduction_preserve_newlines(self):
        """Test reducing whitespace while preserving newlines."""
        code = "  var   x  =  5;  \n  var  y  =  10;  "
        action = WhitespaceReductionAction(preserve_newlines=True)
        result = action.apply(code)
        expected = "var x = 5;\nvar y = 10;"
        self.assertEqual(result, expected)
    
    def test_whitespace_reduction_no_preserve_newlines(self):
        """Test reducing whitespace without preserving newlines."""
        code = "  var   x  =  5;  \n  var  y  =  10;  "
        action = WhitespaceReductionAction(preserve_newlines=False)
        result = action.apply(code)
        expected = "var x = 5; var y = 10;"
        self.assertEqual(result, expected)


class TestEmptyLineRemovalAction(unittest.TestCase):
    """Test the EmptyLineRemovalAction class."""
    
    def test_empty_line_removal(self):
        """Test removing empty lines."""
        code = "var x = 5;\n\n\nvar y = 10;\n\n"
        action = EmptyLineRemovalAction()
        result = action.apply(code)
        expected = "var x = 5;\nvar y = 10;"
        self.assertEqual(result, expected)


class TestOperatorSpaceRemovalAction(unittest.TestCase):
    """Test the OperatorSpaceRemovalAction class."""
    
    def test_operator_space_removal(self):
        """Test removing spaces around operators."""
        code = "var x = 5 + 10; var y = 20 - 5;"
        action = OperatorSpaceRemovalAction()
        result = action.apply(code)
        expected = "var x=5+10; var y=20-5;"
        self.assertEqual(result, expected)


class TestLineJoiningAction(unittest.TestCase):
    """Test the LineJoiningAction class."""
    
    def test_line_joining(self):
        """Test joining lines."""
        code = "var x = 5;\nvar y = 10;\nvar z = 15;"
        action = LineJoiningAction(separator=';')
        result = action.apply(code)
        expected = "var x = 5;var y = 10;var z = 15"
        self.assertEqual(result, expected)


class TestCompositeMinificationAction(unittest.TestCase):
    """Test the CompositeMinificationAction class."""
    
    def test_composite_action(self):
        """Test applying multiple actions in sequence."""
        code = "var x = 5; // Comment\n\nvar y = 10; // Another comment"
        composite = CompositeMinificationAction([
            CommentRemovalAction(single_line_pattern=r'//.*$'),
            EmptyLineRemovalAction(),
            WhitespaceReductionAction(preserve_newlines=True)
        ])
        result = composite.apply(code)
        expected = "var x = 5;\nvar y = 10;"
        self.assertEqual(result, expected)
    
    def test_add_action(self):
        """Test adding an action to a composite."""
        code = "var x = 5; // Comment\n\nvar y = 10; // Another comment"
        composite = CompositeMinificationAction([
            CommentRemovalAction(single_line_pattern=r'//.*$'),
            EmptyLineRemovalAction()
        ])
        composite.add_action(WhitespaceReductionAction(preserve_newlines=True))
        result = composite.apply(code)
        expected = "var x = 5;\nvar y = 10;"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()