"""
CFD-Class 命令行接口(CLI)

提供统一的命令行入口，支持以下子命令:
    run     启动Streamlit应用服务
    test    运行测试套件
    version 显示版本信息
    info    显示项目信息

用法示例:
    cfd-class run --port 8501
    cfd-class test --cov
    cfd-class version
"""

import argparse
import sys
from pathlib import Path

from cfd_class import __version__


def cmd_run(args: argparse.Namespace) -> int:
    """
    启动Streamlit应用服务

    参数:
        args: 命令行参数命名空间，包含port和host等选项

    返回:
        进程退出码，0表示成功
    """
    try:
        import streamlit.web.cli as stcli
    except ImportError:
        print("错误: 未安装streamlit，请运行: pip install streamlit")
        return 1

    # 确定应用入口文件
    project_root = Path(__file__).parent.parent.parent
    app_entry = project_root / "src" / "frontend" / "app.py"

    if not app_entry.exists():
        print(f"错误: 未找到应用入口文件 {app_entry}")
        print("请确认frontend/app.py存在，或检查项目结构")
        return 1

    # 构建streamlit参数
    sys.argv = [
        "streamlit",
        "run",
        str(app_entry),
        f"--server.port={args.port}",
        f"--server.address={args.host}",
    ]

    if args.dev:
        sys.argv.append("--server.runOnSave=true")

    print(f"启动Streamlit服务: http://{args.host}:{args.port}")
    stcli.main()
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    """
    运行测试套件

    参数:
        args: 命令行参数命名空间，包含cov等选项

    返回:
        进程退出码，0表示全部通过
    """
    try:
        import pytest
    except ImportError:
        print("错误: 未安装pytest，请运行: pip install pytest")
        return 1

    pytest_args = ["-v", "--tb=short"]

    if args.cov:
        pytest_args.extend(["--cov=cfd_class", "--cov-report=term-missing"])

    if args.verbose:
        pytest_args.extend(["--capture=no", "-vv"])

    # 添加测试目录
    project_root = Path(__file__).parent.parent.parent
    test_dir = project_root / "tests"
    if test_dir.exists():
        pytest_args.append(str(test_dir))
    else:
        print(f"警告: 未找到测试目录 {test_dir}")
        return 1

    return pytest.main(pytest_args)


def cmd_version(_args: argparse.Namespace) -> int:
    """
    显示版本信息

    返回:
        进程退出码，0表示成功
    """
    print(f"CFD-Class 版本: {__version__}")
    print("符合GB/T国标的一维溃坝CFD教学软件")
    print("项目主页: https://github.com/kaklos-cyber/cfd_class")
    return 0


def cmd_info(_args: argparse.Namespace) -> int:
    """
    显示项目详细信息

    返回:
        进程退出码，0表示成功
    """
    print("=" * 50)
    print("CFD-Class 项目信息")
    print("=" * 50)
    print(f"版本:        {__version__}")
    print("名称:        一维溃坝CFD教学软件")
    print("许可证:      MIT")
    print("作者:        CFD-Team")
    print("Python要求:  >= 3.10")
    print("=" * 50)
    print("\n核心功能:")
    print("  - 6种有限体积数值格式对比")
    print("  - 参数化交互探索")
    print("  - 动画可视化演示")
    print("  - 自动HTML报告生成")
    print("\n支持的数值格式:")
    print("  - Lax-Friedrichs (一阶)")
    print("  - Lax-Wendroff (二阶)")
    print("  - MacCormack (二阶)")
    print("  - Godunov (一阶+)")
    print("  - HLL (一阶+)")
    print("  - MUSCL-Hancock (二阶 TVD)")
    return 0


def main(argv: list[str] | None = None) -> int:
    """
    CLI主入口函数

    参数:
        argv: 命令行参数列表，None则使用sys.argv

    返回:
        进程退出码
    """
    parser = argparse.ArgumentParser(
        prog="cfd-class",
        description="CFD-Class: 符合GB/T国标的一维溃坝CFD教学软件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  cfd-class run                 启动应用（默认端口8501）
  cfd-class run --port 8080     指定端口启动
  cfd-class test                运行测试
  cfd-class test --cov          运行测试并生成覆盖率报告
  cfd-class version             显示版本
  cfd-class info                显示项目信息
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # run 子命令
    run_parser = subparsers.add_parser("run", help="启动Streamlit应用服务")
    run_parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="服务端口（默认: 8501）",
    )
    run_parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="绑定地址（默认: 0.0.0.0）",
    )
    run_parser.add_argument(
        "--dev",
        action="store_true",
        help="开发模式（启用自动重载）",
    )
    run_parser.set_defaults(func=cmd_run)

    # test 子命令
    test_parser = subparsers.add_parser("test", help="运行测试套件")
    test_parser.add_argument(
        "--cov",
        action="store_true",
        help="生成覆盖率报告",
    )
    test_parser.add_argument(
        "--verbose",
        action="store_true",
        help="详细输出模式",
    )
    test_parser.set_defaults(func=cmd_test)

    # version 子命令
    version_parser = subparsers.add_parser("version", help="显示版本信息")
    version_parser.set_defaults(func=cmd_version)

    # info 子命令
    info_parser = subparsers.add_parser("info", help="显示项目详细信息")
    info_parser.set_defaults(func=cmd_info)

    # 解析参数
    args = parser.parse_args(argv)

    # 如果没有子命令，显示帮助
    if args.command is None:
        parser.print_help()
        return 0

    # 执行对应命令
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
