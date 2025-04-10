# MinifyKit

MinifyKit is a flexible Python library designed to minify source code in different programming languages. Minification reduces file size by removing spaces, comments, and other non-essential characters while preserving code functionality.

## Features

- Extensible and modular architecture
- Support for multiple programming languages
- Customizable minification actions
- Batch processing of files and entire projects
- Support for minification profiles

## Installation

```bash
pip install minifykit
```

## Quick Usage

### Minifying a Single File

```python
from minifykit.core.languages import PythonMinifier
from minifykit.file.processor import FileProcessor
from minifykit.file.job import MinificationJob

# Create a file processor and a minifier
file_processor = FileProcessor()
minifier = PythonMinifier()

# Create and execute a minification job
job = MinificationJob("my_script.py", minifier, file_processor)
job.execute()
```

### Minifying an Entire Project

```python
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
project_minifier.minify_project("./my_project", languages=["python", "javascript"])
```

### Clear the Entire Project

```python
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

# Clear the entire project exactly as it minify it. Or you can specify the extensions like this project_minifier.delete_minified_files(extensions=[".py", ".js"])
project_minifier.delete_minified_files()
```

## Architecture

MinifyKit follows several design principles:

1. **Single Responsibility Principle**: Each class has a single responsibility.
2. **Open/Closed Principle**: Code is open for extension but closed for modification.
3. **Dependency Inversion**: Code depends on abstractions, not concrete implementations.
4. **Strategy Pattern**: Minification strategies are interchangeable.
5. **Composite Pattern**: Minification actions can be composed.
6. **Factory Pattern**: Creating minification actions through a factory.

## Adding a New Language

To add support for a new language:

1. Create a class that inherits from `LanguageMinifier`
2. Define appropriate regex patterns for comments and other elements
3. Configure minification actions for the language
4. Register the minifier in the registry

## Contributing

Contributions are welcome! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
