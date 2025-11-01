import re
from pathlib import Path

import pytest


@pytest.fixture
def _github_repos():
    """
    Provide GitHub repository tuples for link validation tests.
    
    Reads README.md and extracts GitHub owner/repository pairs from URLs of the form
    https://github.com/{owner}/{repo}.
    
    Returns:
        list[tuple[str, str]]: A list of (owner, repo) tuples found in README.md; an empty list if no matches are found.
    """
    content = Path("README.md").read_text(encoding="utf-8")
    matches = re.findall(r"https://github\.com/([^/\s\)]+)/([^/\s\)]+)", content)
    return [(owner, repo) for owner, repo in matches]