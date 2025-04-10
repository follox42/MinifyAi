"""
MinifyKit - A library for minifying source code files.
"""

__version__ = "0.1.0"
__author__ = "Follox"
__email__ = "Follox@Shosai.fr"

# Import convenient modules and classes
from .core.languages import (
    LanguageMinifier,
    PythonMinifier,
    JavaScriptMinifier,
    CSSMinifier,
    HTMLMinifier
)
from .file.processor import FileProcessor
from .file.job import MinificationJob
from .project.minify import ProjectMinifier
from .project.registry import MinifierRegistry

# Make version info available
VERSION = __version__