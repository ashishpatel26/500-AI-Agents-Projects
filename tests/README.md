# Test Suite for 500-AI-Agents-Projects

This directory contains comprehensive tests for validating the repository's documentation, configuration, and content.

## Test Categories

### Markdown Validation (`test_markdown_validation.py`)

- Structure and formatting
- Content quality
- URL formatting
- Consistency checks
- Table structure
- Documentation completeness

### YAML Validation (`test_yaml_validation.py`)

- GitHub Actions workflow validation
- YAML syntax and structure
- Security checks
- Configuration validation

### Link Validation (`test_link_validation.py`)

- Link format verification
- GitHub URL validation
- Image reference validation
- Internal link validation

### Content Validation (`test_content_validation.py`)

- License file validation
- Repository structure
- Content quality
- Code examples
- Mermaid diagrams
- File encoding

## Running Tests

Install dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_markdown_validation.py
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Test Philosophy

These tests focus on validation rather than behavior testing since the repository primarily contains documentation and configuration files. They ensure:

1. **Quality**: Documentation is well-formed and complete
2. **Consistency**: Formatting and structure are consistent
3. **Validity**: Links work and configurations are correct
4. **Completeness**: All required files and sections exist