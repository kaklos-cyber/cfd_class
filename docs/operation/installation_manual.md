# 安装手册

> **文档编号**: CFD-CLASS-IM-001
> **版本**: v1.0
> **日期**: 2026-05-15
> **适用软件版本**: v0.1.0-alpha.1
> **依据标准**: GB/T 8567-2006 计算机软件文档编制规范

---

## 文档控制信息

| 项目 | 内容 |
|------|------|
| **软件名称** | CFD-Class 一维溃坝CFD教学软件 |
| **文档作者** | @TW (文档工程师) |
| **审核人** | @Arch (架构师) |
| **批准人** | @PM (项目经理) |
| **分发范围** | 全体开发团队成员、最终用户 |

---

## 1. 引言

### 1.1 编写目的

本文档为 CFD-Class 软件提供详细的安装指导，确保用户能够在不同操作系统环境下正确完成软件的安装与配置。

### 1.2 适用范围

本文档适用于以下用户：
- 首次安装 CFD-Class 的最终用户
- 需要在多台机器上部署软件的系统管理员
- 需要搭建开发环境的贡献者

### 1.3 参考资料

1. GB/T 8567-2006 计算机软件文档编制规范
2. [SRS.md](../requirements/SRS.md) — 软件需求规格说明书
3. [user_manual.md](../user/user_manual.md) — 用户操作手册
4. [CONTRIBUTING.md](../../CONTRIBUTING.md) — 贡献者指南

---

## 2. 安装概述

### 2.1 软件简介

CFD-Class 是一款面向流体力学专业学生的一维溃坝问题数值模拟教学软件，基于 Python 3.10+ 和 Streamlit 框架开发。

### 2.2 安装方式概览

| 安装方式 | 适用场景 | 难度 | 预计时间 |
|----------|----------|------|----------|
| 源码安装 | 开发者、高级用户 | 中等 | 10-15分钟 |
| Docker 部署 | 快速体验、服务器部署 | 简单 | 5-10分钟 |
| 虚拟环境安装 | 普通用户（推荐） | 简单 | 10分钟 |

---

## 3. 系统要求

### 3.1 硬件要求

| 项目 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 双核处理器 | 四核及以上 |
| 内存 | 4GB RAM | 8GB RAM |
| 硬盘空间 | 500MB 可用空间 | 1GB 可用空间 |
| 显示器 | 分辨率 1366×768 | 分辨率 1920×1080 |

### 3.2 软件环境要求

| 项目 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.10 | 3.10 或 3.11 |
| pip | 23.0 | 最新版 |
| Git | 2.30 | 最新版 |
| 操作系统 | Windows 10 / macOS 12 / Ubuntu 20.04 | Windows 11 / macOS 14 / Ubuntu 22.04 |

### 3.3 浏览器要求

| 浏览器 | 最低版本 |
|--------|----------|
| Google Chrome | 120+ |
| Mozilla Firefox | 121+ |
| Microsoft Edge | 120+ |
| Apple Safari | 17+ |

---

## 4. 安装前准备

### 4.1 检查 Python 版本

```bash
python --version
# 或
python3 --version
```

输出应显示 `Python 3.10.x` 或更高版本。如果未安装或版本过低，请访问 [python.org](https://www.python.org/downloads/) 下载安装。

### 4.2 检查 pip 版本

```bash
pip --version
# 或
pip3 --version
```

### 4.3 检查 Git 版本

```bash
git --version
```

### 4.4 网络环境

确保网络连接正常，能够访问以下资源：
- GitHub (克隆仓库)
- PyPI (安装 Python 依赖包)

---

## 5. 安装步骤

### 5.1 方式一：源码安装（推荐开发者）

#### 步骤 1：克隆仓库

```bash
git clone https://github.com/kaklos-cyber/cfd_class.git
cd cfd_class
```

#### 步骤 2：创建虚拟环境

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 步骤 3：安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 步骤 4：验证安装

```bash
python -c "from src.core import DamBreakConfig; print('✅ 环境检查通过')"
```

#### 步骤 5：启动应用

```bash
streamlit run src/frontend/app.py
```

浏览器将自动打开 `http://localhost:8501`。

### 5.2 方式二：Docker 部署

#### 前提条件

已安装 Docker Engine 24.0+ 和 Docker Compose 2.20+。

#### 步骤 1：克隆仓库

```bash
git clone https://github.com/kaklos-cyber/cfd_class.git
cd cfd_class
```

#### 步骤 2：构建 Docker 镜像

```bash
docker build -t cfd-class .
```

#### 步骤 3：运行容器

```bash
docker run -p 8501:8501 --name cfd-class-app cfd-class
```

#### 步骤 4：访问应用

在浏览器中打开 `http://localhost:8501`。

#### 后台运行模式

```bash
docker run -d -p 8501:8501 --name cfd-class-app cfd-class
```

#### 停止容器

```bash
docker stop cfd-class-app
```

### 5.3 方式三：虚拟环境快速安装

#### 步骤 1：下载发布包

从 GitHub Releases 页面下载最新版本的源码压缩包并解压。

#### 步骤 2：创建并激活虚拟环境

```bash
cd cfd_class
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

#### 步骤 3：安装并运行

```bash
pip install -r requirements.txt
streamlit run src/frontend/app.py
```

---

## 6. 安装后配置

### 6.1 首次启动配置

首次启动时，Streamlit 可能会提示收集使用统计数据。教学软件建议禁用：

```bash
streamlit config show
```

在 `~/.streamlit/config.toml` 中添加：

```toml
[browser]
gatherUsageStats = false
```

### 6.2 中文字体配置（Linux）

如果在 Linux 环境下图表中文显示异常，请安装中文字体：

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y fonts-wqy-zenhei

# CentOS/RHEL
sudo yum install -y wqy-zenhei-fonts
```

### 6.3 防火墙配置

如果需要通过局域网访问，请确保防火墙允许 8501 端口：

```bash
# Ubuntu (UFW)
sudo ufw allow 8501/tcp

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

---

## 7. 验证安装

### 7.1 功能验证清单

| 验证项 | 操作方法 | 预期结果 |
|--------|----------|----------|
| 首页加载 | 访问 `http://localhost:8501` | 显示 CFD-Class 首页 |
| 理论背景显示 | 点击左侧"🏠 首页" | 显示浅水方程推导 |
| 模拟运行 | 进入"📊 模拟"页面，点击"▶ 开始模拟" | 显示水深剖面图和误差表格 |
| 动画生成 | 进入"🎬 动画"页面，点击"生成动画" | 生成并显示 GIF 动画 |
| 报告生成 | 进入"📝 报告"页面，点击"生成报告" | 生成 HTML 报告 |

### 7.2 常见问题排查

| 问题现象 | 可能原因 | 解决方法 |
|----------|----------|----------|
| `ModuleNotFoundError` | 依赖未安装完整 | 重新运行 `pip install -r requirements.txt` |
| 端口被占用 | 8501 端口被其他程序占用 | 更换端口：`streamlit run src/frontend/app.py --server.port 8502` |
| 中文显示乱码 | 缺少中文字体 | 安装中文字体包 |
| 页面加载缓慢 | 首次编译缓存 | 等待 1-2 分钟，刷新页面 |
| 模拟运行报错 | 参数超出范围 | 检查参数设置是否在允许范围内 |

---

## 8. 卸载

### 8.1 源码安装卸载

```bash
# 停用虚拟环境
deactivate

# 删除项目目录
cd ..
rm -rf cfd_class

# 删除虚拟环境（可选）
rm -rf .venv
```

### 8.2 Docker 卸载

```bash
# 停止并删除容器
docker stop cfd-class-app
docker rm cfd-class-app

# 删除镜像
docker rmi cfd-class
```

---

## 9. 附录

### 9.1 依赖包清单

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| streamlit | >=1.28.0, <2.0.0 | Web 应用框架 |
| numpy | >=1.24.0, <2.0.0 | 数值计算 |
| scipy | >=1.10.0, <2.0.0 | 科学计算 |
| matplotlib | >=3.7.0, <4.0.0 | 数据可视化 |
| pillow | >=10.0.0, <11.0.0 | 图像处理 |
| jinja2 | >=3.1.0, <4.0.0 | 模板引擎 |

### 9.2 安装日志示例

```
$ streamlit run src/frontend/app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### 9.3 获取帮助

如在安装过程中遇到问题，请通过以下方式获取帮助：
1. 查阅 [用户操作手册](../user/user_manual.md) 的 FAQ 章节
2. 在 GitHub 提交 Issue: https://github.com/kaklos-cyber/cfd_class/issues
3. 联系项目维护团队

---

## 版本历史

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-05-15 | 初始版本，建立安装手册 | @TW |

---

*文档结束*
