from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="memora-memory",
    version="0.2.0",
    description="Smart LLM memory with auto-domain, dedup, and hybrid search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kartik Sharma",
    author_email="kartiknaveen2007@gmail.com",
    url="https://github.com/SPARKEDIX/memora",
    packages=["memora"],
    package_dir={"memora": "memora"},
    install_requires=[
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0",
        "numpy>=1.21.0",
        "rank-bm25>=0.2.2",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="llm memory vector-database ai embedding hybrid-search",
    license="MIT",
)