"""
CFD-Class 命令行入口模块

支持通过以下方式运行:
    python -m cfd_class
    python -m cfd_class --help
    python -m cfd_class run

作为包的直接入口点，委托给cli模块处理。
"""

import sys

from cfd_class.cli import main

if __name__ == "__main__":
    sys.exit(main())
