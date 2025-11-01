"""Tests for image file validation."""

import os
import pytest
from PIL import Image


class TestImageFiles:
    """Test suite for image file validation."""
    
    @pytest.fixture(params=[
        'images/AIAgentUseCase.jpg',
        'images/industry_usecase.png',
        'images/industry_usecase1.png'
    ])
    def image_file(self, request):
        return request.param
    
    def test_image_file_exists(self, image_file):
        assert os.path.exists(image_file), f"Image not found: {image_file}"
    
    def test_image_file_not_empty(self, image_file):
        file_size = os.path.getsize(image_file)
        assert file_size > 1024, f"{image_file} too small"
    
    def test_image_file_readable(self, image_file):
        try:
            with Image.open(image_file) as img:
                img.verify()
        except (OSError, ValueError) as e:
            pytest.fail(f"Failed to read {image_file}: {e}")
    
    def test_image_has_valid_format(self, image_file):
        with Image.open(image_file) as img:
            assert img.format in ['JPEG', 'PNG']
    
    def test_image_has_reasonable_dimensions(self, image_file):
        with Image.open(image_file) as img:
            width, height = img.size
            assert width >= 100 and height >= 100
            assert width <= 10000 and height <= 10000
    
    def test_image_referenced_in_readme(self, image_file):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        image_filename = os.path.basename(image_file)
        assert image_filename in content or image_file in content


class TestImageDirectory:
    """Test the images directory structure."""
    
    def test_images_directory_exists(self):
        assert os.path.exists('images')
        assert os.path.isdir('images')