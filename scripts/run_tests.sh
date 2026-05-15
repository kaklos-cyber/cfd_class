#!/usr/bin/env bash
# =============================================================================
# CFD-Class 测试运行脚本
# =============================================================================
# 功能: 运行项目测试套件，支持覆盖率报告
# 用法: bash scripts/run_tests.sh [选项]
# 选项:
#   --cov       生成覆盖率报告（默认启用）
#   --no-cov    不生成覆盖率报告
#   --html      生成HTML覆盖率报告
#   --verbose   详细输出模式
# =============================================================================

set -euo pipefail

# 颜色定义
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# 项目根目录
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

# 默认配置
WITH_COV=true
HTML_REPORT=false
VERBOSE=false

# 解析参数
for arg in "$@"; do
    case $arg in
        --no-cov)
            WITH_COV=false
            shift
            ;;
        --html)
            HTML_REPORT=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "用法: bash scripts/run_tests.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --cov       生成覆盖率报告（默认）"
            echo "  --no-cov    不生成覆盖率报告"
            echo "  --html      生成HTML格式覆盖率报告"
            echo "  --verbose   详细输出模式"
            echo "  --help, -h  显示此帮助信息"
            exit 0
            ;;
    esac
done

echo -e "${GREEN}=== CFD-Class 测试执行 ===${NC}"
echo "项目目录: ${PROJECT_ROOT}"

# 检查pytest
echo -e "${YELLOW}[1/3] 检查测试环境...${NC}"
if ! python3 -c "import pytest" 2>/dev/null; then
    echo -e "${RED}错误: pytest未安装，请先运行: bash scripts/install_dev.sh${NC}"
    exit 1
fi

# 构建pytest参数
PYTEST_ARGS=("-v" "--tb=short")

if [ "${VERBOSE}" = true ]; then
    PYTEST_ARGS+=("--capture=no" "-vv")
fi

if [ "${WITH_COV}" = true ]; then
    PYTEST_ARGS+=("--cov=cfd_class" "--cov-report=term-missing")
    if [ "${HTML_REPORT}" = true ]; then
        PYTEST_ARGS+=("--cov-report=html:htmlcov")
        echo -e "${BLUE}将生成HTML覆盖率报告到 htmlcov/ 目录${NC}"
    fi
fi

# 运行测试
echo -e "${YELLOW}[2/3] 运行测试套件...${NC}"
echo -e "${BLUE}pytest参数: ${PYTEST_ARGS[*]}${NC}"
echo ""

if pytest "${PYTEST_ARGS[@]}" tests/; then
    echo ""
    echo -e "${GREEN}[3/3] 测试全部通过!${NC}"
else
    echo ""
    echo -e "${RED}[3/3] 测试存在失败项${NC}"
    exit 1
fi

# 提示HTML报告位置
if [ "${HTML_REPORT}" = true ] && [ "${WITH_COV}" = true ]; then
    echo ""
    echo -e "${BLUE}HTML覆盖率报告: ${PROJECT_ROOT}/htmlcov/index.html${NC}"
    echo "  可用浏览器打开查看详细报告"
fi

echo -e "${GREEN}=== 测试执行完成 ===${NC}"
