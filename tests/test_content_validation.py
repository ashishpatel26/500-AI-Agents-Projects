"""
Tests for validating content quality and consistency.
"""
import re
import pytest
from pathlib import Path


class TestLicenseFile:
    """Test the LICENSE file."""
    
    @pytest.fixture
    def license_content(self):
        """Load LICENSE file content."""
        license_path = Path("LICENSE")
        assert license_path.exists(), "LICENSE file should exist"
        return license_path.read_text(encoding='utf-8')
    
    def test_license_is_mit(self, license_content):
        """Test that license is MIT License."""
        assert 'MIT License' in license_content
        assert 'Permission is hereby granted, free of charge' in license_content
    
    def test_license_has_copyright(self, license_content):
        """Test that license includes copyright notice."""
        assert 'Copyright' in license_content
        assert '2025' in license_content or '2024' in license_content
    
    def test_license_has_full_text(self, license_content):
        """Test that license includes full MIT license text."""
        required_phrases = [
            'Permission is hereby granted',
            'THE SOFTWARE IS PROVIDED "AS IS"',
            'WITHOUT WARRANTY OF ANY KIND',
            'IN NO EVENT SHALL',
        ]
        
        for phrase in required_phrases:
            assert phrase in license_content, f"License should contain: {phrase}"


class TestRepositoryStructure:
    """Test repository file structure."""
    
    def test_required_files_exist(self):
        """Test that all required files exist."""
        required_files = [
            'README.md',
            'LICENSE',
            'CONTRIBUTION.md',
            '.github/workflows/jekyll-gh-pages.yml',
            'crewai_mcp_course/README.md',
        ]
        
        for file_path in required_files:
            path = Path(file_path)
            assert path.exists(), f"Required file not found: {file_path}"
    
    def test_images_directory_exists(self):
        """Test that images directory exists with files."""
        images_dir = Path("images")
        assert images_dir.exists()
        assert images_dir.is_dir()
        
        # Should have image files
        image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
        assert len(image_files) > 0, "Should have image files in images directory"
    
    def test_github_workflows_directory_structure(self):
        """Test GitHub workflows directory structure."""
        workflows_dir = Path(".github/workflows")
        assert workflows_dir.exists()
        assert workflows_dir.is_dir()
        
        # Should have at least one workflow
        workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
        assert len(workflow_files) > 0, "Should have workflow files"


class TestContentQuality:
    """Test content quality and consistency."""
    
    def test_no_lorem_ipsum_placeholder_text(self):
        """Test that there's no placeholder Lorem Ipsum text."""
        readme = Path("README.md").read_text(encoding='utf-8')
        contrib = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        
        placeholder_patterns = [
            'lorem ipsum',
            'TODO:',
            'FIXME:',
            'XXX:',
            'placeholder',
        ]
        
        for pattern in placeholder_patterns:
            assert pattern.lower() not in readme.lower(), \
                f"README contains placeholder: {pattern}"
            assert pattern.lower() not in contrib.lower(), \
                f"CONTRIBUTION.md contains placeholder: {pattern}"
    
    def test_consistent_terminology(self):
        """Test that terminology is used consistently."""
        readme = Path("README.md").read_text(encoding='utf-8')
        
        # Check that "AI agent" is used consistently
        ai_agent_count = len(re.findall(r'\bAI [Aa]gent', readme))
        assert ai_agent_count > 5, "Should consistently use 'AI agent' terminology"
    
    def test_proper_capitalization(self):
        """Test that proper nouns are capitalized correctly."""
        readme = Path("README.md").read_text(encoding='utf-8')
        
        proper_nouns = {
            'CrewAI': re.compile(r'\bCrewAI\b'),
            'GitHub': re.compile(r'\bGitHub\b'),
            'Python': re.compile(r'\bPython\b'),
        }
        
        for noun, pattern in proper_nouns.items():
            matches = pattern.findall(readme)
            if matches:
                # Check that it's not lowercase
                incorrect = [m for m in matches if m != noun]
                assert len(incorrect) == 0, \
                    f"Inconsistent capitalization of {noun}: found {incorrect}"


class TestCodeExamples:
    """Test code examples in documentation."""
    
    def test_code_blocks_have_language_specifiers(self):
        """Test that code blocks specify their language."""
        crewai = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        # Find code blocks
        code_blocks = re.findall(r'```(\w*)\n', crewai)
        
        # Most should have language specified
        specified = [lang for lang in code_blocks if lang]
        total = len(code_blocks)
        
        if total > 0:
            ratio = len(specified) / total
            assert ratio > 0.7, f"Most code blocks should have language: {ratio:.1%}"
    
    def test_bash_commands_are_valid(self):
        """Test that bash command examples look valid."""
        crewai = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        # Find bash code blocks
        bash_blocks = re.findall(r'```bash\n(.*?)\n```', crewai, re.DOTALL)
        
        for block in bash_blocks:
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Should be a valid command
                    assert not line.startswith('$'), \
                        "Don't include $ prompt in code examples"


class TestMermaidDiagrams:
    """Test Mermaid diagrams in documentation."""
    
    def test_mermaid_diagrams_are_valid_syntax(self):
        """Test that Mermaid diagrams have valid syntax."""
        crewai = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        # Find mermaid blocks
        mermaid_blocks = re.findall(r'```mermaid\n(.*?)\n```', crewai, re.DOTALL)
        
        assert len(mermaid_blocks) >= 3, "Should have multiple Mermaid diagrams"
        
        for block in mermaid_blocks:
            # Should start with graph type
            assert any(block.strip().startswith(t) for t in ['graph', 'flowchart', 'sequenceDiagram']), \
                "Mermaid diagram should start with graph type"
            
            # Should have connections (arrows)
            assert '-->' in block or '---' in block, \
                "Mermaid diagram should have connections"


class TestContributionGuidelines:
    """Test contribution guidelines content."""
    
    def test_contribution_has_pr_checklist(self):
        """Test that contribution guidelines include PR checklist."""
        contrib = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        
        assert 'checklist' in contrib.lower()
        assert '[ ]' in contrib or '- [ ]' in contrib, \
            "Should have checkbox items in checklist"
    
    def test_contribution_mentions_testing(self):
        """Test that contribution guidelines mention testing."""
        contrib = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        
        testing_keywords = ['test', 'testing', 'smoke test', 'unit test']
        assert any(keyword in contrib.lower() for keyword in testing_keywords), \
            "Contribution guidelines should mention testing"
    
    def test_contribution_has_code_of_conduct_reference(self):
        """Test that contribution guidelines reference code of conduct."""
        contrib = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        
        assert 'code of conduct' in contrib.lower(), \
            "Should reference Code of Conduct"


class TestFileEncoding:
    """Test file encoding and formatting."""
    
    def test_files_use_utf8_encoding(self):
        """Test that text files use UTF-8 encoding."""
        text_files = [
            'README.md',
            'CONTRIBUTION.md',
            'LICENSE',
            'crewai_mcp_course/README.md',
        ]
        
        for file_path in text_files:
            path = Path(file_path)
            # Try to read as UTF-8
            try:
                content = path.read_text(encoding='utf-8')
                assert content is not None
            except UnicodeDecodeError:
                pytest.fail(f"File {file_path} is not valid UTF-8")
    
    def test_files_have_final_newline(self):
        """Test that text files end with a newline."""
        text_files = [
            'README.md',
            'CONTRIBUTION.md',
            'LICENSE',
        ]
        
        for file_path in text_files:
            content = Path(file_path).read_text(encoding='utf-8')
            assert content.endswith('\n'), f"File {file_path} should end with newline"