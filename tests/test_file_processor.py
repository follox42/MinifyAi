"""
Tests for the file processor module.
"""
import unittest
import os
import tempfile
from minifykit.file.processor import FileProcessor


class TestFileProcessor(unittest.TestCase):
    """Tests for the FileProcessor class."""
    
    def setUp(self):
        """Set up the test case."""
        self.processor = FileProcessor()
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        """Clean up after the test case."""
        self.temp_dir.cleanup()
        
    def test_read_write_file(self):
        """Test reading and writing files."""
        test_file = os.path.join(self.temp_dir.name, "test.txt")
        test_content = "Hello, world!"
        
        # Write to the file
        self.processor.write_file(test_file, test_content)
        
        # Check that the file exists
        self.assertTrue(os.path.exists(test_file))
        
        # Read from the file
        content = self.processor.read_file(test_file)
        
        # Check that the content matches
        self.assertEqual(content, test_content)
        
    def test_file_exists(self):
        """Test checking if a file exists."""
        test_file = os.path.join(self.temp_dir.name, "test.txt")
        
        # File doesn't exist yet
        self.assertFalse(self.processor.file_exists(test_file))
        
        # Create the file
        with open(test_file, 'w') as f:
            f.write("Hello, world!")
        
        # File now exists
        self.assertTrue(self.processor.file_exists(test_file))
        
    def test_get_minified_path(self):
        """Test generating the path for the minified version of a file."""
        original_path = "/path/to/file.js"
        
        # Default suffix
        minified_path = self.processor.get_minified_path(original_path)
        self.assertEqual(minified_path, "/path/to/file.min.js")
        
        # Custom suffix
        minified_path = self.processor.get_minified_path(original_path, suffix=".minified")
        self.assertEqual(minified_path, "/path/to/file.minified.js")
        
    def test_delete_file(self):
        """Test deleting a file."""
        test_file = os.path.join(self.temp_dir.name, "test.txt")
        
        # Create the file
        with open(test_file, 'w') as f:
            f.write("Hello, world!")
        
        # File exists
        self.assertTrue(os.path.exists(test_file))
        
        # Delete the file
        self.processor.delete_file(test_file)
        
        # File no longer exists
        self.assertFalse(os.path.exists(test_file))
        
    def test_read_nonexistent_file(self):
        """Test reading a nonexistent file."""
        test_file = os.path.join(self.temp_dir.name, "nonexistent.txt")
        
        # Reading a nonexistent file should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.processor.read_file(test_file)
            
    def test_delete_nonexistent_file(self):
        """Test deleting a nonexistent file."""
        test_file = os.path.join(self.temp_dir.name, "nonexistent.txt")
        
        # Deleting a nonexistent file should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.processor.delete_file(test_file)


if __name__ == '__main__':
    unittest.main()