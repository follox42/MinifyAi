# Contributing to MinifyKit

We're excited that you're interested in contributing to MinifyKit! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug:

1. First check if the bug has already been reported in the [GitHub issues](https://github.com/your-username/minifykit/issues).
2. If the bug hasn't been reported yet, [create a new issue](https://github.com/your-username/minifykit/issues/new).
3. Clearly describe the problem, including steps to reproduce the bug and expected behavior.
4. If possible, include a minimal code example that reproduces the issue.

### Suggesting Enhancements

To suggest an enhancement:

1. Check if the enhancement has already been suggested in the [GitHub issues](https://github.com/your-username/minifykit/issues).
2. If the enhancement hasn't been suggested yet, [create a new issue](https://github.com/your-username/minifykit/issues/new).
3. Clearly describe the enhancement, its use case, and why it would be beneficial for the project.

### Submitting Code

To contribute code:

1. Fork the repository on GitHub.
2. Create a branch for your feature or fix (`git checkout -b feature/feature-name` or `git checkout -b fix/fix-name`).
3. Write your code, following the project's style conventions.
4. Add tests for your code.
5. Make sure all tests pass.
6. Update documentation if necessary.
7. Submit a Pull Request.

## Style Conventions

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- Use docstrings in [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) format.
- Make sure your code passes linting checks with `flake8` and `black`.

### Tests

- Write unit tests for your code using `pytest`.
- Aim for a code coverage of at least 80%.

### Commit Messages

- Use a clear and descriptive message.
- Start with a verb in the imperative (e.g., "Add", "Fix", "Update").
- Reference relevant issues when appropriate.

## Development Process

1. Create an issue to discuss the feature or bug before you start coding.
2. Wait for feedback from the maintainers.
3. Develop your feature or fix in a separate branch.
4. Submit a Pull Request.
5. Wait for code review and feedback.
6. Make requested changes if necessary.

## Setting Up the Development Environment

1. Clone the repository to your local machine.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install development dependencies: `pip install -e ".[dev]"`
5. Install development tools: `pip install pytest flake8 black`

## Running Tests

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=minifykit
```

Thank you for contributing to MinifyKit!
