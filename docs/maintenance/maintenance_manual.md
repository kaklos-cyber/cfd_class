# 维护手册

> **文档编号**: CFD-CLASS-MM-001
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
| **分发范围** | 开发团队维护人员 |

---

## 1. 引言

### 1.1 编写目的

本文档为 CFD-Class 软件的维护人员提供系统维护、故障排除、性能优化和版本升级的详细指导。

### 1.2 适用范围

本文档适用于：
- 软件维护工程师
- 系统管理员
- 技术负责人
- 参与后续版本开发的团队成员

### 1.3 参考资料

1. GB/T 8567-2006 计算机软件文档编制规范
2. [SRS.md](../requirements/SRS.md) — 软件需求规格说明书
3. [SDD.md](../design/SDD.md) — 概要设计说明书
4. [architecture.md](../design/architecture.md) — 架构设计详细文档
5. [CONTRIBUTING.md](../../CONTRIBUTING.md) — 贡献者指南

---

## 2. 维护概述

### 2.1 维护范围

| 维护类别 | 内容 | 频率 |
|----------|------|------|
| 日常维护 | 日志检查、性能监控 | 每日 |
| 定期维护 | 依赖更新、数据备份 | 每周 |
| 版本维护 | 功能更新、缺陷修复 | 按需 |
| 应急维护 | 故障排查、紧急修复 | 按需 |

### 2.2 维护人员职责

| 角色 | 职责 |
|------|------|
| 维护负责人 | 统筹维护计划、审批变更、协调资源 |
| 后端维护工程师 | 核心算法维护、性能优化、数值问题排查 |
| 前端维护工程师 | UI 组件维护、交互优化、浏览器兼容性 |
| 测试维护工程师 | 回归测试、测试用例维护、覆盖率监控 |

---

## 3. 系统监控

### 3.1 日志监控

#### 日志位置

| 日志类型 | 位置 | 说明 |
|----------|------|------|
| 应用日志 | 终端标准输出 | Streamlit 运行日志 |
| 错误日志 | 终端标准错误 | Python 异常堆栈 |
| 访问日志 | Streamlit 内部 | 页面访问记录 |

#### 关键日志信息

```
# 正常启动日志
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501

# 模拟运行日志
Running simulation with config: DamBreakConfig(h_L=1.0, h_R=0.0, ...)
Simulation completed in 2.34s

# 错误日志示例
ERROR: ConfigValidationError: h_L must be positive
```

### 3.2 性能监控

#### 监控指标

| 指标 | 正常范围 | 告警阈值 |
|------|----------|----------|
| 单次模拟耗时 (nx=500) | < 5 秒 | > 10 秒 |
| 内存占用峰值 | < 512 MB | > 1 GB |
| CPU 使用率 | < 90% | > 95% |
| 页面加载时间 | < 3 秒 | > 5 秒 |

#### 性能检查命令

```bash
# 查看 Python 进程资源占用
ps aux | grep streamlit

# 实时监控内存和 CPU
top -p $(pgrep -f "streamlit")

# 使用 pytest-benchmark 进行性能测试
pytest tests/benchmark/ -v
```

---

## 4. 故障诊断与排除

### 4.1 故障分级

| 级别 | 描述 | 响应时间 | 处理要求 |
|------|------|----------|----------|
| P0 - 紧急 | 系统崩溃、数据丢失 | 1 小时内 | 立即修复 |
| P1 - 高 | 核心功能不可用 | 4 小时内 | 优先修复 |
| P2 - 中 | 非核心功能异常 | 1 个工作日内 | 计划修复 |
| P3 - 低 | 界面显示问题、优化建议 | 下一版本 | 排期处理 |

### 4.2 常见故障处理

#### 故障 1：软件无法启动

**现象**：执行启动命令后无响应或报错

**排查步骤**：
1. 检查 Python 版本：`python --version`（需 >= 3.10）
2. 检查虚拟环境是否激活
3. 检查依赖是否完整：`pip list | grep streamlit`
4. 检查端口占用：`lsof -i :8501`（Linux/macOS）或 `netstat -ano | findstr :8501`（Windows）

**解决方案**：
```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 更换端口启动
streamlit run src/frontend/app.py --server.port 8502
```

#### 故障 2：模拟运行崩溃

**现象**：点击"开始模拟"后程序报错或卡死

**排查步骤**：
1. 检查终端错误输出
2. 检查参数是否在合法范围内
3. 检查 CFL 数是否过大（建议 <= 0.9）
4. 检查网格数是否过多（建议 nx <= 2000）

**解决方案**：
- 降低 CFL 数到 0.5 以下测试
- 减少同时运行的格式数量
- 检查是否有除零错误（h_L 或 h_R 是否为 0）

#### 故障 3：数值结果异常

**现象**：模拟完成但结果明显不合理（如负水深、激波位置错误）

**排查步骤**：
1. 对比精确解验证
2. 检查边界条件设置
3. 检查格式实现是否正确
4. 检查正性保持机制是否生效

**解决方案**：
- 启用正性保持：`EPS_H = 1e-12`
- 检查 Riemann 求解器收敛性
- 验证通量计算正确性

#### 故障 4：内存溢出

**现象**：运行大规模模拟时系统内存不足

**排查步骤**：
1. 监控内存使用：`free -h`（Linux）或活动监视器（macOS）
2. 检查网格数和格式数量
3. 检查是否同时运行多个模拟

**解决方案**：
- 减少网格数（nx <= 1000）
- 减少同时运行的格式数量
- 增加系统内存或交换空间
- 启用结果缓存清理

#### 故障 5：中文显示异常

**现象**：界面或图表中文字符显示为方框或乱码

**排查步骤**：
1. 检查系统是否安装中文字体
2. 检查 Matplotlib 字体配置
3. 检查浏览器编码设置

**解决方案**：
```bash
# Linux 安装中文字体
sudo apt-get install fonts-wqy-zenhei

# 清除 Matplotlib 字体缓存
rm -rf ~/.cache/matplotlib
```

### 4.3 故障报告模板

```markdown
## 故障报告

**故障编号**: BUG-YYYY-MM-DD-NNN
**报告人**: 
**报告日期**: 
**故障级别**: P0/P1/P2/P3

### 故障描述
简要描述故障现象

### 复现步骤
1. 步骤一
2. 步骤二
3. 步骤三

### 预期结果
描述正常情况下的预期行为

### 实际结果
描述实际观察到的异常行为

### 环境信息
- 操作系统: 
- Python 版本: 
- 软件版本: 
- 浏览器: 

### 错误日志
```
粘贴相关错误日志
```

### 附件
- 截图
- 相关数据文件
```

---

## 5. 数据备份与恢复

### 5.1 备份内容

| 备份项 | 路径 | 备份频率 |
|--------|------|----------|
| 源代码 | `src/` | 每次发布前 |
| 文档 | `docs/` | 每次发布前 |
| 测试数据 | `tests/` | 每次发布前 |
| 配置文件 | `requirements.txt`, `pyproject.toml` | 每次变更后 |
| 用户导出数据 | 浏览器下载目录 | 用户自行管理 |

### 5.2 备份方法

#### Git 备份

```bash
# 创建备份分支
git checkout -b backup/YYYY-MM-DD

# 推送至远程
git push origin backup/YYYY-MM-DD
```

#### 归档备份

```bash
# 创建压缩包
tar -czvf cfd-class-backup-YYYY-MM-DD.tar.gz \
  src/ docs/ tests/ requirements.txt pyproject.toml
```

### 5.3 恢复方法

```bash
# 从 Git 恢复
git checkout backup/YYYY-MM-DD

# 从压缩包恢复
tar -xzvf cfd-class-backup-YYYY-MM-DD.tar.gz
```

---

## 6. 版本升级

### 6.1 升级前检查

| 检查项 | 方法 |
|--------|------|
| 当前版本 | `git describe --tags` |
| 依赖版本 | `pip list` |
| 测试通过率 | `pytest tests/ -v` |
| 代码覆盖率 | `pytest --cov=src` |

### 6.2 升级步骤

#### 小版本升级（补丁修复）

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 更新依赖
pip install -r requirements.txt --upgrade

# 3. 运行测试
pytest tests/ -v

# 4. 启动验证
streamlit run src/frontend/app.py
```

#### 大版本升级（功能更新）

```bash
# 1. 备份当前版本
git tag backup-before-vX.Y.Z
git push origin backup-before-vX.Y.Z

# 2. 拉取新版本
git fetch origin
git checkout vX.Y.Z

# 3. 重建虚拟环境
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 4. 安装新依赖
pip install -r requirements.txt

# 5. 运行完整测试
pytest tests/ -v --cov=src

# 6. 验证功能
streamlit run src/frontend/app.py
```

### 6.3 回滚步骤

```bash
# 1. 停止当前服务
Ctrl + C

# 2. 切换到备份版本
git checkout backup/YYYY-MM-DD

# 3. 恢复依赖
pip install -r requirements.txt --force-reinstall

# 4. 重新启动
streamlit run src/frontend/app.py
```

---

## 7. 性能优化

### 7.1 计算性能优化

| 优化项 | 方法 | 预期效果 |
|--------|------|----------|
| 向量化运算 | 使用 NumPy 数组操作替代 Python 循环 | 10-100 倍加速 |
| 缓存精确解 | 使用 `@st.cache_data` 缓存 Riemann 精确解 | 减少重复计算 |
| 并行计算 | 使用 `multiprocessing` 并行运行多格式 | 线性加速 |
| 减少快照频率 | 增大快照记录间隔 | 降低内存占用 |

### 7.2 内存优化

| 优化项 | 方法 | 预期效果 |
|--------|------|----------|
| 数组复用 | 预分配数组避免重复创建 | 减少 GC 压力 |
| 及时释放 | 使用 `del` 释放大数组 | 降低峰值内存 |
| 生成器模式 | 动画使用生成器逐帧处理 | 流式处理 |

### 7.3 前端性能优化

| 优化项 | 方法 | 预期效果 |
|--------|------|----------|
| 缓存数据 | 使用 `st.cache_data` | 减少重复计算 |
| 延迟加载 | 分页加载大数据表格 | 加快页面响应 |
| 图表优化 | 降低 Matplotlib DPI | 减少渲染时间 |

---

## 8. 安全维护

### 8.1 依赖安全

```bash
# 检查依赖漏洞
pip install safety
safety check -r requirements.txt

# 更新有漏洞的依赖
pip install <package> --upgrade
```

### 8.2 代码安全

| 检查项 | 工具 | 频率 |
|--------|------|------|
| 静态安全分析 | bandit | 每次提交 |
| 密钥泄露检测 | git-secrets | 每次提交 |
| 依赖漏洞扫描 | safety | 每周 |

### 8.3 访问控制

- 生产环境限制访问 IP
- 定期更换部署密钥
- 监控异常访问日志

---

## 9. 维护记录

### 9.1 维护日志模板

```markdown
## 维护记录

**维护日期**: YYYY-MM-DD
**维护人员**: 
**维护类型**: 日常/定期/版本/应急

### 维护内容
描述本次维护的具体内容

### 变更清单
- [ ] 变更项 1
- [ ] 变更项 2

### 测试结果
- 单元测试: 通过/失败 (X/Y)
- 集成测试: 通过/失败 (X/Y)
- 覆盖率: XX%

### 遗留问题
描述未解决的问题及计划

### 下次维护计划
YYYY-MM-DD - 维护内容
```

---

## 10. 附录

### 10.1 维护工具清单

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| pytest | 测试框架 | `pip install pytest` |
| pytest-cov | 覆盖率 | `pip install pytest-cov` |
| pytest-benchmark | 性能测试 | `pip install pytest-benchmark` |
| black | 代码格式化 | `pip install black` |
| flake8 | 静态检查 | `pip install flake8` |
| mypy | 类型检查 | `pip install mypy` |
| safety | 安全扫描 | `pip install safety` |
| bandit | 安全分析 | `pip install bandit` |

### 10.2 紧急联系信息

| 角色 | 联系人 | 职责 |
|------|--------|------|
| 维护负责人 | @PM | 统筹维护工作 |
| 技术负责人 | @Arch | 技术决策支持 |
| 后端支持 | @BE | 算法问题排查 |
| 前端支持 | @FE | UI 问题排查 |

### 10.3 维护检查表

#### 每日检查
- [ ] 检查应用日志是否有异常
- [ ] 检查系统资源使用情况
- [ ] 检查用户反馈

#### 每周检查
- [ ] 运行完整测试套件
- [ ] 检查代码覆盖率
- [ ] 检查依赖安全漏洞
- [ ] 备份重要数据

#### 每月检查
- [ ] 审查维护日志
- [ ] 评估性能指标
- [ ] 更新文档
- [ ] 制定下月维护计划

---

## 版本历史

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-05-15 | 初始版本，建立维护手册 | @TW |

---

*文档结束*
