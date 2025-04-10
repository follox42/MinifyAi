from typing import Optional
from ..core.languages import LanguageMinifier
from .processor import FileProcessor

class MinificationJob:
    """
    Class representing a minification job for a single file.
    """
    
    def __init__(self, file_path: str, minifier: LanguageMinifier, 
                file_processor: FileProcessor,
                suffix: str = ".min"):
        """
        Initialize the minification job.
        
        Args:
            file_path (str): Path to the file to minify.
            minifier (LanguageMinifier): The minifier to use.
            file_processor (FileProcessor): The file processor to use.
            profile_name (Optional[str]): The name of the profile to use.
                If None, the default profile is used.
            suffix (str): Suffix to add to the minified file.
        """
        self.file_path = file_path
        self.minifier = minifier
        self.file_processor = file_processor
        self.minified_path = file_processor.get_minified_path(file_path, suffix)
    
    def execute(self) -> bool:
        """
        Execute the minification job.
        
        Returns:
            bool: True if the file was minified, False if it was skipped.
            
        Raises:
            Exception: If an error occurs during minification.
        """
        try:
            # Read the file
            code = self.file_processor.read_file(self.file_path)
            
            # Minify the code
            minified_code = self.minifier.minify(code)
            
            # Check if the minified file already exists and if it has changed
            if self.file_processor.file_exists(self.minified_path):
                existing_code = self.file_processor.read_file(self.minified_path)
                if existing_code == minified_code:
                    print(f"⏩ No change: {self.minified_path}")
                    return False  # Skip writing if identical
            
            # Write the minified code
            self.file_processor.write_file(self.minified_path, minified_code)
            print(f"✅ Minified: {self.minified_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error processing {self.file_path}: {e}")
            raise