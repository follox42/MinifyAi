"""
Comprehensive tests for the languages module.
"""
import unittest
from minifykit.core.languages import (
    LanguageMinifier,
    PythonMinifier,
    JavaScriptMinifier,
    CSSMinifier,
    HTMLMinifier,
    create_custom_minifier
)
from minifykit.core.actions.basic_actions import (
    CommentRemovalAction,
    WhitespaceReductionAction,
    EmptyLineRemovalAction,
    OperatorSpaceRemovalAction,
    CompositeMinificationAction
)


class MockLanguageMinifier(LanguageMinifier):
    """A mock implementation of LanguageMinifier for testing."""
    
    def __init__(self, name="mock", extensions=None, minify_result=None):
        self._name = name
        self._extensions = extensions or [".mock"]
        self._minify_result = minify_result or "MINIFIED"
    
    @property
    def name(self):
        return self._name
    
    @property
    def file_extensions(self):
        return self._extensions
    
    def minify(self, code):
        return self._minify_result


class TestLanguageMinifier(unittest.TestCase):
    """Tests for the abstract LanguageMinifier class."""
    
    def test_abstract_methods(self):
        """Test that abstract methods must be implemented."""
        # Cannot instantiate abstract class
        with self.assertRaises(TypeError):
            LanguageMinifier()
        
        # But can instantiate a concrete subclass
        minifier = MockLanguageMinifier()
        self.assertEqual(minifier.name, "mock")
        self.assertEqual(minifier.file_extensions, [".mock"])
        self.assertEqual(minifier.minify("code"), "MINIFIED")


class TestPythonMinifier(unittest.TestCase):
    """Comprehensive tests for the PythonMinifier class."""
    
    def setUp(self):
        """Set up the test case."""
        self.minifier = PythonMinifier()
        
    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.minifier.name, "python")
        
    def test_extensions_property(self):
        """Test the file_extensions property."""
        self.assertEqual(self.minifier.file_extensions, [".py"])
        
    def test_default_minification(self):
        """Test the default minification behavior."""
        code = """
def hello():
    # This is a comment
    print("Hello, world!")  # Another comment
    
    # Empty line above
"""
        result = self.minifier.minify(code)
        # Should remove comments and empty lines
        self.assertNotIn("# This is a comment", result)
        self.assertNotIn("# Another comment", result)
        self.assertNotIn("\n\n", result)
        
    def test_preserve_newlines(self):
        """Test minification with preserve_newlines=True."""
        code = """def hello():
    print("Hello, world!")
    
    print("Another line")
"""
        # With preserve_newlines=True
        minifier = PythonMinifier(preserve_newlines=True)
        result = minifier.minify(code)
        # Should preserve line breaks
        self.assertIn("\n", result)
        
        # With preserve_newlines=False
        minifier.set_preserve_newlines(False)
        result = minifier.minify(code)
        # Should remove multiple line breaks
        self.assertNotIn("\n\n", result)
        
    def test_preserve_docstrings(self):
        """Test minification with preserve_docstrings=True."""
        code = '''def hello():
    """
    This is a docstring.
    """
    # This is a comment
    print("Hello, world!")
'''

        # With preserve_docstrings=False (default)
        result = self.minifier.minify(code)
        self.assertNotIn('"""', result)
        
        # With preserve_docstrings=True
        minifier = PythonMinifier(preserve_docstrings=True)
        result = minifier.minify(code)
        self.assertIn('"""', result)
        self.assertNotIn("# This is a comment", result)
        
        # Test setter method
        minifier.set_preserve_docstrings(False)
        result = minifier.minify(code)
        self.assertNotIn('"""', result)
    
    def test_create_action(self):
        """Test the _create_action method."""
        # Test with various configurations
        configs = [
            (True, True),   # preserve_newlines=True, preserve_docstrings=True
            (True, False),  # preserve_newlines=True, preserve_docstrings=False
            (False, True),  # preserve_newlines=False, preserve_docstrings=True
            (False, False)  # preserve_newlines=False, preserve_docstrings=False
        ]
        
        test_code = '''
def example():
    """
    This is a docstring.
    """
    # This is a comment
    return "Hello, world!"  # Another comment
'''
        
        for preserve_newlines, preserve_docstrings in configs:
            minifier = PythonMinifier(
                preserve_newlines=preserve_newlines,
                preserve_docstrings=preserve_docstrings
            )
            
            result = minifier.minify(test_code)
            
            # Check docstring handling
            if preserve_docstrings:
                self.assertIn('"""', result)
            else:
                self.assertNotIn('"""', result)
            
            # Check newline handling
            if preserve_newlines:
                # Should still have some newlines
                self.assertIn('\n', result)
            else:
                # Should have fewer newlines
                self.assertLessEqual(result.count('\n'), test_code.count('\n'))
    
    def test_complex_python_code(self):
        """Test minification of complex Python code with various features."""
        code = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Complex Python module example.

This module demonstrates various Python features for testing minification.
\"\"\"

import os
import sys
from typing import List, Dict, Optional

# Constants
DEBUG = True
VERSION = '1.0.0'

class ExampleClass:
    \"\"\"Example class docstring.\"\"\"
    
    def __init__(self, name: str, value: int = 0):
        \"\"\"Initialize the class.\"\"\"
        self.name = name    # Instance variable
        self.value = value  # With default
        
        # Some calculation
        self._computed = value * 2
    
    def get_info(self) -> Dict[str, object]:
        \"\"\"Return information about this instance.\"\"\"
        return {
            'name': self.name,
            'value': self.value,
            'computed': self._computed
        }
    
    @property
    def computed(self) -> int:
        # Property example
        return self._computed


def main():
    # Function with multiline comment
    '''
    This is the main function.
    It demonstrates various Python syntax elements.
    '''
    
    # Create an instance
    example = ExampleClass('test', 42)
    
    # Conditional
    if DEBUG:
        print(f"Created {example.name} with value {example.value}")
    
    # Loop
    for i in range(5):
        # Skip even numbers
        if i % 2 == 0:
            continue
        
        print(f"Processing {i}")
    
    # List comprehension
    squares = [x**2 for x in range(10) if x % 2 == 1]
    
    # With statement
    with open('example.txt', 'w') as f:
        f.write("Example content\\n")
    
    return example.get_info()


if __name__ == "__main__":
    # Script entry point
    result = main()
    print(result)
    
    # Exit
    sys.exit(0)
"""
        
        # Test with default settings
        result = self.minifier.minify(code)
        
        # Comments and docstrings should be removed
        self.assertNotIn("# Constants", result)
        self.assertNotIn('"""\nComplex Python module example.', result)
        self.assertNotIn("\"\"\"Example class docstring.\"\"\"", result)
        
        # Code structure should be preserved
        self.assertIn("import os", result)
        self.assertIn("import sys", result)
        self.assertIn("from typing import List, Dict, Optional", result)
        self.assertIn("DEBUG = True", result)
        self.assertIn("VERSION = '1.0.0'", result)
        self.assertIn("class ExampleClass:", result)
        self.assertIn("def __init__(self, name: str, value: int = 0):", result)
        self.assertIn("def get_info(self) -> Dict[str, object]:", result)
        self.assertIn("@property", result)
        self.assertIn("def computed(self) -> int:", result)
        self.assertIn("def main():", result)
        self.assertIn("example = ExampleClass('test', 42)", result)
        self.assertIn("if DEBUG:", result)
        self.assertIn("for i in range(5):", result)
        self.assertIn("if i % 2 == 0:", result)
        self.assertIn("squares = [x**2 for x in range(10) if x % 2 == 1]", result)
        self.assertIn("with open('example.txt', 'w') as f:", result)
        self.assertIn("if __name__ == \"__main__\":", result)
        
        # Test with preserve_docstrings=True
        minifier = PythonMinifier(preserve_docstrings=True)
        result = minifier.minify(code)
        
        # Regular comments should still be removed
        self.assertNotIn("# Constants", result)


class TestJavaScriptMinifier(unittest.TestCase):
    """Comprehensive tests for the JavaScriptMinifier class."""
    
    def setUp(self):
        """Set up the test case."""
        self.minifier = JavaScriptMinifier()
        
    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.minifier.name, "javascript")
        
    def test_extensions_property(self):
        """Test the file_extensions property."""
        self.assertEqual(self.minifier.file_extensions, [".js"])
        
    def test_default_minification(self):
        """Test the default minification behavior."""
        code = """
function hello() {
    // This is a comment
    console.log("Hello, world!");  // Another comment
    
    /* Multi-line
    comment */
}
"""
        result = self.minifier.minify(code)
        # Should remove comments
        self.assertNotIn("// This is a comment", result)
        self.assertNotIn("// Another comment", result)
        self.assertNotIn("/* Multi-line", result)
        
    def test_aggressive_minification(self):
        """Test aggressive minification."""
        code = """
function hello() {
    var x = 10;
    var y = 20;
    return x + y;
}
"""
        # Default (non-aggressive)
        result = self.minifier.minify(code)
        self.assertIn(" = ", result)  # Space around operators is preserved
        
        # Aggressive
        aggressive_minifier = JavaScriptMinifier(aggressive=True)
        result = aggressive_minifier.minify(code)
        self.assertIn("=", result)  # Operators are included
        self.assertNotIn(" = ", result)  # But spaces around them are removed
        
        # Test setter method
        self.minifier.set_aggressive(True)
        result = self.minifier.minify(code)
        self.assertNotIn(" = ", result)
    
    def test_setter_methods(self):
        """Test the setter methods."""
        minifier = JavaScriptMinifier(preserve_newlines=True, aggressive=False)
        
        # Test initial state
        code = "function f() {\n  var x = 1 + 2;\n  return x;\n}"
        result = minifier.minify(code)
        self.assertIn("\n", result)  # Newlines preserved
        self.assertIn(" = ", result)  # Spaces around operators preserved
        
        # Test set_preserve_newlines
        minifier.set_preserve_newlines(False)
        result = minifier.minify(code)
        self.assertLess(result.count("\n"), code.count("\n"))
        
        # Test set_aggressive
        minifier.set_aggressive(True)
        result = minifier.minify(code)
        self.assertIn("=", result)  # Equal sign is present
        self.assertNotIn(" = ", result)  # But spaces around it are removed
    
    def test_complex_javascript(self):
        """Test minification of complex JavaScript code."""
        code = """/**
 * Complex JavaScript module example.
 *
 * This module demonstrates various JavaScript features for testing minification.
 */

// Import dependencies
import { Component } from 'library';

// Constants
const DEBUG = true;
const VERSION = '1.0.0';

/**
 * Example class
 */
class ExampleClass {
    /**
     * Constructor
     */
    constructor(name, value = 0) {
        this.name = name;    // Instance variable
        this.value = value;  // With default
        
        // Some calculation
        this._computed = value * 2;
    }
    
    /**
     * Get information about this instance
     */
    getInfo() {
        return {
            name: this.name,
            value: this.value,
            computed: this._computed
        };
    }
    
    // Arrow function example
    processItems = (items) => {
        return items.map(item => {
            // Transform each item
            return {
                ...item,
                processed: true
            };
        });
    }
    
    // Getter
    get computed() {
        return this._computed;
    }
}

// Main function
function main() {
    // Function with multiline comment
    /*
    This is the main function.
    It demonstrates various JavaScript syntax elements.
    */
    
    // Create an instance
    const example = new ExampleClass('test', 42);
    
    // Conditional
    if (DEBUG) {
        console.log(`Created ${example.name} with value ${example.value}`);
    }
    
    // Loop
    for (let i = 0; i < 5; i++) {
        // Skip even numbers
        if (i % 2 === 0) {
            continue;
        }
        
        console.log(`Processing ${i}`);
    }
    
    // Array methods
    const numbers = [1, 2, 3, 4, 5];
    const squares = numbers
        .filter(x => x % 2 === 1)
        .map(x => x * x);
    
    // Async/await example
    async function fetchData() {
        try {
            const response = await fetch('https://api.example.com/data');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching data:', error);
            return null;
        }
    }
    
    // Promise example
    return new Promise((resolve, reject) => {
        // Simulating async operation
        setTimeout(() => {
            resolve(example.getInfo());
        }, 100);
    });
}

// Export
export default main;

// IIFE example
(function() {
    // Self-invoking function
    console.log('Module loaded');
})();
"""
        
        # Test with default settings
        result = self.minifier.minify(code)
        
        # Comments should be removed
        self.assertNotIn("// Import dependencies", result)
        self.assertNotIn("// Constants", result)
        self.assertNotIn("/**", result)
        self.assertNotIn("* Complex JavaScript module example", result)
        self.assertNotIn("// Export", result)
        
        # Code structure should be preserved
        self.assertIn("import { Component } from 'library';", result)
        self.assertIn("const DEBUG = true;", result)
        self.assertIn("const VERSION = '1.0.0';", result)
        self.assertIn("class ExampleClass {", result)
        self.assertIn("constructor(name, value = 0) {", result)
        self.assertIn("this.name = name;", result)
        self.assertIn("this.value = value;", result)
        self.assertIn("getInfo() {", result)
        self.assertIn("processItems = (items) => {", result)
        self.assertIn("get computed() {", result)
        self.assertIn("function main() {", result)
        self.assertIn("const example = new ExampleClass('test', 42);", result)
        self.assertIn("if (DEBUG) {", result)
        self.assertIn("for (let i = 0; i < 5; i++) {", result)
        self.assertIn("if (i % 2 === 0) {", result)
        self.assertIn("const numbers = [1, 2, 3, 4, 5];", result)
        self.assertIn("async function fetchData() {", result)
        self.assertIn("try {", result)
        self.assertIn("catch (error) {", result)
        self.assertIn("return new Promise((resolve, reject) => {", result)
        self.assertIn("export default main;", result)
        self.assertIn("(function() {", result)
        
        # Test with aggressive=True
        minifier = JavaScriptMinifier(aggressive=True)
        result = minifier.minify(code)
        
        # Spaces around operators should be removed
        self.assertIn("value=0", result)
        self.assertIn("i<5", result)
        self.assertIn("i%2===0", result)
        
        # Code should still be valid JavaScript
        self.assertIn("class ExampleClass{", result)
        self.assertIn("constructor(name,value=0){", result)
        self.assertIn("this.name=name;", result)
        self.assertIn("this.value=value;", result)


class TestCSSMinifier(unittest.TestCase):
    """Comprehensive tests for the CSSMinifier class."""
    
    def setUp(self):
        """Set up the test case."""
        self.minifier = CSSMinifier()
        
    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.minifier.name, "css")
        
    def test_extensions_property(self):
        """Test the file_extensions property."""
        self.assertEqual(self.minifier.file_extensions, [".css"])
        
    def test_basic_minification(self):
        """Test basic CSS minification."""
        code = """
body {
    /* This is a comment */
    font-size: 16px;
    
    color: #333;
}
"""
        result = self.minifier.minify(code)
        # Comments should be removed
        self.assertNotIn("/* This is a comment */", result)
        # Whitespace should be reduced
        self.assertNotIn("    ", result)
        # Properties should be preserved
        self.assertIn("font-size:16px", result)
        self.assertIn("color:#333", result)
    
    def test_complex_css_minification(self):
        """Test minifying complex CSS code."""
        css = """
        /* Header styles */
        header {
            background-color: #f8f9fa;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Navigation styles */
        nav ul {
            display: flex;
            list-style: none;
            margin: 0;
            padding: 0;
        }
        
        nav li {
            margin-right: 20px;
        }
        
        /* This is an important comment that should be removed */
        nav a {
            color: #333;
            text-decoration: none;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            /* Mobile styles */
            header {
                padding: 10px;
            }
            
            nav ul {
                flex-direction: column;
            }
            
            nav li {
                margin-right: 0;
                margin-bottom: 10px;
            }
        }
        """
        
        result = self.minifier.minify(css)
        
        # Check that all comments are removed
        self.assertNotIn("/* Header styles */", result)
        self.assertNotIn("/* Navigation styles */", result)
        self.assertNotIn("/* This is an important comment that should be removed */", result)
        self.assertNotIn("/* Mobile styles */", result)
        
        # Check that all necessary CSS properties are preserved
        self.assertIn("background-color:#f8f9fa", result)
        self.assertIn("padding:20px", result)
        self.assertIn("box-shadow:0 2px 4px rgba(0,0,0,0.1)", result)
        self.assertIn("display:flex", result)
        self.assertIn("list-style:none", result)
        self.assertIn("margin:0", result)
        self.assertIn("padding:0", result)
        self.assertIn("margin-right:20px", result)
        self.assertIn("color:#333", result)
        self.assertIn("text-decoration:none", result)
        self.assertIn("font-weight:bold", result)
        self.assertIn("@media(max-width:768px)", result)
        self.assertIn("padding:10px", result)
        self.assertIn("flex-direction:column", result)
        self.assertIn("margin-right:0", result)
        self.assertIn("margin-bottom:10px", result)
        
        # Check that whitespace is significantly reduced
        self.assertNotIn("    ", result)
        self.assertNotIn("\n\n", result)
    
    def test_css_advanced_features(self):
        """Test minification of CSS with advanced features."""
        css = """
        /* CSS Variables */
        :root {
            --primary-color: #3498db;
            --secondary-color: #2ecc71;
            --text-color: #333;
            --spacing: 20px;
        }

        /* Advanced selectors */
        .container > .item {
            color: var(--text-color);
        }

        /* Attribute selectors */
        input[type="text"] {
            border: 1px solid #ccc;
        }

        /* Pseudo-classes and pseudo-elements */
        a:hover, a:focus {
            color: var(--primary-color);
        }

        p::first-line {
            font-weight: bold;
        }

        /* Flexbox */
        .flex-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        /* Grid */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-gap: var(--spacing);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .animated {
            animation: fadeIn 1s ease-in-out;
        }

        /* Media queries */
        @media screen and (max-width: 768px) {
            .grid-container {
                grid-template-columns: 1fr;
            }
        }

        /* Custom properties and calculations */
        .dynamic-element {
            width: calc(100% - var(--spacing) * 2);
            margin: var(--spacing);
            background-color: var(--secondary-color);
        }
        """
        
        result = self.minifier.minify(css)
        
        # Comments should be removed
        self.assertNotIn("/* CSS Variables */", result)
        self.assertNotIn("/* Advanced selectors */", result)
        
        # CSS features should be preserved
        self.assertIn(":root{", result)
        self.assertIn("--primary-color:#3498db", result)
        self.assertIn(".container>.item{", result)
        self.assertIn("color:var(--text-color)", result)
        self.assertIn("input[type=\"text\"]", result)
        self.assertIn("a:hover,a:focus{", result)
        self.assertIn("p::first-line{", result)
        self.assertIn("display:flex", result)
        self.assertIn("justify-content:space-between", result)
        self.assertIn("display:grid", result)
        self.assertIn("grid-template-columns:repeat(3,1fr)", result)
        self.assertIn("@keyframes fadeIn{", result)
        self.assertIn("from{opacity:0;}", result)
        self.assertIn("to{opacity:1;}", result)
        self.assertIn("animation:fadeIn 1s ease-in-out", result)
        self.assertIn("@media screen and(max-width:768px)", result)
        self.assertIn("width:calc(100%-var(--spacing)*2)", result)
        self.assertIn("background-color:var(--secondary-color)", result)


class TestHTMLMinifier(unittest.TestCase):
    """Comprehensive tests for the HTMLMinifier class."""
    
    def setUp(self):
        """Set up the test case."""
        self.minifier = HTMLMinifier()
        
    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.minifier.name, "html")
        
    def test_extensions_property(self):
        """Test the file_extensions property."""
        self.assertEqual(self.minifier.file_extensions, [".html", ".htm"])
        
    def test_basic_minification(self):
        """Test HTML minification."""
        code = """
<!DOCTYPE html>
<html>
    <head>
        <title>Test Page</title>
        <!-- This is a comment -->
    </head>
    <body>
        <h1>Hello, World!</h1>
        
        <p>This is a test page.</p>
    </body>
</html>
"""
        result = self.minifier.minify(code)
        # Comments should be removed
        self.assertNotIn("<!-- This is a comment -->", result)
        # HTML tags should be preserved
        self.assertIn("<title>Test Page</title>", result)
        self.assertIn("<h1>Hello, World!</h1>", result)
        
    def test_preserve_newlines(self):
        """Test HTML minification with different newline settings."""
        code = """
<div>
    <p>Line 1</p>
    
    <p>Line 2</p>
</div>
"""
        # With preserve_newlines=True (default)
        result = self.minifier.minify(code)
        # New lines between tags should be preserved
        self.assertIn("<p>Line 1</p>", result)
        self.assertIn("<p>Line 2</p>", result)
        self.assertIn("\n", result)
        
        # With preserve_newlines=False
        minifier = HTMLMinifier(preserve_newlines=False)
        result = minifier.minify(code)
        # All content should be on one line
        self.assertNotIn("\n", result)
        
        # Test setter method
        self.minifier.set_preserve_newlines(False)
        result = self.minifier.minify(code)
        self.assertNotIn("\n", result)
    
    def test_complex_html(self):
        """Test minifying more complex HTML with nested tags."""
        html = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Complex Test</title>
        <style>
            /* CSS comment */
            body { font-family: Arial; }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </nav>
        </header>
        
        <main>
            <article>
                <h1>Article Title</h1>
                <p>Article content goes here...</p>
                
                <!-- Article comment -->
                <section>
                    <h2>Section Title</h2>
                    <p>Section content...</p>
                </section>
            </article>
        </main>
        
        <footer>
            <p>&copy; 2025</p>
        </footer>
        
        <script>
            // JavaScript comment
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Loaded!');
            });
        </script>
    </body>
</html>
"""
        result = self.minifier.minify(html)
        
        # Test comment removal
        self.assertNotIn("/* CSS comment */", result)
        self.assertNotIn("<!-- Article comment -->", result)
        self.assertNotIn("// JavaScript comment", result)
        
        # Test structure preservation
        self.assertIn("<!DOCTYPE html>", result)
        self.assertIn("<meta charset=\"UTF-8\">", result)
        self.assertIn("<title>Complex Test</title>", result)
        self.assertIn("<h1>Article Title</h1>", result)
        self.assertIn("<p>Article content goes here...</p>", result)
        self.assertIn("<footer>", result)
        self.assertIn("<p>&copy; 2025</p>", result)
        
        # Test script preservation
        self.assertIn("document.addEventListener('DOMContentLoaded', function() {", result)
        self.assertIn("console.log('Loaded!');", result)
    
    def test_complex_html_with_attributes(self):
        """Test minifying HTML with various attributes and special cases."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Page</title>
    <!-- This is a metadata comment -->
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <!-- Navigation section -->
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
    </nav>
    
    <main>
        <section>
            <h1>Welcome to Our Website</h1>
            <p>This is a paragraph with some <strong>bold text</strong> and <em>italicized text</em>.</p>
            
            <!-- This comment should be removed -->
            <div class="info-box">
                <h2>Important Information</h2>
                <p>Here is some important information that you should know.</p>
            </div>
        </section>
        
        <section>
            <h2>Our Services</h2>
            <ul>
                <li>Service 1</li>
                <li>Service 2</li>
                <li>Service 3</li>
            </ul>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 Example Company</p>
    </footer>
    
    <!-- Scripts -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Page loaded!');
        });
    </script>
</body>
</html>"""
        
        # With default settings (preserve_newlines=True)
        result = self.minifier.minify(html)
        
        # Check that comments are removed
        self.assertNotIn("<!-- This is a metadata comment -->", result)
        self.assertNotIn("<!-- Navigation section -->", result)
        self.assertNotIn("<!-- This comment should be removed -->", result)
        self.assertNotIn("<!-- Scripts -->", result)
        
        # Check that HTML structure is preserved
        self.assertIn("<!DOCTYPE html>", result)
        self.assertIn('<html lang="en">', result)
        self.assertIn('<meta charset="UTF-8">', result)
        self.assertIn('<title>Test Page</title>', result)
        self.assertIn('<nav>', result)
        self.assertIn('<main>', result)
        self.assertIn('<footer>', result)
        self.assertIn('<script>', result)
        
        # With preserve_newlines=False
        minifier = HTMLMinifier(preserve_newlines=False)
        result = minifier.minify(html)
        
        # Check that all necessary content is still preserved
        self.assertIn("<!DOCTYPE html>", result)
        self.assertIn('<title>Test Page</title>', result)
        self.assertIn('<h1>Welcome to Our Website</h1>', result)
        self.assertIn('<p>This is a paragraph with some <strong>bold text</strong> and <em>italicized text</em>.</p>', result)
        
        # Verify that there are significantly fewer newlines
        original_newline_count = html.count('\n')
        result_newline_count = result.count('\n')
        self.assertLess(result_newline_count, original_newline_count)


class TestCreateCustomMinifier(unittest.TestCase):
    """Tests for the create_custom_minifier function."""
    
    def test_create_custom_minifier_for_json(self):
        """Test creating a custom minifier for JSON."""
        json_minifier = create_custom_minifier(
            name="json",
            extensions=[".json"],
            actions=[
                WhitespaceReductionAction(preserve_newlines=False),
                EmptyLineRemovalAction(),
                OperatorSpaceRemovalAction()
            ]
        )
        
        # Check properties
        self.assertEqual(json_minifier.name, "json")
        self.assertEqual(json_minifier.file_extensions, [".json"])
        
        # Test minification
        json_code = """{
    "name": "John Doe",
    "age": 30,
    "isEmployed": true,
    
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345"
    },
    
    "phoneNumbers": [
        {
            "type": "home",
            "number": "555-1234"
        },
        {
            "type": "work",
            "number": "555-5678"
        }
    ]
}"""
        
        result = json_minifier.minify(json_code)
        
        # Check that whitespace is reduced
        self.assertNotIn("    ", result)
        self.assertNotIn("\n", result)
        
        # Check that all data is preserved
        self.assertIn('"name":"John Doe"', result)
        self.assertIn('"age":30', result)
        self.assertIn('"isEmployed":true', result)
        self.assertIn('"street":"123 Main St"', result)
        self.assertIn('"type":"home"', result)
        self.assertIn('"number":"555-1234"', result)
    
    def test_create_custom_minifier_for_sql(self):
        """Test creating a custom minifier for SQL."""
        sql_minifier = create_custom_minifier(
            name="sql",
            extensions=[".sql"],
            actions=[
                CommentRemovalAction(
                    single_line_pattern=r'--.*$',
                    multi_line_pattern=r'/\*.*?\*/'
                ),
                WhitespaceReductionAction(preserve_newlines=True),
                EmptyLineRemovalAction()
            ]
        )
        
        # Check properties
        self.assertEqual(sql_minifier.name, "sql")
        self.assertEqual(sql_minifier.file_extensions, [".sql"])
        
        # Test minification
        sql_code = """-- Create a users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    
    /* This is a multi-line comment
       about the password field */
    password_hash VARCHAR(100) NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data
INSERT INTO users (username, email, password_hash)
VALUES 
    ('john_doe', 'john@example.com', 'hashed_password_1'),
    ('jane_smith', 'jane@example.com', 'hashed_password_2');

/* Select all users */
SELECT * FROM users WHERE created_at > '2025-01-01';"""
        
        result = sql_minifier.minify(sql_code)
        
        # Check that comments are removed
        self.assertNotIn("-- Create a users table", result)
        self.assertNotIn("-- Insert test data", result)
        self.assertNotIn("/* This is a multi-line comment", result)
        self.assertNotIn("/* Select all users */", result)
        
        # Check that SQL structure is preserved
        self.assertIn("CREATE TABLE users (", result)
        self.assertIn("id INTEGER PRIMARY KEY", result)
        self.assertIn("username VARCHAR(50) NOT NULL UNIQUE", result)
        self.assertIn("email VARCHAR(100) NOT NULL UNIQUE", result)
        self.assertIn("password_hash VARCHAR(100) NOT NULL", result)
        self.assertIn("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP", result)
        self.assertIn("INSERT INTO users (username, email, password_hash)", result)
        self.assertIn("VALUES", result)
        self.assertIn("('john_doe', 'john@example.com', 'hashed_password_1')", result)
        self.assertIn("('jane_smith', 'jane@example.com', 'hashed_password_2')", result)
        self.assertIn("SELECT * FROM users WHERE created_at > '2025-01-01'", result)
    
    def test_create_custom_minifier_minimal(self):
        """Test creating a custom minifier with minimal configuration."""
        minifier = create_custom_minifier(
            name="test",
            extensions=[".test"],
            actions=[]
        )
        
        # Check properties
        self.assertEqual(minifier.name, "test")
        self.assertEqual(minifier.file_extensions, [".test"])
        
        # No actions means no changes
        test_code = "This is a test"
        self.assertEqual(minifier.minify(test_code), test_code)
    
    def test_create_custom_minifier_with_single_action(self):
        """Test creating a custom minifier with a single action."""
        minifier = create_custom_minifier(
            name="test",
            extensions=[".test"],
            actions=[WhitespaceReductionAction(preserve_newlines=False)]
        )
        
        test_code = "This   is  a  test\nwith  multiple  spaces"
        result = minifier.minify(test_code)
        
        self.assertEqual(result, "This is a test with multiple spaces")
    
    def test_create_custom_minifier_complex_chain(self):
        """Test creating a custom minifier with a complex chain of actions."""
        minifier = create_custom_minifier(
            name="test",
            extensions=[".test", ".tst"],
            actions=[
                CommentRemovalAction(single_line_pattern=r'#.*$'),
                WhitespaceReductionAction(preserve_newlines=True),
                EmptyLineRemovalAction()
            ]
        )
        
        test_code = """Line 1 with   spaces # and a comment
        
Line 2 with   more   spaces # another comment

# A comment-only line"""

        result = minifier.minify(test_code)
        
        # Check that comments are removed
        self.assertNotIn("#", result)
        
        # Check that whitespace is reduced
        self.assertNotIn("   ", result)
        
        # Check that empty lines are removed
        self.assertNotIn("\n\n", result)
        
        # Check that the content is preserved
        self.assertIn("Line 1 with spaces", result)
        self.assertIn("Line 2 with more spaces", result)
        
        # Check that a comment-only line is completely removed
        self.assertNotIn("A comment-only line", result)


if __name__ == '__main__':
    unittest.main()