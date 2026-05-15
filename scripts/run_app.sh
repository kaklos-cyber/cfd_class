#!/usr/bin/env bash
# =============================================================================
# CFD-Class 应用运行脚本
# =============================================================================
# 功能: 启动Streamlit应用服务
# 用法: bash scripts/run_app.sh [选项]
# 选项:
#   --port PORT     指定服务端口（默认8501）
#   --host HOST     指定绑定地址（默认0.0.0.0）
#   --dev           开发模式（启用自动重载）
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
PORT=8501
HOST="0.0.0.0"
DEV_MODE=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --dev)
            DEV_MODE=true
            shift
            ;;
        --help|-h)
            echo "用法: bash scripts/run_app.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --port PORT   指定服务端口（默认: 8501）"
            echo "  --host HOST   指定绑定地址（默认: 0.0.0.0）"
            echo "  --dev         开发模式（启用自动重载）"
            echo "  --help, -h    显示此帮助信息"
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}=== CFD-Class 应用启动 ===${NC}"
echo "项目目录: ${PROJECT_ROOT}"

# 检查streamlit
echo -e "${YELLOW}[1/2] 检查运行环境...${NC}"
if ! command -v streamlit &> /dev/null; then
    echo -e "${RED}错误: streamlit未安装，请先运行: bash scripts/install_dev.sh${NC}"
    exit 1
fi

# 检查入口文件
APP_ENTRY="src/frontend/app.py"
if [ ! -f "${APP_ENTRY}" ]; then
    echo -e "${YELLOW}警告: 未找到 ${APP_ENTRY}，尝试备用入口...${NC}"
    # 备用入口：使用CLI模块启动
    APP_ENTRY=""
fi

# 构建streamlit参数
STREAMLIT_ARGS=("run")

if [ -n "${APP_ENTRY}" ]; then
    STREAMLIT_ARGS+=("${APP_ENTRY}")
else
    # 备用：通过模块方式运行
    echo -e "${YELLOW}使用CLI入口启动...${NC}"
    STREAMLIT_ARGS=("run" "src/cfd_class/cli.py")
fi

STREAMLIT_ARGS+=("--server.port=${PORT}")
STREAMLIT_ARGS+=("--server.address=${HOST}")

if [ "${DEV_MODE}" = true ]; then
    echo -e "${BLUE}开发模式: 启用自动重载${NC}"
    STREAMLIT_ARGS+=("--server.runOnSave=true")
else
    STREAMLIT_ARGS+=("--server.runOnSave=false")
fi

# 启动应用
echo -e "${YELLOW}[2/2] 启动Streamlit服务...${NC}"
echo -e "${BLUE}访问地址: http://${HOST}:${PORT}${NC}"
echo ""

exec streamlit "${STREAMLIT_ARGS[@]}"
