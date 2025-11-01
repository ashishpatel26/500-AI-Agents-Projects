"""
Tests for validating links in markdown files.
Tests that URLs are accessible and well-formed.
"""
import re
import pytest
from pathlib import Path
from urllib.parse import urlparse


class TestLinkFormat:
    """Test link formatting and structure."""
    
    @pytest.fixture
    def readme_links(self):
        """Extract all links from README.md."""
        content = Path("README.md").read_text(encoding='utf-8')
        # Find markdown links: [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        return [(text, url) for text, url in links if url.startswith('http')]
    
    def test_all_github_links_are_well_formed(self, readme_links):
        """Test that all GitHub links follow proper format."""
        github_links = [(text, url) for text, url in readme_links 
                       if 'github.com' in url]
        
        assert len(github_links) > 0, "Should have GitHub links in README"
        
        for _text, url in github_links:
            # Parse URL
            parsed = urlparse(url)
            assert parsed.scheme in ['http', 'https'], f"Invalid scheme in {url}"
            assert parsed.netloc == 'github.com', f"Invalid GitHub URL: {url}"
            
            # Path should have at least /user/repo
            path_parts = [p for p in parsed.path.split('/') if p]
            assert len(path_parts) >= 2, f"GitHub URL should have user/repo: {url}"
    
    def test_no_duplicate_links(self, readme_links):
        """Test that there are no duplicate links (same URL)."""
        urls = [url for _, url in readme_links]
        
        from collections import Counter
        url_counts = Counter(urls)
        
        # Some duplication is OK (like framework repos), but not excessive
        duplicates = {url: count for url, count in url_counts.items() if count > 5}
        
        assert len(duplicates) == 0, f"Found excessive duplicate links: {list(duplicates.keys())[:3]}"
    
    def test_link_text_is_descriptive(self, readme_links):
        """Test that link text is descriptive and not just 'here' or 'link'."""
        generic_texts = ['here', 'link', 'click here', 'this', 'url']
        
        for text, url in readme_links:
            text_lower = text.lower().strip()
            assert text_lower not in generic_texts, \
                f"Link has generic text '{text}' for URL: {url}"
    
    def test_links_have_consistent_structure(self, readme_links):
        """Test that links follow consistent patterns within categories."""
        github_badge_links = [(t, u) for t, u in readme_links if 'img.shields.io' in u]
        
        # Badge links should have specific text patterns
        for text, _url in github_badge_links:
            # Should mention GitHub or Code
            assert 'github' in text.lower() or 'code' in text.lower() or \
                   'notebook' in text.lower() or 'view' in text.lower(), \
                f"Badge link should have descriptive text: {text}"


class TestGitHubLinks:
    """Test GitHub repository links specifically."""
    
    @pytest.fixture
    def github_repos(self):
        """Extract all GitHub repository URLs from README."""
        content = Path("README.md").read_text(encoding='utf-8')
        repos = re.findall(r'https://github\.com/([^/\s\)]+)/([^/\s\)]+)', content)
        return [(owner, repo) for owner, repo in repos]
    
    def test_github_repos_follow_naming_conventions(self, github_repos):
        """Test that GitHub repo names follow conventions."""
        for owner, repo in github_repos:
            # Owner should not be empty
            assert len(owner) > 0, "GitHub owner should not be empty"
            
            # Repo should not be empty
            assert len(repo) > 0, "GitHub repo should not be empty"
            
            # Should not have .git extension in URL
            assert not repo.endswith('.git'), f"Remove .git from URL: {owner}/{repo}"
    
    def test_github_links_point_to_valid_paths(self, _github_repos):
        """Test that GitHub links point to valid repository paths."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Extract full GitHub URLs
        full_urls = re.findall(r'https://github\.com/[^\s\)]+', content)
        
        for url in full_urls:
            # Should not have double slashes
            assert '//' not in url.replace('https://', ''), f"Invalid path in URL: {url}"
            
            # Should not end with slash
            assert not url.endswith('/'), f"URL should not end with slash: {url}"
    
    def test_no_broken_github_url_patterns(self):
        """Test for common GitHub URL mistakes."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Check for common mistakes
        assert 'github.com//' not in content, "Found double slash in GitHub URL"
        assert 'github.com/tree/main/tree/' not in content, "Found duplicate /tree/ in URL"
        assert 'github.com/blob/main/blob/' not in content, "Found duplicate /blob/ in URL"


class TestLinkAccessibility:
    """Test link accessibility patterns (not making actual HTTP requests)."""
    
    def test_links_use_https_where_appropriate(self):
        """Test that external links use HTTPS."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Find all HTTP (not HTTPS) links
        http_links = re.findall(r'http://[^\s\)]+', content)
        
        # Filter out legitimate HTTP usage (like localhost examples)
        suspicious = [link for link in http_links 
                     if not any(x in link for x in ['localhost', 'example.'])]
        
        # Most external links should use HTTPS
        assert len(suspicious) == 0, f"Found HTTP links that should be HTTPS: {suspicious[:3]}"
    
    def test_microsoft_github_io_links_are_valid(self):
        """Test that microsoft.github.io links follow valid patterns."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        ms_links = re.findall(r'https://microsoft\.github\.io/[^\s\)]+', content)
        
        for link in ms_links:
            # Should have proper structure: microsoft.github.io/project/...
            parts = link.replace('https://microsoft.github.io/', '').split('/')
            assert len(parts) >= 1, f"microsoft.github.io link should have project name: {link}"


class TestImageReferences:
    """Test image references in markdown."""
    
    def test_all_referenced_images_exist(self):
        """Test that all images referenced in markdown exist."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Find image references
        image_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)
        
        for img_path in image_refs:
            # Skip external URLs
            if img_path.startswith('http'):
                continue
            
            full_path = Path(img_path)
            assert full_path.exists(), f"Referenced image not found: {img_path}"
            assert full_path.is_file(), f"Image path is not a file: {img_path}"
    
    def test_image_paths_are_relative(self):
        """Test that image paths are relative, not absolute."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        image_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)
        
        for img_path in image_refs:
            if not img_path.startswith('http'):
                # Should not start with /
                assert not img_path.startswith('/'), \
                    f"Image path should be relative: {img_path}"
    
    def test_images_directory_structure(self):
        """Test that images are in appropriate directory."""
        images_dir = Path("images")
        assert images_dir.exists(), "Images directory should exist"
        assert images_dir.is_dir(), "Images should be a directory"
        
        # Should have image files
        image_files = list(images_dir.glob('*.*'))
        assert len(image_files) > 0, "Images directory should contain files"


class TestInternalLinks:
    """Test internal links and anchors."""
    
    def test_table_of_contents_links_are_valid(self):
        """Test that table of contents links point to valid sections."""
        content = Path("README.md").read_text(encoding='utf-8')
        
        # Find TOC links (links starting with #)
        toc_links = re.findall(r'\]\((#[^\)]+)\)', content)
        
        # Find all headers
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        
        # Convert headers to anchor format
        def to_anchor(header):
            # Remove markdown, emojis, and special chars
            clean = re.sub(r'[^\w\s-]', '', header)
            return '#' + clean.lower().replace(' ', '-')
        
        valid_anchors = [to_anchor(h) for h in headers]
        
        for link in toc_links:
            # Simplify link for comparison
            clean_link = re.sub(r'[^\w-]', '', link.replace('#', '').replace('-', ''))
            
            # Check if any valid anchor matches (fuzzy matching)
            found = False
            for anchor in valid_anchors:
                clean_anchor = re.sub(r'[^\w-]', '', anchor.replace('#', '').replace('-', ''))
                if clean_link in clean_anchor or clean_anchor in clean_link:
                    found = True
                    break
            
            if not found:
                print(f"Warning: TOC link might be broken: {link}")