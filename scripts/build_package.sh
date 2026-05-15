#!/usr/bin/env bash
# =============================================================================
# CFD-Class 构建脚本
# =============================================================================
# 功能: 构建Python wheel和源码分发包(sdist)
# 用法: bash scripts/build_package.sh
# =============================================================================

set -euo pipefail

# 颜色定义
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# 项目根目录
readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

echo -e "${GREEN}=== CFD-Class 打包构建 ===${NC}"
echo "项目目录: ${PROJECT_ROOT}"

# 检查Python环境
echo -e "${YELLOW}[1/5] 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到python3命令${NC}"
    exit 1
fi

python3 --version

# 清理旧构建产物
echo -e "${YELLOW}[2/5] 清理旧构建产物...${NC}"
rm -rf build/ dist/ *.egg-info src/*.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "清理完成"

# 安装构建依赖
echo -e "${YELLOW}[3/5] 安装构建依赖...${NC}"
python3 -m pip install --quiet build twine check-wheel-contents

# 执行构建
echo -e "${YELLOW}[4/5] 构建wheel和sdist...${NC}"
python3 -m build

# 验证构建产物
echo -e "${YELLOW}[5/5] 验证构建产物...${NC}"
if [ -d "dist" ]; then
    echo -e "${GREEN}构建产物列表:${NC}"
    ls -lh dist/

    # 检查wheel内容
    for wheel in dist/*.whl; do
        if [ -f "${wheel}" ]; then
            echo -e "${YELLOW}检查wheel: $(basename "${wheel}")${NC}"
            check-wheel-contents "${wheel}" || true
        fi
    done

    # 验证上传可行性
    echo -e "${YELLOW}运行twine检查...${NC}"
    python3 -m twine check dist/*
else
    echo -e "${RED}错误: 未找到构建产物目录 dist/${NC}"
    exit 1
fi

echo -e "${GREEN}=== 构建完成 ===${NC}"
echo "产物位于: ${PROJECT_ROOT}/dist/"
