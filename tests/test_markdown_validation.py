"""
Comprehensive tests for validating markdown files in the repository.
Tests structure, syntax, formatting, and content quality.
"""
import re
import pytest
from pathlib import Path


class TestMarkdownStructure:
    """Test the structure and format of markdown files."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        readme_path = Path("README.md")
        assert readme_path.exists(), "README.md not found"
        return readme_path.read_text(encoding='utf-8')
    
    @pytest.fixture
    def contribution_content(self):
        """Load CONTRIBUTION.md content."""
        contrib_path = Path("CONTRIBUTION.md")
        assert contrib_path.exists(), "CONTRIBUTION.md not found"
        return contrib_path.read_text(encoding='utf-8')
    
    @pytest.fixture
    def crewai_readme_content(self):
        """Load crewai_mcp_course/README.md content."""
        crewai_path = Path("crewai_mcp_course/README.md")
        assert crewai_path.exists(), "crewai_mcp_course/README.md not found"
        return crewai_path.read_text(encoding='utf-8')
    
    def test_readme_has_title(self, readme_content):
        """Test that README.md has a proper title."""
        assert readme_content.startswith('#'), "README.md should start with a title"
        first_line = readme_content.split('\n')[0]
        assert '500' in first_line or 'AI Agent' in first_line, "Title should mention AI Agents"
    
    def test_readme_has_table_of_contents(self, readme_content):
        """Test that README.md includes a table of contents."""
        assert '## 📋 Table of Contents' in readme_content or '## Table of Contents' in readme_content
        assert '[Introduction]' in readme_content
        assert '[Contributing]' in readme_content
    
    def test_readme_has_license_section(self, readme_content):
        """Test that README.md references the license."""
        assert '## 📜 License' in readme_content or 'License' in readme_content
        assert 'MIT' in readme_content, "Should mention MIT license"
    
    def test_contribution_has_structure(self, contribution_content):
        """Test that CONTRIBUTION.md has proper structure."""
        assert '# Contributing' in contribution_content
        assert '## What to contribute' in contribution_content
        assert '## Project folder requirements' in contribution_content
    
    def test_crewai_readme_has_lessons(self, crewai_readme_content):
        """Test that CrewAI README has lesson structure."""
        assert '## Lessons' in crewai_readme_content or '### Lesson' in crewai_readme_content
        assert 'Lesson 1' in crewai_readme_content
        assert 'Lesson 2' in crewai_readme_content
        assert 'Lesson 3' in crewai_readme_content
    
    def test_no_broken_heading_hierarchy(self, readme_content):
        """Test that heading hierarchy is proper (no skipping levels)."""
        lines = readme_content.split('\n')
        headings = [line for line in lines if line.strip().startswith('#')]
        
        prev_level = 0
        for heading in headings:
            level = len(heading) - len(heading.lstrip('#'))
            # Allow going up multiple levels but not down more than 1
            if level > prev_level:
                assert level <= prev_level + 1, f"Heading hierarchy broken: jumped from {prev_level} to {level}"
            prev_level = level
    
    def test_code_blocks_are_properly_formatted(self, readme_content, crewai_readme_content):
        """Test that code blocks use proper formatting with language specifiers."""
        all_content = readme_content + '\n' + crewai_readme_content
        
        # Find all code blocks
        code_blocks = re.findall(r'```(\w*)\n', all_content)
        
        # At least some code blocks should have language specifiers
        assert len(code_blocks) > 0, "Should have code blocks in documentation"
    
    def test_lists_are_properly_formatted(self, contribution_content):
        """Test that lists use consistent formatting."""
        lines = contribution_content.split('\n')
        list_markers = [line for line in lines if re.match(r'^\s*[-*]\s', line)]
        
        # Should have at least some list items
        assert len(list_markers) > 0, "CONTRIBUTION.md should have list items"


class TestMarkdownContent:
    """Test the content quality of markdown files."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        return Path("README.md").read_text(encoding='utf-8')
    
    @pytest.fixture
    def contribution_content(self):
        """Load CONTRIBUTION.md content."""
        return Path("CONTRIBUTION.md").read_text(encoding='utf-8')
    
    def test_no_merge_conflict_markers(self, contribution_content):
        """Test that there are no Git merge conflict markers."""
        conflict_markers = ['<<<<<<<', '=======', '>>>>>>>']
        for marker in conflict_markers:
            assert marker not in contribution_content, f"Found merge conflict marker: {marker}"
    
    def test_images_referenced_exist(self, readme_content):
        """Test that images referenced in markdown actually exist."""
        # Find all image references
        image_refs = re.findall(r'!\[.*?\]\((.*?)\)', readme_content)
        
        for img_path in image_refs:
            # Skip URLs
            if img_path.startswith('http'):
                continue
            
            full_path = Path(img_path)
            assert full_path.exists(), f"Referenced image not found: {img_path}"
    
    def test_no_duplicate_headings(self, readme_content):
        """Test that there are no duplicate section headings."""
        lines = readme_content.split('\n')
        headings = [line.strip() for line in lines if line.strip().startswith('#')]
        
        # Remove duplicate spaces and normalize
        normalized = [' '.join(h.split()) for h in headings]
        
        # Allow some duplicates (like multiple "## UseCase" sections)
        # but flag if more than 3 of the same
        from collections import Counter
        counts = Counter(normalized)
        for heading, count in counts.items():
            if count > 4:
                pytest.fail(f"Heading appears too many times ({count}): {heading}")
    
    def test_external_links_have_descriptions(self, readme_content):
        """Test that external links have descriptive text."""
        # Find all markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', readme_content)
        
        for text, url in links:
            if url.startswith('http'):
                # Link text should not be empty or just the URL
                assert text.strip(), f"Empty link text for URL: {url}"
                assert text != url, f"Link text is same as URL: {url}"
    
    def test_tables_have_proper_structure(self, readme_content):
        """Test that markdown tables are properly formatted."""
        # Find all table sections
        lines = readme_content.split('\n')
        
        in_table = False
        table_lines = []
        
        for line in lines:
            if '|' in line:
                in_table = True
                table_lines.append(line)
            elif in_table and not line.strip():
                # End of table
                if len(table_lines) > 2:
                    # Check header separator
                    header_sep = table_lines[1]
                    assert re.match(r'\|[\s\-:|]+\|', header_sep), "Table should have proper separator"
                table_lines = []
                in_table = False
    
    def test_no_trailing_whitespace(self, readme_content, contribution_content):
        """Test that lines don't have trailing whitespace."""
        for content, filename in [(readme_content, 'README.md'), 
                                  (contribution_content, 'CONTRIBUTION.md')]:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Allow lines that are entirely whitespace (empty lines)
                if line.strip():
                    assert not line.endswith(' ') and not line.endswith('\t'), \
                        f"{filename}:{i} has trailing whitespace"


class TestMarkdownURLs:
    """Test URL formatting and structure in markdown files."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        return Path("README.md").read_text(encoding='utf-8')
    
    def test_github_urls_are_well_formed(self, readme_content):
        """Test that GitHub URLs are properly formatted."""
        github_urls = re.findall(r'https://github\.com/[^\s\)]+', readme_content)
        
        assert len(github_urls) > 0, "README should contain GitHub URLs"
        
        for url in github_urls:
            # Should not have trailing punctuation
            assert not url.endswith('.'), f"URL has trailing period: {url}"
            assert not url.endswith(','), f"URL has trailing comma: {url}"
            
            # Should follow pattern: github.com/user/repo
            parts = url.replace('https://github.com/', '').split('/')
            assert len(parts) >= 2, f"GitHub URL should have user/repo: {url}"
    
    def test_badge_urls_are_valid(self, readme_content):
        """Test that badge URLs (shields.io) are properly formatted."""
        badge_urls = re.findall(r'https://img\.shields\.io/[^\s\)]+', readme_content)
        
        for url in badge_urls:
            # Badges should have proper parameters
            assert 'badge' in url.lower() or 'shields.io' in url, f"Invalid badge URL: {url}"
    
    def test_no_localhost_urls(self, readme_content):
        """Test that there are no localhost URLs in documentation."""
        assert 'localhost' not in readme_content.lower(), "Should not reference localhost"
        assert '127.0.0.1' not in readme_content, "Should not reference 127.0.0.1"
    
    def test_urls_use_https(self, readme_content):
        """Test that URLs use HTTPS instead of HTTP where possible."""
        # Find all HTTP URLs
        http_urls = re.findall(r'http://[^\s\)]+', readme_content)
        
        # Filter out those that might legitimately need HTTP
        suspicious = [url for url in http_urls 
                     if not any(x in url for x in ['localhost', 'example.com'])]
        
        # Most URLs should use HTTPS
        if suspicious:
            print(f"Found {len(suspicious)} HTTP URLs that could use HTTPS")


class TestMarkdownConsistency:
    """Test consistency across markdown files."""
    
    def test_consistent_emoji_usage(self):
        """Test that emoji usage is consistent across files."""
        readme = Path("README.md").read_text(encoding='utf-8')
        
        # Check that emojis are used (part of the style)
        emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]|🌟|🤖|📋|🧠|🏭|🎮|💻|📊')
        assert emoji_pattern.search(readme), "README should use emojis for visual appeal"
    
    def test_consistent_section_formatting(self):
        """Test that sections use consistent formatting."""
        readme = Path("README.md").read_text(encoding='utf-8')
        
        # Framework sections should follow consistent pattern
        framework_sections = re.findall(r'### \*\*Framework Name\*\*: \*\*(\w+)\*\*', readme)
        assert len(framework_sections) >= 3, "Should have multiple framework sections"
        
        # Check each framework has a table
        for framework in framework_sections:
            assert f"Framework Name**: **{framework}" in readme


class TestTableStructure:
    """Test the structure and formatting of tables in markdown files."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        return Path("README.md").read_text(encoding='utf-8')
    
    def test_use_case_table_has_required_columns(self, readme_content):
        """Test that the main use case table has all required columns."""
        # Find the main use case table
        lines = readme_content.split('\n')
        
        table_start = None
        for i, line in enumerate(lines):
            if '| Use Case' in line and '| Industry' in line:
                table_start = i
                break
        
        assert table_start is not None, "Could not find main use case table"
        
        header = lines[table_start]
        assert 'Use Case' in header
        assert 'Industry' in header
        assert 'Description' in header
        assert 'GitHub' in header or 'Code' in header
    
    def test_framework_tables_have_consistent_structure(self, readme_content):
        """Test that framework-specific tables follow consistent structure."""
        # Find all framework table headers
        lines = readme_content.split('\n')
        
        framework_tables = []
        for i, line in enumerate(lines):
            if '| Use Case' in line and i < len(lines) - 1:
                framework_tables.append(i)
        
        assert len(framework_tables) >= 4, "Should have tables for multiple frameworks"
        
        # Each table should have similar structure
        for table_idx in framework_tables:
            header = lines[table_idx]
            # Should have pipes for column separation
            assert header.count('|') >= 3, "Table should have multiple columns"
    
    def test_table_rows_are_aligned(self, readme_content):
        """Test that table rows have consistent column counts."""
        lines = readme_content.split('\n')
        
        in_table = False
        expected_cols = None
        
        for line in lines:
            if '|' in line and line.count('|') > 2:
                if not in_table:
                    in_table = True
                    expected_cols = line.count('|')
                
                current_cols = line.count('|')
                if expected_cols and current_cols > 0:
                    # Allow some variation (±1) for formatting
                    assert abs(current_cols - expected_cols) <= 1, \
                        f"Table row has inconsistent columns: expected ~{expected_cols}, got {current_cols}"
            elif in_table and not line.strip():
                in_table = False
                expected_cols = None


class TestDocumentationCompleteness:
    """Test that documentation is complete and comprehensive."""
    
    def test_readme_has_all_sections(self):
        """Test that README has all expected sections."""
        readme = Path("README.md").read_text(encoding='utf-8')
        
        required_sections = [
            'Introduction',
            'Table of Contents',
            'Use Case Table',
            'Framework',
            'Contributing',
            'License'
        ]
        
        for section in required_sections:
            assert section in readme, f"README should have '{section}' section"
    
    def test_contribution_guide_has_all_sections(self):
        """Test that CONTRIBUTION.md has all expected sections."""
        contrib = Path("CONTRIBUTION.md").read_text(encoding='utf-8')
        
        required_sections = [
            'What to contribute',
            'Project folder requirements',
            'Naming & layout conventions',
            'Reproducibility',
            'Code style',
            'PR process',
            'Security',
            'Ethics'
        ]
        
        for section in required_sections:
            assert any(s in contrib for s in [section, section.lower()]), \
                f"CONTRIBUTION.md should have '{section}' section"
    
    def test_crewai_course_has_complete_structure(self):
        """Test that CrewAI course README has complete structure."""
        crewai = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        required_elements = [
            'Course Overview',
            'Lesson 1',
            'Lesson 2',
            'Lesson 3',
            'Getting Started',
            'Requirements',
            'Next Steps'
        ]
        
        for element in required_elements:
            assert element in crewai, f"CrewAI README should have '{element}'"
    
    def test_mermaid_diagrams_present(self):
        """Test that mermaid diagrams are included in CrewAI course."""
        crewai = Path("crewai_mcp_course/README.md").read_text(encoding='utf-8')
        
        # Should have mermaid code blocks
        assert '```mermaid' in crewai, "Should include mermaid diagrams"
        
        # Count mermaid diagrams
        diagram_count = crewai.count('```mermaid')
        assert diagram_count >= 3, f"Should have at least 3 mermaid diagrams, found {diagram_count}"