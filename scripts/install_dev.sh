#!/usr/bin/env bash
# =============================================================================
# CFD-Class 开发环境安装脚本
# =============================================================================
# 功能: 安装项目及其所有开发依赖
# 用法: bash scripts/install_dev.sh
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

echo -e "${GREEN}=== CFD-Class 开发环境安装 ===${NC}"
echo "项目目录: ${PROJECT_ROOT}"

# 检查Python版本
echo -e "${YELLOW}[1/5] 检查Python版本...${NC}"
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_MAJOR=3
REQUIRED_MINOR=10

IFS='.' read -r MAJOR MINOR <<< "${PYTHON_VERSION}"
if [ "${MAJOR}" -lt ${REQUIRED_MAJOR} ] || ([ "${MAJOR}" -eq ${REQUIRED_MAJOR} ] && [ "${MINOR}" -lt ${REQUIRED_MINOR} ]); then
    echo -e "${RED}错误: 需要Python >= 3.10, 当前版本: ${PYTHON_VERSION}${NC}"
    exit 1
fi
echo -e "${GREEN}Python版本符合要求: ${PYTHON_VERSION}${NC}"

# 检查虚拟环境（可选但推荐）
echo -e "${YELLOW}[2/5] 检查虚拟环境...${NC}"
if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo -e "${BLUE}提示: 未检测到虚拟环境，建议创建venv以获得隔离环境${NC}"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
else
    echo -e "${GREEN}当前虚拟环境: ${VIRTUAL_ENV}${NC}"
fi

# 升级pip
echo -e "${YELLOW}[3/5] 升级pip...${NC}"
python3 -m pip install --upgrade pip setuptools wheel

# 安装项目（开发模式，包含所有可选依赖）
echo -e "${YELLOW}[4/5] 安装项目及依赖...${NC}"
python3 -m pip install -e ".[dev,docs,animation,report]"

# 验证安装
echo -e "${YELLOW}[5/5] 验证安装...${NC}"
if python3 -c "import cfd_class; print(cfd_class.__version__)" 2>/dev/null; then
    INSTALLED_VERSION=$(python3 -c "import cfd_class; print(cfd_class.__version__)")
    echo -e "${GREEN}cfd_class 安装成功，版本: ${INSTALLED_VERSION}${NC}"
else
    echo -e "${RED}警告: 无法导入cfd_class模块${NC}"
fi

# 检查CLI入口点
echo -e "${YELLOW}检查CLI入口点...${NC}"
if command -v cfd-class &> /dev/null; then
    echo -e "${GREEN}CLI命令 'cfd-class' 可用${NC}"
else
    echo -e "${YELLOW}提示: CLI命令 'cfd-class' 可能需要重新激活虚拟环境或刷新shell${NC}"
fi

# 检查关键依赖
echo -e "${YELLOW}检查关键依赖...${NC}"
python3 -c "
import numpy, scipy, matplotlib, streamlit
print(f'  numpy: {numpy.__version__}')
print(f'  scipy: {scipy.__version__}')
print(f'  matplotlib: {matplotlib.__version__}')
print(f'  streamlit: {streamlit.__version__}')
"

echo -e "${GREEN}=== 开发环境安装完成 ===${NC}"
echo ""
echo "常用命令:"
echo "  运行应用:    streamlit run src/frontend/app.py"
echo "  运行测试:    pytest"
echo "  代码格式化:  black src/ tests/"
echo "  静态检查:    mypy src/"
