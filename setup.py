#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFD-Class 安装脚本（兼容备用）

符合GB/T国标的计算流体动力学(CFD)教学软件打包配置。
支持setuptools传统安装方式，作为pyproject.toml的兼容备用方案。

用法:
    python setup.py sdist bdist_wheel
    pip install -e .
"""

from pathlib import Path

from setuptools import find_packages, setup

# 读取README.md作为长描述
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

setup(
    # 项目基础信息
    name="cfd-class",
    version="0.1.0-alpha.1",
    description="CFD-Class: 符合GB/T国标的一维溃坝教学软件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CFD-Team",
    author_email="team@cfd-class.org",
    license="MIT",
    # Python版本要求
    python_requires=">=3.10",
    # 包发现配置
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["cfd_class*"]),
    include_package_data=True,
    # 核心依赖
    install_requires=[
        "numpy>=1.24.0,<2.0.0",
        "scipy>=1.10.0,<2.0.0",
        "matplotlib>=3.7.0,<4.0.0",
        "streamlit>=1.28.0,<2.0.0",
    ],
    # 可选依赖
    extras_require={
        "dev": [
            "pytest>=7.4.0,<9.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "black>=23.0.0,<25.0.0",
            "isort>=5.12.0,<6.0.0",
            "flake8>=6.1.0,<8.0.0",
            "mypy>=1.5.0,<2.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0,<8.0.0",
            "sphinx-rtd-theme>=1.3.0,<2.0.0",
        ],
        "animation": [
            "Pillow>=10.0.0,<11.0.0",
        ],
        "report": [
            "jinja2>=3.1.0,<4.0.0",
        ],
    },
    # 入口点配置
    entry_points={
        "console_scripts": [
            "cfd-class=cfd_class.cli:main",
        ],
    },
    # 项目URL
    url="https://github.com/kaklos-cyber/cfd_class",
    project_urls={
        "Documentation": "https://github.com/kaklos-cyber/cfd_class#readme",
        "Source": "https://github.com/kaklos-cyber/cfd_class.git",
        "Tracker": "https://github.com/kaklos-cyber/cfd_class/issues",
    },
    # 分类器
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="cfd fluid-dynamics dam-break education finite-volume",
    zip_safe=False,
)
