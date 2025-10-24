"""
Setup script for Payroll App
Alternative packaging method using setuptools
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Professional Payroll System - Advanced Employee & Payroll Management"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="payroll-app",
    version="2.0.0",
    author="Payroll Solutions",
    author_email="support@payroll-solutions.com",
    description="Advanced Employee & Payroll Management System",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/payroll-solutions/payroll-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: GTK",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "build": [
            "pyinstaller>=5.0",
            "cx_Freeze>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "payroll-app=payroll_gui_advanced:main",
        ],
        "gui_scripts": [
            "payroll-app-gui=payroll_gui_advanced:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.ico", "*.png"],
    },
    data_files=[
        ("profiles", []),  # Empty profiles directory
        ("backups", []),   # Empty backups directory
        ("exports", []),   # Empty exports directory
    ],
    keywords="payroll, employee, management, accounting, business, finance",
    project_urls={
        "Bug Reports": "https://github.com/payroll-solutions/payroll-app/issues",
        "Source": "https://github.com/payroll-solutions/payroll-app",
        "Documentation": "https://payroll-solutions.com/docs",
    },
)
