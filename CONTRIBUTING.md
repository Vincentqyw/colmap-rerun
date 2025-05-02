# Contributing Guidelines

We welcome contributions from the community. Please follow these guidelines when contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Development Workflow

1. Create a new branch for your feature/bugfix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the project's coding standards

3. Run tests:
```bash
pytest
```

4. Format your code:
```bash
black .
```

5. Commit your changes with a descriptive message

6. Push to your fork and open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep docstrings up-to-date
- Format code with Black

## Pull Request Guidelines

- Include a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep changes focused on a single purpose

## Reporting Issues

When reporting issues, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
