# Testing Guide for 500-AI-Agents-Projects

Comprehensive testing documentation for the repository validation suite.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## Test Organization

### Test Files (44 total tests)

- `test_github_workflow.py` - GitHub Actions workflow validation (14 tests)
- `test_markdown_files.py` - Markdown documentation validation (7 tests)
- `test_license.py` - LICENSE file validation (7 tests)
- `test_images.py` - Image file validation (7 tests)
- `test_integration.py` - Integration tests (9 tests)

## Running Specific Tests

```bash
# Run specific test file
pytest tests/test_markdown_files.py -v

# Run specific test class
pytest tests/test_license.py::TestLicense -v

# Run specific test method
pytest tests/test_license.py::TestLicense::test_license_is_mit -v
```

## Test Coverage

- ✅ GitHub Actions workflow configuration.
- ✅ Markdown structure and formatting.
- ✅ MIT License compliance.
- ✅ Image validation and references.
- ✅ Repository structure.
- ✅ Documentation quality.
- ✅ Cross-file consistency.

## For Contributors

When adding new files:

1. Add appropriate validation tests.
2. Run full test suite locally.
3. Ensure all tests pass before committing.

See `tests/README.md` for detailed test documentation.