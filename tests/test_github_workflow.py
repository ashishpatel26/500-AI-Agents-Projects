"""
Tests for GitHub Actions workflow configuration.

This test suite validates the Jekyll GitHub Pages workflow YAML file
for syntax correctness, required fields, and proper configuration.
"""

import os
import pytest
import yaml


class TestGitHubWorkflow:
    """Test suite for GitHub Actions workflow validation."""
    
    @pytest.fixture
    def workflow_path(self):
        """Return the path to the workflow file."""
        return ".github/workflows/jekyll-gh-pages.yml"
    
    @pytest.fixture
    def workflow_content(self, workflow_path):
        """Load and parse the workflow YAML file."""
        assert os.path.exists(workflow_path), f"Workflow file not found: {workflow_path}"
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def test_workflow_file_exists(self, workflow_path):
        """Test that the workflow file exists."""
        assert os.path.exists(workflow_path), "GitHub workflow file should exist"
    
    def test_workflow_has_name(self, workflow_content):
        """Test that workflow has a name defined."""
        assert 'name' in workflow_content, "Workflow must have a name"
        assert workflow_content['name'], "Workflow name must not be empty"
        assert len(workflow_content['name']) > 0, "Workflow name must be non-empty"
    
    def test_workflow_has_on_triggers(self, workflow_content):
        """Test that workflow has proper trigger configuration."""
        assert 'on' in workflow_content, "Workflow must have 'on' triggers defined"
        on_config = workflow_content['on']
        assert on_config is not None, "Workflow triggers must not be None"
        
        # Check for push trigger
        assert 'push' in on_config, "Workflow should have push trigger"
        assert 'branches' in on_config['push'], "Push trigger should specify branches"
        assert 'main' in on_config['push']['branches'], "Should trigger on main branch"
    
    def test_workflow_has_workflow_dispatch(self, workflow_content):
        """Test that workflow can be manually triggered."""
        assert 'workflow_dispatch' in workflow_content['on'], \
            "Workflow should support manual dispatch"
    
    def test_workflow_has_permissions(self, workflow_content):
        """Test that workflow has appropriate permissions configured."""
        assert 'permissions' in workflow_content, "Workflow must define permissions"
        perms = workflow_content['permissions']
        
        # Check required permissions for GitHub Pages deployment
        assert 'contents' in perms, "Must have contents permission"
        assert perms['contents'] == 'read', "Contents should be read-only"
        assert 'pages' in perms, "Must have pages permission"
        assert perms['pages'] == 'write', "Pages should be writable"
        assert 'id-token' in perms, "Must have id-token permission"
        assert perms['id-token'] == 'write', "ID token should be writable"
    
    def test_workflow_has_concurrency_control(self, workflow_content):
        """Test that workflow has concurrency control."""
        assert 'concurrency' in workflow_content, "Workflow should define concurrency"
        concurrency = workflow_content['concurrency']
        assert 'group' in concurrency, "Concurrency must have a group"
        assert concurrency['group'] == 'pages', "Should use 'pages' concurrency group"
        assert 'cancel-in-progress' in concurrency, "Should define cancel-in-progress"
        assert not concurrency['cancel-in-progress'], \
            "Should not cancel in-progress deployments"
    
    def test_workflow_has_jobs(self, workflow_content):
        """Test that workflow defines jobs."""
        assert 'jobs' in workflow_content, "Workflow must define jobs"
        jobs = workflow_content['jobs']
        assert len(jobs) > 0, "Workflow must have at least one job"
    
    def test_workflow_has_build_job(self, workflow_content):
        """Test that workflow has a build job."""
        jobs = workflow_content['jobs']
        assert 'build' in jobs, "Workflow must have a 'build' job"
        build_job = jobs['build']
        
        # Check runner
        assert 'runs-on' in build_job, "Build job must specify runner"
        assert build_job['runs-on'] == 'ubuntu-latest', \
            "Should use ubuntu-latest runner"
        
        # Check steps
        assert 'steps' in build_job, "Build job must have steps"
        assert len(build_job['steps']) > 0, "Build job must have at least one step"
    
    def test_workflow_has_deploy_job(self, workflow_content):
        """Test that workflow has a deploy job."""
        jobs = workflow_content['jobs']
        assert 'deploy' in jobs, "Workflow must have a 'deploy' job"
        deploy_job = jobs['deploy']
        
        # Check runner
        assert 'runs-on' in deploy_job, "Deploy job must specify runner"
        assert deploy_job['runs-on'] == 'ubuntu-latest', \
            "Should use ubuntu-latest runner"
        
        # Check dependencies
        assert 'needs' in deploy_job, "Deploy job should depend on other jobs"
        assert 'build' in deploy_job['needs'], "Deploy should depend on build"
        
        # Check environment
        assert 'environment' in deploy_job, "Deploy job should specify environment"
        env = deploy_job['environment']
        assert 'name' in env, "Environment must have a name"
        assert env['name'] == 'github-pages', "Should deploy to github-pages"
    
    def test_build_job_checkout_step(self, workflow_content):
        """Test that build job has checkout step."""
        build_steps = workflow_content['jobs']['build']['steps']
        checkout_step = next((s for s in build_steps if 'Checkout' in s.get('name', '')), None)
        assert checkout_step is not None, "Build job must have a checkout step"
        assert 'uses' in checkout_step, "Checkout step must use an action"
        assert 'actions/checkout@v4' in checkout_step['uses'], \
            "Should use checkout@v4 action"
    
    def test_build_job_jekyll_build_step(self, workflow_content):
        """Test that build job has Jekyll build step."""
        build_steps = workflow_content['jobs']['build']['steps']
        jekyll_step = next((s for s in build_steps 
                          if 'Jekyll' in s.get('name', '')), None)
        assert jekyll_step is not None, "Build job must have a Jekyll build step"
        assert 'uses' in jekyll_step, "Jekyll step must use an action"
        assert 'jekyll-build-pages' in jekyll_step['uses'], \
            "Should use jekyll-build-pages action"
    
    def test_build_job_upload_artifact_step(self, workflow_content):
        """Test that build job uploads artifact."""
        build_steps = workflow_content['jobs']['build']['steps']
        upload_step = next((s for s in build_steps 
                          if 'Upload' in s.get('name', '') or 'upload' in s.get('uses', '')), None)
        assert upload_step is not None, "Build job must upload artifact"
        assert 'uses' in upload_step, "Upload step must use an action"
        assert 'upload-pages-artifact' in upload_step['uses'], \
            "Should use upload-pages-artifact action"
    
    def test_deploy_job_deploy_step(self, workflow_content):
        """Test that deploy job has deploy step."""
        deploy_steps = workflow_content['jobs']['deploy']['steps']
        deploy_step = next((s for s in deploy_steps 
                          if 'Deploy' in s.get('name', '')), None)
        assert deploy_step is not None, "Deploy job must have a deploy step"
        assert 'uses' in deploy_step, "Deploy step must use an action"
        assert 'deploy-pages' in deploy_step['uses'], \
            "Should use deploy-pages action"
        assert 'id' in deploy_step, "Deploy step should have an ID"
        assert deploy_step['id'] == 'deployment', "Deploy step ID should be 'deployment'"
    
    def test_yaml_syntax_valid(self, workflow_path):
        """Test that YAML file has valid syntax."""
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML syntax: {e}")