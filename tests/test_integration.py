"""Integration tests for repository structure."""

import os
import re
import pytest


class TestRepositoryStructure:
    """Test overall repository structure."""
    
    def test_all_required_files_exist(self):
        required_files = [
            'README.md',
            'LICENSE',
            'CONTRIBUTION.md',
            '.github/workflows/jekyll-gh-pages.yml'
        ]
        for file_path in required_files:
            assert os.path.exists(file_path), f"Missing: {file_path}"
    
    def test_required_directories_exist(self):
        required_dirs = [
            'images',
            '.github',
            '.github/workflows',
            'crewai_mcp_course'
        ]
        for dir_path in required_dirs:
            assert os.path.exists(dir_path), f"Missing: {dir_path}"
            assert os.path.isdir(dir_path), f"Not a directory: {dir_path}"
    
    def test_readme_links_to_contribution_guide(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        assert 'CONTRIBUT' in readme.upper() or 'Contributing' in readme
    
    def test_readme_links_to_license(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        assert 'LICENSE' in readme or 'MIT' in readme


class TestDocumentationQuality:
    """Test documentation quality."""
    
    def test_readme_has_badges(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        badge_pattern = r'!\[.*\]\(https://.*badge.*\)'
        matches = re.findall(badge_pattern, readme, re.IGNORECASE)
        assert len(matches) > 0
    
    def test_readme_has_emojis(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        emoji_patterns = [r'🌟', r'📋', r'🧠', r'🤖', r'💻']
        found = any(re.search(p, readme) for p in emoji_patterns)
        assert found
    
    def test_contribution_guide_has_examples(self):
        with open('CONTRIBUTION.md', 'r', encoding='utf-8') as f:
            content = f.read()
        assert '```' in content
    
    def test_course_readme_has_code_examples(self):
        with open('crewai_mcp_course/README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        code_blocks = content.count('```')
        assert code_blocks >= 4


class TestConsistency:
    """Test consistency across documentation."""
    
    def test_consistent_license_references(self):
        for doc_file in ['README.md', 'CONTRIBUTION.md']:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            assert 'license' in content or 'mit' in content