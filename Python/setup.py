"""Setup script for seedhash package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="seedhash",
    version="0.1.0",
    author="melhzy",
    author_email="your.email@example.com",
    description="Deterministic seed generation from string inputs using MD5 hashing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/melhzy/seedhash",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No required dependencies - uses only Python standard library
    ],
    extras_require={
        "torch": ["torch>=1.7.0"],
        "tensorflow": ["tensorflow>=2.0.0"],
        "numpy": ["numpy>=1.19.0"],
        "all": [
            "torch>=1.7.0",
            "tensorflow>=2.0.0",
            "numpy>=1.19.0",
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    keywords="seed random hash reproducible deterministic pytorch tensorflow numpy deep-learning",
    project_urls={
        "Bug Reports": "https://github.com/melhzy/seedhash/issues",
        "Source": "https://github.com/melhzy/seedhash",
    },
)
