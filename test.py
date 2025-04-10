from minifykit.core.languages import PythonMinifier
from minifykit.file.processor import FileProcessor
from minifykit.file.job import MinificationJob

# Create a file processor and a minifier
file_processor = FileProcessor()
minifier = PythonMinifier()

# Create and execute a minification job
job = MinificationJob("my.py", minifier, file_processor)
job.execute()