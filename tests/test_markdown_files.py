"""Tests for Markdown documentation files."""

import os
import re
import pytest


class TestMarkdownFiles:
    """Test suite for Markdown file validation."""
    
    @pytest.fixture(params=['README.md', 'CONTRIBUTION.md', 'crewai_mcp_course/README.md'])
    def markdown_file(self, request):
        return request.param
    
    def test_markdown_file_exists(self, markdown_file):
        assert os.path.exists(markdown_file), f"File not found: {markdown_file}"
    
    def test_markdown_file_not_empty(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert len(content.strip()) > 0
    
    def test_markdown_has_title(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        h1_pattern = r'^#\s+.+$'
        matches = re.findall(h1_pattern, content, re.MULTILINE)
        assert len(matches) > 0, f"{markdown_file} should have H1 heading"
    
    def test_markdown_code_blocks_closed(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        fence_pattern = r'^```'
        fences = re.findall(fence_pattern, content, re.MULTILINE)
        assert len(fences) % 2 == 0, f"{markdown_file} has unclosed code blocks"


class TestReadmeSpecific:
    """Specific tests for README.md."""
    
    def test_readme_has_table_of_contents(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'Table of Contents' in content
    
    def test_readme_has_use_case_table(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        table_pattern = r'\|.*\|.*\|'
        matches = re.findall(table_pattern, content)
        assert len(matches) > 3, "README should contain tables"
    
    def test_readme_has_github_links(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'github.com' in content.lower()