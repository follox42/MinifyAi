from typing import List, Optional, Tuple, Set
import os
from typing import TYPE_CHECKING
from ..file.job import MinificationJob
from .registry import MinifierRegistry
from ..file.processor import FileProcessor

class ProjectMinifier:
    """
    Class responsible for minifying an entire project.
    
    This class follows the Dependency Inversion Principle by depending on
    abstractions (MinifierRegistry, FileProcessor) rather than concrete implementations.
    """
    
    def __init__(self, minifier_registry: MinifierRegistry, file_processor: FileProcessor, files_to_skip: Optional[List[str]] = None):
        """
        Initialize the project minifier.
        
        Args:
            minifier_registry (MinifierRegistry): The minifier registry to use.
            file_processor (FileProcessor): The file processor to use.
        """
        self.minifier_registry = minifier_registry
        self.file_processor = file_processor
        self.files_to_skip = files_to_skip or ["__pycache__"]
    
    def minify_project(self, root_dir: str,
                      languages: Optional[List[str]] = None, 
                      extensions: Optional[List[str]] = None,
                      suffix: str = ".min", files_to_skip = None) -> Tuple[int, int]:
        """
        Minify all files in a project.
        
        Args:
            root_dir (str): The root directory of the project.
            file_types (Optional[List[str]]): List of file types to process (e.g., ['python', 'javscipt']).
            extensions (Optional[List[str]]): List of extensions to process.
            suffix (str): Suffix to add to minified files.
            
        Returns:
            Tuple[int, int]: The number of processed and skipped files.
        """
        if files_to_skip:
            self.files_to_skip.extend(files_to_skip)

        # Initialize counters
        processed = 0
        skipped = 0
        
        # Determine which extensions to process
        extensions_to_process = self._get_extensions_to_process(languages, extensions)
        
        print(f"🔍 Processing file types: {', '.join(extensions_to_process)}")

        # Walk through the directory tree
        for foldername, subfolders, filenames in os.walk(root_dir):
            # Check if this directory should be skipped
            skip_this_dir = False
            for skip_dir in self.files_to_skip:
                if skip_dir in foldername:
                    skip_this_dir = True
                    break

            if skip_this_dir:
                continue

            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                _, file_ext = os.path.splitext(filename)
                file_ext = file_ext.lower()
                
                # Skip already minified files
                if '.min.' in filename:
                    skipped += 1
                    continue
                
                # Process files with matching extensions
                if file_ext in extensions_to_process:
                    minifier = self.minifier_registry.get_minifier_for_extension(file_ext)
                    
                    if minifier:
                        job = MinificationJob(file_path, minifier, self.file_processor, suffix)
                        
                        try:
                            if job.execute():
                                processed += 1
                        except Exception:
                            # Error already logged in MinificationJob.execute()
                            pass
        
        print(f"✅ Minification complete! Processed {processed} files, skipped {skipped} already minified files.")
        return processed, skipped
    
    def delete_minified_files(self, root_dir: str, suffix: str = ".min", 
                            extensions: Optional[List[str]] = None) -> int:
        """
        Delete all minified files in a project.
        
        Args:
            root_dir (str): The root directory of the project.
            suffix (str): Suffix of minified files.
            extensions (Optional[List[str]]): List of extensions to delete (e.g., ['.py', '.js']).
            
        Returns:
            int: The number of deleted files.
        """
        count = 0
        
        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                _, file_ext = os.path.splitext(filename)
                file_ext = file_ext.lower()
                
                # Check if file is a minified file (contains the suffix)
                if suffix in filename:
                    # If extensions are specified, check if file matches any of them
                    if extensions is None or file_ext in extensions:
                        try:
                            self.file_processor.delete_file(file_path)
                            count += 1
                            print(f"🗑️ Deleted: {file_path}")
                        except Exception as e:
                            print(f"❌ Error deleting {file_path}: {e}")
        
        if count > 0:
            print(f"✅ {count} minified files have been deleted.")
        else:
            print("ℹ️ No minified files found.")
            
        return count
    
    def _get_extensions_to_process(self, languages: Optional[List[str]], 
                                  extensions: Optional[List[str]]) -> Set[str]:
        """
        Determine which extensions to process.
        
        Args:
            languages (Optional[List[str]]): List of languages to process (e.g., ['python', 'javascript']).
            extensions (Optional[List[str]]): List of custom extensions to process.
            
        Returns:
            Set[str]: Set of extensions to process.
        """
        extensions_to_process: Set[str] = set()
        
        # Add file types if specified
        if languages:
            for file_type in languages:
                minifier = self.minifier_registry.get_minifier_by_name(file_type)
                if minifier:
                    extensions_to_process.update(minifier.file_extensions)
        
        # Add extensions if provided
        if extensions:
            for ext in extensions:
                if not ext.startswith('.'):
                    ext = f'.{ext}'
                extensions_to_process.add(ext.lower())
        
        # If no file types are specified, use all supported extensions
        if not extensions_to_process:
            extensions_to_process = set(self.minifier_registry.get_supported_extensions())
        
        return extensions_to_process
