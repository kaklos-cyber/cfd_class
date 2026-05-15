.PHONY: help install install-dev test test-cov lint lint-fix build docs clean run format check all

# 默认目标
.DEFAULT_GOAL := help

# 变量定义
PYTHON := python
PIP := pip
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip

# 检测操作系统
ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV_DIR)/Scripts
	VENV_PYTHON := $(VENV_BIN)/python.exe
	VENV_PIP := $(VENV_BIN)/pip.exe
endif

# 帮助信息
help:
	@echo "CFD-Class Makefile 命令列表"
	@echo ""
	@echo "  安装命令:"
	@echo "    make install      - 安装项目依赖"
	@echo "    make install-dev  - 安装开发依赖(包含测试、文档、代码检查工具)"
	@echo ""
	@echo "  运行命令:"
	@echo "    make run          - 运行 Streamlit 应用"
	@echo ""
	@echo "  测试命令:"
	@echo "    make test         - 运行测试套件"
	@echo "    make test-cov     - 运行测试并生成覆盖率报告"
	@echo ""
	@echo "  代码检查命令:"
	@echo "    make lint         - 执行代码检查(black, isort, flake8, mypy)"
	@echo "    make lint-fix     - 自动修复代码格式问题"
	@echo "    make format       - 格式化代码(black + isort)"
	@echo "    make check        - 完整代码质量检查(不自动修复)"
	@echo ""
	@echo "  构建命令:"
	@echo "    make build        - 构建 Python 分发包"
	@echo "    make docs         - 生成 Sphinx 文档"
	@echo ""
	@echo "  清理命令:"
	@echo "    make clean        - 清理构建产物和缓存文件"
	@echo ""
	@echo "  综合命令:"
	@echo "    make all          - 执行完整检查(格式+测试+构建)"
	@echo ""
	@echo "  帮助:"
	@echo "    make help         - 显示此帮助信息"

# ========== 安装命令 ==========

install:
	@echo "==> 安装项目依赖..."
	$(PIP) install -r requirements.txt
	@echo "==> 安装完成"

install-dev:
	@echo "==> 安装开发依赖..."
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev,docs,animation,report]"
	@echo "==> 开发环境安装完成"

# ========== 运行命令 ==========

run:
	@echo "==> 启动 Streamlit 应用..."
	streamlit run src/frontend/app.py

# ========== 测试命令 ==========

test:
	@echo "==> 运行测试套件..."
	pytest tests/ -v --tb=short

test-cov:
	@echo "==> 运行测试并生成覆盖率报告..."
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html:tests/coverage_html
	@echo "==> 覆盖率报告已生成: tests/coverage_html/index.html"

# ========== 代码检查命令 ==========

lint:
	@echo "==> 执行代码检查..."
	@echo "--> 检查 black 格式..."
	black --check .
	@echo "--> 检查 isort 导入排序..."
	isort --check-only .
	@echo "--> 执行 flake8 静态检查..."
	flake8 src/ tests/
	@echo "--> 执行 mypy 类型检查..."
	mypy src/
	@echo "==> 代码检查全部通过"

lint-fix:
	@echo "==> 自动修复代码格式..."
	black .
	isort .
	@echo "==> 代码格式修复完成"

format:
	@echo "==> 格式化代码..."
	black .
	isort .
	@echo "==> 格式化完成"

check:
	@echo "==> 执行完整代码质量检查..."
	@echo ""
	@echo "[1/4] 检查代码格式..."
	black --check . || (echo "代码格式不符合规范，请运行 'make lint-fix' 修复"; exit 1)
	@echo ""
	@echo "[2/4] 检查导入排序..."
	isort --check-only . || (echo "导入排序不符合规范，请运行 'make lint-fix' 修复"; exit 1)
	@echo ""
	@echo "[3/4] 执行静态检查..."
	flake8 src/ tests/
	@echo ""
	@echo "[4/4] 执行类型检查..."
	mypy src/
	@echo ""
	@echo "==> 全部代码质量检查通过"

# ========== 构建命令 ==========

build:
	@echo "==> 构建 Python 分发包..."
	$(PYTHON) -m build
	@echo "==> 构建完成，产物位于 dist/ 目录"

docs:
	@echo "==> 生成 Sphinx 文档..."
	cd docs && $(MAKE) html
	@echo "==> 文档已生成: docs/_build/html/index.html"

# ========== 清理命令 ==========

clean:
	@echo "==> 清理构建产物..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf tests/coverage_html/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "==> 清理完成"

# ========== 综合命令 ==========

all: format check test build
	@echo ""
	@echo "==> 完整检查流程全部通过"
	@echo "    - 代码已格式化"
	@echo "    - 代码质量检查通过"
	@echo "    - 测试全部通过"
	@echo "    - 构建成功"
