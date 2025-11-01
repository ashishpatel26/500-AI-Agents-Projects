"""GitHub Actions workflow validation."""
import pytest
import yaml
from pathlib import Path


class TestWorkflowStructure:
    """Test workflow file structure."""
    
    @pytest.fixture
    def workflow_data(self):
        """Load workflow YAML."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        return yaml.safe_load(content)
    
    def test_has_required_fields(self, workflow_data):
        """Workflow has all required fields."""
        assert 'name' in workflow_data
        assert 'on' in workflow_data
        assert 'jobs' in workflow_data
    
    def test_triggers_configured(self, workflow_data):
        """Workflow has triggers."""
        triggers = workflow_data['on']
        assert 'push' in triggers or 'workflow_dispatch' in triggers
    
    def test_jobs_have_steps(self, workflow_data):
        """All jobs have steps."""
        for _job_name, job_config in workflow_data['jobs'].items():
            assert 'runs-on' in job_config
            assert 'steps' in job_config
            assert len(job_config['steps']) > 0
    
    def test_permissions_set(self, workflow_data):
        """Workflow has permissions."""
        assert 'permissions' in workflow_data
        perms = workflow_data['permissions']
        assert isinstance(perms, dict)
    
    def test_uses_versioned_actions(self, workflow_data):
        """Actions have version pinning."""
        for job_config in workflow_data['jobs'].values():
            for step in job_config.get('steps', []):
                if 'uses' in step:
                    action = step['uses']
                    assert '@' in action, f"Pin version: {action}"


class TestYAMLFormatting:
    """Test YAML file formatting."""
    
    def test_valid_yaml(self):
        """File is valid YAML."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        data = yaml.safe_load(content)
        assert data is not None
    
    def test_no_tabs(self):
        """YAML doesn't use tabs."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        assert '\t' not in content, "Use spaces, not tabs"
    
    def test_consistent_indentation(self):
        """YAML uses 2-space indentation."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if line and not line.strip().startswith('#'):
                spaces = len(line) - len(line.lstrip(' '))
                if spaces > 0:
                    assert spaces % 2 == 0, f"Line {i}: use 2-space indent"


class TestWorkflowSecurity:
    """Test workflow security."""
    
    def test_no_hardcoded_secrets(self):
        """No hardcoded secrets in workflow."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text()
        
        # Check for secret patterns
        assert 'password:' not in content.lower()
        assert 'api_key:' not in content.lower()
        
        # Allow secrets context references
        if 'secrets.' in content:
            assert '${{' in content, "Use secrets context"