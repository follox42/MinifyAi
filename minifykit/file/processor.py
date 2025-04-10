from __future__ import annotations
import os

class FileProcessor:
    """
    Class responsible for file operations.
    """
    
    def __init__(self):
        """Initialize the file processor."""
        pass
    
    def read_file(self, file_path: str) -> str:
        """
        Read the content of a file.
        
        Args:
            file_path (str): Path to the file.
            
        Returns:
            str: Content of the file.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            UnicodeDecodeError: If the file cannot be decoded as UTF-8.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write_file(self, file_path: str, content: str) -> None:
        """
        Write content to a file.
        
        Args:
            file_path (str): Path to the file.
            content (str): Content to write.
            
        Raises:
            PermissionError: If the file cannot be written to.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_minified_path(self, file_path: str, suffix: str = ".min") -> str:
        """
        Generate the path for the minified version of a file.
        
        Args:
            file_path (str): Path to the original file.
            suffix (str): Suffix to add to the minified file.
            
        Returns:
            str: Path for the minified file.
        """
        base, ext = os.path.splitext(file_path)
        return f"{base}{suffix}{ext}"
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path (str): Path to the file.
            
        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(file_path)
    
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file.
        
        Args:
            file_path (str): Path to the file.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be deleted.
        """
        os.remove(file_path)
