"""Comprehensive documentation validation tests."""
import re
import pytest
from pathlib import Path


class TestREADME:
    """Test README.md structure and content."""
    
    def test_readme_exists(self):
        assert Path("README.md").exists()
    
    def test_readme_has_title(self):
        content = Path("README.md").read_text(encoding='utf-8')
        assert content.startswith('#')
        assert '500' in content[:100] or 'AI Agent' in content[:100]
    
    def test_readme_has_toc(self):
        content = Path("README.md").read_text(encoding='utf-8')
        assert 'Table of Contents' in content
        assert '[Introduction]' in content
    
    def test_readme_has_license_section(self):
        content = Path("README.md").read_text(encoding='utf-8')
        assert 'License' in content
        assert 'MIT' in content
    
    def test_images_exist(self):
        content = Path("README.md").read_text(encoding='utf-8')
        images = re.findall(r'!\[.*?\]\((images/[^\)]+)\)', content)
        for img in images:
            assert Path(img).exists(), f"Missing: {img}"
    
    def test_github_urls_valid(self):
        content = Path("README.md").read_text(encoding='utf-8')
        urls = re.findall(r'https://github\.com/[^\s\)]+', content)
        assert len(urls) > 50, "Should have many GitHub URLs"
        for url in urls:
            assert not url.endswith('.'), f"Trailing period: {url}"


class TestContribution:
    """Test CONTRIBUTION.md content."""
    
    def test_contribution_exists(self):
        assert Path("CONTRIBUTION.md").exists()
    
    def test_has_requirements_section(self):
        content = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        assert 'Project folder requirements' in content
        assert 'README.md' in content
    
    def test_has_pr_process(self):
        content = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        assert 'PR process' in content or 'pull request' in content.lower()
    
    def test_no_merge_conflicts(self):
        content = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        assert '<<<<<<<' not in content
        assert '>>>>>>>' not in content


class TestCrewAICourse:
    """Test CrewAI course documentation."""
    
    def test_course_readme_exists(self):
        assert Path("crewai_mcp_course/README.md").exists()
    
    def test_has_lessons(self):
        content = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        assert 'Lesson 1' in content
        assert 'Lesson 2' in content
        assert 'Lesson 3' in content
    
    def test_has_mermaid_diagrams(self):
        content = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        assert '```mermaid' in content
        assert content.count('```mermaid') >= 3


class TestWorkflow:
    """Test GitHub Actions workflow."""
    
    def test_workflow_exists(self):
        assert Path(".github/workflows/jekyll-gh-pages.yml").exists()
    
    def test_workflow_valid_yaml(self):
        import yaml
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        data = yaml.safe_load(content)
        assert data is not None
        assert 'jobs' in data
        assert 'name' in data
    
    def test_workflow_has_build_job(self):
        import yaml
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        data = yaml.safe_load(content)
        assert 'build' in data['jobs']
        assert 'steps' in data['jobs']['build']


class TestLicense:
    """Test LICENSE file."""
    
    def test_license_exists(self):
        assert Path("LICENSE").exists()
    
    def test_is_mit_license(self):
        content = Path("LICENSE").read_text(encoding='utf-8')
        assert 'MIT License' in content
        assert 'Permission is hereby granted' in content
        assert '2025' in content or '2024' in content