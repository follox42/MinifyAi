from minifykit.project.minify import ProjectMinifier
from minifykit.project.registry import MinifierRegistry
from minifykit.file.processor import FileProcessor
from minifykit.core.languages import PythonMinifier, JavaScriptMinifier

# Create a minifier registry and register language minifiers
registry = MinifierRegistry()
registry.register_minifier(PythonMinifier())
registry.register_minifier(JavaScriptMinifier())

# Create a file processor
file_processor = FileProcessor()

# Create a project minifier
project_minifier = ProjectMinifier(registry, file_processor)

# Minify an entire project
project_minifier.delete_minified_files(extensions=[".py", ".js"])