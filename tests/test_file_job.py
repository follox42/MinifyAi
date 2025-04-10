"""
Tests for the minification job module.
"""
import unittest
import os
import tempfile
from unittest.mock import Mock, patch
from minifykit.file.job import MinificationJob
from minifykit.file.processor import FileProcessor
from minifykit.core.languages import LanguageMinifier


class MockMinifier(LanguageMinifier):
    """Mock minifier for testing."""
    
    def __init__(self, name="mock", extensions=None):
        self._name = name
        self._extensions = extensions or [".mock"]
        
    @property
    def name(self):
        return self._name
        
    @property
    def file_extensions(self):
        return self._extensions
        
    def minify(self, code, profile_name=None):
        return f"MINIFIED_{code}_WITH_{profile_name or 'default'}"


class TestMinificationJob(unittest.TestCase):
    """Tests for the MinificationJob class."""
    
    def setUp(self):
        """Set up the test case."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test.txt")
        self.minified_file = os.path.join(self.temp_dir.name, "test.min.txt")
        
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("TEST CONTENT")
        
        # Create minifier and processor
        self.minifier = MockMinifier()
        self.processor = FileProcessor()
        
        # Create job
        self.job = MinificationJob(
            file_path=self.test_file,
            minifier=self.minifier,
            file_processor=self.processor
        )
    
    def tearDown(self):
        """Clean up after the test case."""
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test job initialization."""
        self.assertEqual(self.job.file_path, self.test_file)
        self.assertEqual(self.job.minifier, self.minifier)
        self.assertEqual(self.job.file_processor, self.processor)
        self.assertEqual(self.job.minified_path, self.minified_file)
        
        # Test with custom profile and suffix
        custom_job = MinificationJob(
            file_path=self.test_file,
            minifier=self.minifier,
            file_processor=self.processor,
            suffix=".custommin"
        )
        
        expected_path = os.path.join(self.temp_dir.name, "test.custommin.txt")
        self.assertEqual(custom_job.minified_path, expected_path)
    
    def test_execute_new_file(self):
        """Test executing a job when the minified file doesn't exist."""
        # Execute the job
        result = self.job.execute()
        
        # Check that the minified file was created
        self.assertTrue(os.path.exists(self.minified_file))
        
        # Check the content of the minified file
        with open(self.minified_file, 'r') as f:
            content = f.read()
        
        self.assertEqual(content, "MINIFIED_TEST CONTENT_WITH_default")
        
        # Check that the function returned True (file was processed)
        self.assertTrue(result)
    
    def test_execute_no_change(self):
        """Test executing a job when the minified file exists and hasn't changed."""
        # Create minified file with the expected content
        with open(self.minified_file, 'w') as f:
            f.write("MINIFIED_TEST CONTENT_WITH_default")
        
        # Execute the job
        with patch('builtins.print') as mock_print:
            result = self.job.execute()
            
            # Check that the appropriate message was printed
            mock_print.assert_called_with(f"⏩ No change: {self.minified_file}")
        
        # Check that the function returned False (file was skipped)
        self.assertFalse(result)
    
    def test_execute_with_change(self):
        """Test executing a job when the minified file exists but has changed."""
        # Create minified file with different content
        with open(self.minified_file, 'w') as f:
            f.write("OLD CONTENT")
        
        # Execute the job
        with patch('builtins.print') as mock_print:
            result = self.job.execute()
            
            # Check that the appropriate message was printed
            mock_print.assert_called_with(f"✅ Minified: {self.minified_file}")
        
        # Check the updated content of the minified file
        with open(self.minified_file, 'r') as f:
            content = f.read()
            
        self.assertEqual(content, "MINIFIED_TEST CONTENT_WITH_default")
        
        # Check that the function returned True (file was processed)
        self.assertTrue(result)
    
    def test_execute_error(self):
        """Test executing a job that encounters an error."""
        # Create a faulty minifier that raises an exception
        faulty_minifier = Mock()
        faulty_minifier.minify.side_effect = ValueError("Test error")
        
        # Create a job with the faulty minifier
        faulty_job = MinificationJob(
            file_path=self.test_file,
            minifier=faulty_minifier,
            file_processor=self.processor
        )
        
        # Execute the job and check that it raises the exception
        with patch('builtins.print') as mock_print:
            with self.assertRaises(ValueError):
                faulty_job.execute()
                
            # Check that the error message was printed
            mock_print.assert_called_with(f"❌ Error processing {self.test_file}: Test error")


if __name__ == '__main__':
    unittest.main()