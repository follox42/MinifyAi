from minifykit.project.minify import ProjectMinifier
from minifykit.project.registry import MinifierRegistry
from minifykit.file.processor import FileProcessor
from minifykit.core.languages import PythonMinifier, JavaScriptMinifier
registry = MinifierRegistry()
registry.register_minifier(PythonMinifier())
registry.register_minifier(JavaScriptMinifier())
file_processor = FileProcessor()
project_minifier = ProjectMinifier(registry, file_processor)
project_minifier.minify_project("./my_project", languages=["python", "javascript"])