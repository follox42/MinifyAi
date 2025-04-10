from typing import Dict, List, Optional
from ..core.languages import LanguageMinifier

class MinifierRegistry:
    """
    Registry for language minifiers.
    """
    
    def __init__(self):
        """Initialize the minifier registry."""
        self._minifiers: Dict[str, LanguageMinifier] = {}
        self._extension_map: Dict[str, LanguageMinifier] = {}
    
    def register_minifier(self, minifier: LanguageMinifier) -> None:
        """
        Register a minifier.
        
        Args:
            minifier (LanguageMinifier): The minifier to register.
        """
        self._minifiers[minifier.name.lower()] = minifier
        
        for ext in minifier.file_extensions:
            self._extension_map[ext.lower()] = minifier
    
    def get_minifier_by_name(self, name: str) -> Optional[LanguageMinifier]:
        """
        Get a minifier by name.
        
        Args:
            name (str): The name of the minifier.
            
        Returns:
            Optional[LanguageMinifier]: The minifier, or None if not found.
        """
        return self._minifiers.get(name.lower())
    
    def get_minifier_for_extension(self, extension: str) -> Optional[LanguageMinifier]:
        """
        Get the minifier for a file extension.
        
        Args:
            extension (str): The file extension (with dot).
            
        Returns:
            Optional[LanguageMinifier]: The minifier for the extension, or None if not found.
        """
        if not extension.startswith('.'):
            extension = f".{extension}"
        return self._extension_map.get(extension.lower())
    
    def get_supported_extensions(self) -> List[str]:
        """
        Get all supported file extensions.
        
        Returns:
            List[str]: List of all supported file extensions.
        """
        return list(self._extension_map.keys())
    
    def get_all_minifiers(self) -> List[LanguageMinifier]:
        """
        Get all registered minifiers.
        
        Returns:
            List[LanguageMinifier]: List of all minifiers.
        """
        return list(self._minifiers.values())