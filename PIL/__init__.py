"""Minimal subset of the :mod:`PIL` package used by the test-suite."""

from __future__ import annotations

from . import Image as Image  # Re-export the Image module for ``from PIL import Image``
from .Image import ImageFile, UnidentifiedImageError, open

__all__ = ["Image", "ImageFile", "UnidentifiedImageError", "open"]
