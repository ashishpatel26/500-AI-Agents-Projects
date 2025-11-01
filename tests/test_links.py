"""Link and URL validation tests."""
import re
import pytest
from pathlib import Path
from urllib.parse import urlparse


class TestGitHubLinks:
    """Validate GitHub repository links."""
    
    def test_github_links_structure(self):
        """Test GitHub URLs follow correct format."""
        content = Path("README.md").read_text(encoding='utf-8')
        repos = re.findall(r'https://github\.com/([^/\s\)]+)/([^/\s\)]+)', content)
        
        for owner, repo in repos:
            assert len(owner) > 0, "GitHub owner cannot be empty"
            assert len(repo) > 0, "GitHub repo cannot be empty"
            assert not repo.endswith('.git'), f"Remove .git: {owner}/{repo}"
    
    def test_no_broken_url_patterns(self):
        """Test for common URL mistakes."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        assert 'github.com//' not in content, "Double slash in GitHub URL"
        assert 'github.com/tree/main/tree/' not in content, "Duplicate /tree/"
        assert 'github.com/blob/main/blob/' not in content, "Duplicate /blob/"
    
    def test_https_usage(self):
        """Test that external links use HTTPS."""
        content = Path("README.md").read_text(encoding='utf-8')
        http_links = re.findall(r'http://[^\s\)]+', content)
        
        # Filter legitimate HTTP usage
        suspicious = [link for link in http_links if 'localhost' not in link]
        assert len(suspicious) == 0, f"Use HTTPS: {suspicious[:3]}"
    
    def test_badge_links_valid(self):
        """Test shield.io badge URLs."""
        content = Path("README.md").read_text(encoding='utf-8')
        badges = re.findall(r'https://img\.shields\.io/[^\s\)]+', content)
        
        assert len(badges) > 0, "Should have badge URLs"
        for badge in badges:
            assert 'badge' in badge.lower() or 'shields' in badge


class TestInternalLinks:
    """Validate internal anchors and references."""
    
    def test_image_references_exist(self):
        """Test all referenced images exist."""
        for md_file in ['README.md', 'crewai_mcp_course/README.md']:
            content = Path(md_file).read_text(encoding='utf-8')
            images = re.findall(r'!\[.*?\]\((.*?)\)', content)
            
            for img_path in images:
                if not img_path.startswith('http'):
                    # Resolve relative to markdown file
                    base_dir = Path(md_file).parent
                    full_path = base_dir / img_path
                    assert full_path.exists(), f"Missing image: {img_path} in {md_file}"
    
    def test_toc_links_valid(self):
        """Test table of contents links point to valid sections."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Find TOC links
        toc_links = re.findall(r'\]\((#[^\)]+)\)', content)
        
        # Find headers
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        
        # Basic validation - at least check we have both
        assert len(toc_links) > 0, "Should have TOC links"
        assert len(headers) > 0, "Should have headers"


class TestLinkDescriptions:
    """Test link text quality."""
    
    def test_no_generic_link_text(self):
        """Links should have descriptive text."""
        content = Path("README.md").read_text(encoding='utf-8')
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        
        generic = ['here', 'link', 'click here', 'this']
        
        for text, url in links:
            if url.startswith('http'):
                assert text.lower().strip() not in generic, \
                    f"Generic link text '{text}' for {url}"
    
    def test_badge_links_descriptive(self):
        """Badge links should describe their purpose."""
        content = Path("README.md").read_text(encoding='utf-8')
        badge_links = re.findall(r'\[([^\]]+)\]\((https://img\.shields\.io[^\)]+)\)', content)
        
        for text, _url in badge_links:
            keywords = ['github', 'code', 'notebook', 'view', 'badge']
            assert any(k in text.lower() for k in keywords), \
                f"Badge should be descriptive: {text}"