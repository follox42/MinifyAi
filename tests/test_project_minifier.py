"""
Tests for the project minifier module.
"""
import unittest
import os
import tempfile
from unittest.mock import Mock, patch
from minifykit.project.minify import ProjectMinifier
from minifykit.project.registry import MinifierRegistry
from minifykit.file.processor import FileProcessor
from minifykit.core.languages import LanguageMinifier


class MockMinifier(LanguageMinifier):
    """Mock minifier for testing."""
    
    def __init__(self, name, extensions):
        self._name = name
        self._extensions = extensions
        
    @property
    def name(self):
        return self._name
        
    @property
    def file_extensions(self):
        return self._extensions
        
    def minify(self, code, profile_name=None):
        return f"MINIFIED_{code}_WITH_{profile_name or 'default'}"


class TestProjectMinifier(unittest.TestCase):
    """Tests for the ProjectMinifier class."""
    
    def setUp(self):
        """Set up the test case."""
        # Create a minifier registry and register some mock minifiers
        self.registry = MinifierRegistry()
        self.registry.register_minifier(MockMinifier("python", [".py"]))
        self.registry.register_minifier(MockMinifier("javascript", [".js"]))
        
        # Create a file processor
        self.file_processor = FileProcessor()
        
        # Create a project minifier
        self.project_minifier = ProjectMinifier(self.registry, self.file_processor)
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        """Clean up after the test case."""
        self.temp_dir.cleanup()
        
    def _create_test_files(self):
        """Create some test files for the project minifier."""
        # Create a Python file
        py_file = os.path.join(self.temp_dir.name, "test.py")
        with open(py_file, 'w') as f:
            f.write("def hello(): print('Hello, world!')")
            
        # Create a JavaScript file
        js_file = os.path.join(self.temp_dir.name, "test.js")
        with open(js_file, 'w') as f:
            f.write("function hello() { console.log('Hello, world!'); }")
            
        # Create an already minified file
        min_file = os.path.join(self.temp_dir.name, "test.min.js")
        with open(min_file, 'w') as f:
            f.write("function hello(){console.log('Hello, world!')}")
            
        # Create a file with an unsupported extension
        txt_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("Hello, world!")
            
        # Create a directory to be skipped
        skip_dir = os.path.join(self.temp_dir.name, "__pycache__")
        os.makedirs(skip_dir, exist_ok=True)
        skip_file = os.path.join(skip_dir, "test.py")
        with open(skip_file, 'w') as f:
            f.write("def hello(): print('Hello, world!')")
            
    def test_minify_project(self):
        """Test minifying a project."""
        # Create test files
        self._create_test_files()
        
        # Mock the MinificationJob.execute method to avoid actual file operations
        with patch('minifykit.file.job.MinificationJob.execute', return_value=True):
            # Minify the project
            processed, skipped = self.project_minifier.minify_project(self.temp_dir.name)
            
            # Check that the Python and JavaScript files were processed
            self.assertEqual(processed, 2)
            
            # Check that the minified file was skipped
            self.assertEqual(skipped, 1)
            
    def test_minify_project_with_languages(self):
        """Test minifying a project with specific languages."""
        # Create test files
        self._create_test_files()
        
        # Mock the MinificationJob.execute method to avoid actual file operations
        with patch('minifykit.file.job.MinificationJob.execute', return_value=True):
            # Minify only Python files
            processed, skipped = self.project_minifier.minify_project(
                self.temp_dir.name, languages=["python"]
            )
            
            # Check that only the Python file was processed
            self.assertEqual(processed, 1)
            
    def test_minify_project_with_extensions(self):
        """Test minifying a project with specific extensions."""
        # Create test files
        self._create_test_files()
        
        # Mock the MinificationJob.execute method to avoid actual file operations
        with patch('minifykit.file.job.MinificationJob.execute', return_value=True):
            # Minify only .js files
            processed, skipped = self.project_minifier.minify_project(
                self.temp_dir.name, extensions=[".js"]
            )
            
            # Check that only the JavaScript file was processed
            self.assertEqual(processed, 1)
            
    def test_delete_minified_files(self):
        """Test deleting minified files."""
        # Create test files
        self._create_test_files()
        
        # Delete minified files
        count = self.project_minifier.delete_minified_files(self.temp_dir.name)
        
        # Check that one minified file was deleted
        self.assertEqual(count, 1)
        
        # Check that the minified file doesn't exist anymore
        min_file = os.path.join(self.temp_dir.name, "test.min.js")
        self.assertFalse(os.path.exists(min_file))
        
    def test_delete_minified_files_with_extensions(self):
        """Test deleting minified files with specific extensions."""
        # Create test files
        self._create_test_files()
        
        # Create a minified Python file
        min_py_file = os.path.join(self.temp_dir.name, "test.min.py")
        with open(min_py_file, 'w') as f:
            f.write("def hello():print('Hello, world!')")
            
        # Delete only minified JavaScript files
        count = self.project_minifier.delete_minified_files(
            self.temp_dir.name, extensions=[".js"]
        )
        
        # Check that one minified file was deleted
        self.assertEqual(count, 1)
        
        # Check that the minified JavaScript file doesn't exist anymore
        min_js_file = os.path.join(self.temp_dir.name, "test.min.js")
        self.assertFalse(os.path.exists(min_js_file))
        
        # Check that the minified Python file still exists
        self.assertTrue(os.path.exists(min_py_file))


if __name__ == '__main__':
    unittest.main()