"""Tests for LICENSE file validation."""

import os
import re
import pytest


class TestLicense:
    """Test suite for LICENSE file validation."""
    
    def test_license_file_exists(self):
        assert os.path.exists("LICENSE")
    
    def test_license_not_empty(self):
        with open("LICENSE", 'r', encoding='utf-8') as f:
            content = f.read()
        assert len(content.strip()) > 0
    
    def test_license_is_mit(self):
        with open("LICENSE", 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'MIT License' in content
    
    def test_license_has_copyright(self):
        with open("LICENSE", 'r', encoding='utf-8') as f:
            content = f.read()
        copyright_pattern = r'Copyright \(c\) \d{4}'
        assert re.search(copyright_pattern, content)
    
    def test_license_has_permission_grant(self):
        with open("LICENSE", 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'Permission is hereby granted' in content
    
    def test_license_has_warranty_disclaimer(self):
        with open("LICENSE", 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'WITHOUT WARRANTY OF ANY KIND' in content
    
    def test_readme_mentions_license(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'MIT' in content or 'License' in content