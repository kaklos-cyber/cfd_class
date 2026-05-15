# =============================================================================
# CFD-Class Docker多阶段构建文件
# =============================================================================
# 功能: 构建CFD-Class应用的容器镜像
# 用法:
#   docker build -t cfd-class:latest .
#   docker run -p 8501:8501 cfd-class:latest
# =============================================================================

# -----------------------------------------------------------------------------
# 阶段1: 构建阶段（Build Stage）
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt pyproject.toml setup.py ./
COPY src/ ./src/

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 升级pip并安装构建工具
RUN pip install --no-cache-dir --upgrade pip setuptools wheel build

# 安装项目及其依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .

# -----------------------------------------------------------------------------
# 阶段2: 生产运行阶段（Production Stage）
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS production

# 设置元数据标签
LABEL maintainer="CFD-Team <team@cfd-class.org>"
LABEL description="CFD-Class: 符合GB/T国标的一维溃坝CFD教学软件"
LABEL version="0.1.0-alpha.1"

# 设置工作目录
WORKDIR /app

# 安装运行时系统依赖（仅必要的库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用源码（用于开发热重载等场景）
COPY src/ ./src/
COPY docs/ ./docs/
COPY README.md LICENSE CHANGELOG.md ./

# 创建非root用户运行应用（安全最佳实践）
RUN groupadd -r cfduser && useradd -r -g cfduser cfduser
RUN chown -R cfduser:cfduser /app
USER cfduser

# 暴露Streamlit默认端口
EXPOSE 8501

# 设置Streamlit环境变量
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# 启动命令
CMD ["streamlit", "run", "src/frontend/app.py"]

# -----------------------------------------------------------------------------
# 阶段3: 开发阶段（Development Stage）
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS development

# 设置元数据标签
LABEL stage="development"

# 设置工作目录
WORKDIR /app

# 安装开发所需的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt pyproject.toml setup.py ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY docs/ ./docs/
COPY scripts/ ./scripts/
COPY README.md LICENSE CHANGELOG.md CONTRIBUTING.md ./

# 安装所有依赖（含开发依赖）
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e ".[dev,docs,animation,report]"

# 暴露Streamlit端口
EXPOSE 8501

# 设置Streamlit环境变量（开发模式启用自动重载）
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_RUN_ON_SAVE=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 开发模式默认命令
CMD ["streamlit", "run", "src/frontend/app.py", "--server.runOnSave=true"]
