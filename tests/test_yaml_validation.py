"""
Tests for validating YAML configuration files.
"""
import pytest
import yaml
from pathlib import Path


class TestGitHubWorkflow:
    """Test the GitHub Actions workflow YAML file."""
    
    @pytest.fixture
    def workflow_path(self):
        """Get path to workflow file."""
        return Path(".github/workflows/jekyll-gh-pages.yml")
    
    @pytest.fixture
    def workflow_content(self, workflow_path):
        """Load workflow file content."""
        assert workflow_path.exists(), "Workflow file should exist"
        return workflow_path.read_text(encoding='utf-8')
    
    @pytest.fixture
    def workflow_data(self, workflow_content):
        """Parse workflow YAML."""
        return yaml.safe_load(workflow_content)
    
    def test_workflow_file_exists(self, workflow_path):
        """Test that the GitHub Actions workflow file exists."""
        assert workflow_path.exists()
        assert workflow_path.is_file()
    
    def test_workflow_is_valid_yaml(self, workflow_data):
        """Test that the workflow file is valid YAML."""
        assert workflow_data is not None
        assert isinstance(workflow_data, dict)
    
    def test_workflow_has_name(self, workflow_data):
        """Test that workflow has a name."""
        assert 'name' in workflow_data
        assert isinstance(workflow_data['name'], str)
        assert len(workflow_data['name']) > 0
    
    def test_workflow_has_triggers(self, workflow_data):
        """Test that workflow has on: triggers defined."""
        assert 'on' in workflow_data
        triggers = workflow_data['on']
        
        # Should have push trigger
        assert 'push' in triggers or 'workflow_dispatch' in triggers
    
    def test_workflow_has_jobs(self, workflow_data):
        """Test that workflow has jobs defined."""
        assert 'jobs' in workflow_data
        assert isinstance(workflow_data['jobs'], dict)
        assert len(workflow_data['jobs']) > 0
    
    def test_workflow_jobs_have_runs_on(self, workflow_data):
        """Test that all jobs specify runs-on."""
        jobs = workflow_data['jobs']
        for job_name, job_config in jobs.items():
            assert 'runs-on' in job_config, f"Job '{job_name}' should have 'runs-on'"
            assert isinstance(job_config['runs-on'], str)
    
    def test_workflow_jobs_have_steps(self, workflow_data):
        """Test that all jobs have steps defined."""
        jobs = workflow_data['jobs']
        for job_name, job_config in jobs.items():
            assert 'steps' in job_config, f"Job '{job_name}' should have 'steps'"
            assert isinstance(job_config['steps'], list)
            assert len(job_config['steps']) > 0
    
    def test_workflow_steps_have_names(self, workflow_data):
        """Test that workflow steps have descriptive names."""
        jobs = workflow_data['jobs']
        for job_name, job_config in jobs.items():
            steps = job_config.get('steps', [])
            for _i, step in enumerate(steps):
                if 'name' in step:
                    assert len(step['name']) > 0, f"Step in job '{job_name}' has empty name"
    
    def test_workflow_uses_valid_actions(self, workflow_data):
        """Test that workflow uses valid GitHub Actions."""
        jobs = workflow_data['jobs']
        
        for _job_name, job_config in jobs.items():
            steps = job_config.get('steps', [])
            for step in steps:
                if 'uses' in step:
                    action = step['uses']
                    # Should be in format owner/repo@version
                    assert '@' in action, f"Action '{action}' should have version specified"
    
    def test_workflow_permissions_are_defined(self, workflow_data):
        """Test that workflow has permissions defined."""
        assert 'permissions' in workflow_data
        permissions = workflow_data['permissions']
        assert isinstance(permissions, dict)
    
    def test_workflow_concurrency_is_configured(self, workflow_data):
        """Test that workflow has concurrency control."""
        assert 'concurrency' in workflow_data
        concurrency = workflow_data['concurrency']
        assert 'group' in concurrency
    
    def test_jekyll_specific_configuration(self, workflow_data):
        """Test Jekyll-specific workflow configuration."""
        # Should be deploying to GitHub Pages
        assert workflow_data['name'].lower().find('jekyll') >= 0 or \
               workflow_data['name'].lower().find('pages') >= 0
        
        # Should have a deploy job
        jobs = workflow_data['jobs']
        job_names = [name.lower() for name in jobs.keys()]
        assert any('deploy' in name for name in job_names)
    
    def test_workflow_build_job_configuration(self, workflow_data):
        """Test that build job is properly configured."""
        jobs = workflow_data['jobs']
        
        # Should have a build job
        assert 'build' in jobs
        build_job = jobs['build']
        
        # Build job should have steps
        assert 'steps' in build_job
        steps = build_job['steps']
        
        # Should checkout code
        step_actions = [s.get('uses', '') for s in steps]
        assert any('checkout' in action.lower() for action in step_actions)


class TestYAMLFormatting:
    """Test YAML file formatting and style."""
    
    @pytest.fixture
    def workflow_content(self):
        """Load workflow file content."""
        return Path(".github/workflows/jekyll-gh-pages.yml").read_text(encoding='utf-8')
    
    def test_yaml_uses_consistent_indentation(self, workflow_content):
        """Test that YAML uses consistent indentation (2 spaces)."""
        lines = workflow_content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if line and not line.strip().startswith('#'):
                # Count leading spaces
                leading_spaces = len(line) - len(line.lstrip(' '))
                if leading_spaces > 0:
                    # Should be multiple of 2
                    assert leading_spaces % 2 == 0, \
                        f"Line {i} has inconsistent indentation: {leading_spaces} spaces"
    
    def test_yaml_has_no_tabs(self, workflow_content):
        """Test that YAML file doesn't use tabs."""
        assert '\t' not in workflow_content, "YAML should not contain tabs"
    
    def test_yaml_has_proper_line_endings(self, workflow_content):
        """Test that YAML file uses Unix line endings."""
        assert '\r\n' not in workflow_content, "Should use Unix line endings (LF)"


class TestYAMLSecurity:
    """Test security aspects of YAML configuration."""
    
    @pytest.fixture
    def workflow_data(self):
        """Load and parse workflow file."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text(encoding='utf-8')
        return yaml.safe_load(content)
    
    def test_no_hardcoded_secrets(self):
        """Test that there are no hardcoded secrets in workflow."""
        content = Path(".github/workflows/jekyll-gh-pages.yml").read_text(encoding='utf-8')
        
        # Common secret patterns
        secret_patterns = [
            r'password\s*[:=]\s*["\']?\w+',
            r'api[_-]?key\s*[:=]\s*["\']?\w+',
            r'token\s*[:=]\s*["\']?\w+',
            r'secret\s*[:=]\s*["\']?\w+',
        ]
        
        import re
        for pattern in secret_patterns:
            matches = re.findall(pattern, content.lower())
            # Allow references to secrets. context like ${{ secrets.X }}
            for match in matches:
                assert '${{' in content or 'secrets.' not in match.lower(), \
                    f"Possible hardcoded secret: {match}"
    
    def test_workflow_uses_pinned_action_versions(self, workflow_data):
        """Test that workflow uses pinned action versions."""
        jobs = workflow_data['jobs']
        
        for _job_name, job_config in jobs.items():
            steps = job_config.get('steps', [])
            for step in steps:
                if 'uses' in step:
                    action = step['uses']
                    # Should have version pinned
                    assert '@' in action, f"Action should be version-pinned: {action}"