#!/usr/bin/env python3
"""
Command-line interface for MinifyKit.

Usage:
    minifykit_cli.py minify [--languages=<langs>] [--extensions=<exts>] [--suffix=<suffix>] <directory>
    minifykit_cli.py clean [--extensions=<exts>] [--suffix=<suffix>] <directory>
    minifykit_cli.py list-languages
    minifykit_cli.py (-h | --help)
    minifykit_cli.py --version

Options:
    -h --help               Show this help message and exit.
    --version               Show version.
    --languages=<langs>     Comma-separated list of languages to process [default: all].
    --extensions=<exts>     Comma-separated list of file extensions to process [default: all].
    --suffix=<suffix>       Suffix to add to minified files [default: .min].
    <directory>             Directory to process.
"""

import sys
import os
from docopt import docopt

from minifykit import VERSION
from minifykit.project.minify import ProjectMinifier
from minifykit.project.registry import MinifierRegistry
from minifykit.file.processor import FileProcessor
from minifykit.core.languages import PythonMinifier, JavaScriptMinifier, CSSMinifier, HTMLMinifier


def setup_registry():
    """Set up the minifier registry with all available minifiers."""
    registry = MinifierRegistry()
    registry.register_minifier(PythonMinifier())
    registry.register_minifier(JavaScriptMinifier())
    registry.register_minifier(CSSMinifier())
    registry.register_minifier(HTMLMinifier())
    return registry


def parse_list_option(option):
    """Parse a comma-separated list option."""
    if option == "all":
        return None
    return [item.strip() for item in option.split(',')]


def main():
    """Run the MinifyKit CLI."""
    arguments = docopt(__doc__, version=f"MinifyKit {VERSION}")
    
    # Set up the registry and processor
    registry = setup_registry()
    processor = FileProcessor()
    
    # Create the project minifier
    project_minifier = ProjectMinifier(registry, processor)
    
    # Handle the list-languages command
    if arguments['list-languages']:
        print("Available languages:")
        for minifier in registry.get_all_minifiers():
            extensions = ', '.join(minifier.file_extensions)
            print(f"  - {minifier.name} ({extensions})")
        return 0
    
    # Parse common options
    directory = arguments['<directory>']
    
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return 1
    
    suffix = arguments['--suffix']
    extensions = parse_list_option(arguments['--extensions'])
    
    # Handle the minify command
    if arguments['minify']:
        languages = parse_list_option(arguments['--languages'])
        
        print(f"Minifying files in '{directory}'...")
        processed, skipped = project_minifier.minify_project(
            directory, 
            languages=languages, 
            extensions=extensions, 
            suffix=suffix
        )
        print(f"Done! Processed {processed} files, skipped {skipped} files.")
        return 0
    
    # Handle the clean command
    if arguments['clean']:
        print(f"Cleaning minified files in '{directory}'...")
        count = project_minifier.delete_minified_files(
            directory,
            suffix=suffix,
            extensions=extensions
        )
        print(f"Done! Deleted {count} minified files.")
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())