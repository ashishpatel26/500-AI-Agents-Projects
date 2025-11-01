"""Markdown formatting and quality tests."""
import re
import pytest
from pathlib import Path


class TestMarkdownFormatting:
    """Test markdown structure and formatting."""
    
    def test_heading_hierarchy(self):
        """Test proper heading hierarchy."""
        content = Path("README.md").read_text(encoding='utf-8')
        lines = content.split('\n')
        headings = [line for line in lines if line.strip().startswith('#')]
        
        prev_level = 0
        for heading in headings:
            level = len(heading) - len(heading.lstrip('#'))
            if level > prev_level:
                assert level <= prev_level + 1, \
                    f"Skipped heading level: {prev_level} to {level}"
            prev_level = level
    
    def test_code_blocks_formatted(self):
        """Test code blocks have language specifiers."""
        content = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        code_blocks = re.findall(r'```(\w*)\n', content)
        assert len(code_blocks) > 0, "Should have code blocks"
        
        # Most should have language
        with_lang = [b for b in code_blocks if b]
        ratio = len(with_lang) / len(code_blocks) if code_blocks else 0
        assert ratio > 0.5, f"Most code blocks should specify language: {ratio:.0%}"
    
    def test_lists_consistent(self):
        """Test list formatting is consistent."""
        content = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        lines = content.split('\n')
        
        list_items = [line for line in lines if re.match(r'^\s*[-*]\s', line)]
        assert len(list_items) > 0, "Should have list items"
    
    def test_no_trailing_whitespace(self):
        """Test lines don't have trailing whitespace."""
        for file_path in ['README.md', 'CONTRIBUTION.md', 'LICENSE']:
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                if line.strip():  # Ignore empty lines
                    assert not line.rstrip() != line or line == '\n', \
                        f"{file_path}:{i} has trailing whitespace"


class TestTableFormatting:
    """Test markdown table structure."""
    
    def test_tables_have_separators(self):
        """Tables should have proper header separators."""
        content = Path("README.md").read_text(encoding='utf-8')
        lines = content.split('\n')
        
        in_table = False
        for i, line in enumerate(lines):
            if '|' in line and line.count('|') > 2:
                if not in_table:
                    in_table = True
                    # Next line should be separator
                    if i + 1 < len(lines):
                        sep = lines[i + 1]
                        if '|' in sep:
                            assert re.search(r'[-:]+', sep), "Need separator row"
            elif in_table and not line.strip():
                in_table = False
    
    def test_use_case_table_columns(self):
        """Main use case table has required columns."""
        content = Path("README.md").read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Find main table
        for _i, line in enumerate(lines):
            if '| Use Case' in line and '| Industry' in line:
                assert 'Description' in line
                assert 'GitHub' in line or 'Code' in line
                break


class TestContentQuality:
    """Test content quality and consistency."""
    
    def test_no_placeholder_text(self):
        """No TODO or placeholder text."""
        for file_path in ['README.md', 'CONTRIBUTION.md']:
            content = Path(file_path).read_text(encoding='utf-8')
            
            placeholders = ['TODO:', 'FIXME:', 'XXX:', 'lorem ipsum']
            for placeholder in placeholders:
                assert placeholder not in content.lower(), \
                    f"{file_path} has placeholder: {placeholder}"
    
    def test_consistent_terminology(self):
        """Terminology used consistently."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Should use "AI agent" consistently
        ai_mentions = len(re.findall(r'\bAI [Aa]gent', content))
        assert ai_mentions > 5, "Should mention 'AI agent' frequently"
    
    def test_proper_capitalization(self):
        """Proper nouns capitalized correctly."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Check some key proper nouns
        assert re.search(r'\bGitHub\b', content), "Use 'GitHub' not 'github'"
        assert re.search(r'\bPython\b', content), "Use 'Python' not 'python'"
    
    def test_files_utf8_encoded(self):
        """All text files use UTF-8."""
        for file_path in ['README.md', 'CONTRIBUTION.md', 'LICENSE']:
            try:
                Path(file_path).read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"{file_path} not UTF-8 encoded")


class TestMermaidDiagrams:
    """Test Mermaid diagram syntax."""
    
    def test_mermaid_present(self):
        """CrewAI course has Mermaid diagrams."""
        content = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        diagrams = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
        assert len(diagrams) >= 3, "Should have 3+ Mermaid diagrams"
    
    def test_mermaid_syntax(self):
        """Mermaid diagrams have valid basic syntax."""
        content = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        diagrams = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
        
        for diagram in diagrams:
            # Should start with graph type
            assert any(diagram.strip().startswith(t) 
                      for t in ['graph', 'flowchart', 'sequenceDiagram']), \
                "Mermaid needs graph type"
            
            # Should have connections
            assert '-->' in diagram or '---' in diagram, \
                "Mermaid needs connections"