# CFD-Class 版本历史

> **文档编号**: CFD-CLASS-VH-001
> **版本**: v1.0
> **日期**: 2026-05-15
> **状态**: 正式版
> **维护者**: @PM (@TW协助)

---

## 文档控制信息

| 项目 | 内容 |
|------|------|
| **软件名称** | CFD-Class 一维溃坝CFD教学软件 |
| **文档作者** | @TW (文档工程师) |
| **审核人** | @PM (项目经理) |
| **批准人** | @PM (项目经理) |
| **分发范围** | 全体开发团队成员、用户 |

---

## 1. 版本号规范说明

本项目严格遵循 [语义化版本控制 2.0.0](https://semver.org/lang/zh-CN/spec/v2.0.0.html) 规范，版本号格式为：

```
vMAJOR.MINOR.PATCH[-prerelease[.N]]
```

### 1.1 版本号组成

| 组成部分 | 说明 | 递增规则 |
|---------|------|---------|
| `MAJOR` | 主版本号 | 进行不兼容的 API 修改时递增 |
| `MINOR` | 次版本号 | 向下兼容的功能性新增时递增 |
| `PATCH` | 修订号 | 向下兼容的问题修复时递增 |
| `prerelease` | 预发布标识 | alpha(内测) / beta(公测) / rc(候选) |
| `N` | 预发布修订号 | 同一预发布阶段的迭代次数 |

### 1.2 预发布阶段定义

| 阶段 | 标识 | 说明 | 使用场景 |
|------|------|------|---------|
| 内测版 | `alpha` | 功能未完成，内部测试 | 开发团队内部验证 |
| 公测版 | `beta` | 功能基本完成，外部测试 | 邀请用户参与测试 |
| 候选版 | `rc` | 发布候选，仅修复Bug | 发布前的最终验证 |
| 正式版 | 无标识 | 经过充分验证，可交付 | 对外正式发布 |

### 1.3 版本号示例

| 版本号 | 含义 | 阶段 |
|--------|------|------|
| v0.1.0-alpha | 初始框架版本 | 内测 |
| v0.1.0-alpha.1 | 框架版本第一次修订 | 内测 |
| v0.2.0-alpha | 核心算法实现 | 内测 |
| v0.5.0-beta | 完整功能公测 | 公测 |
| v1.0.0-rc.1 | 正式版候选1 | 候选 |
| v1.0.0 | 首个正式版 | 正式 |
| v1.1.0 | 功能更新 | 正式 |
| v1.1.1 | Bug修复 | 正式 |

---

## 2. 版本发布记录

### 2.1 v0.1.0-alpha.1 (当前版本)

- **发布日期**: 2026-05-15
- **代号**: Foundation
- **状态**: 预发布 (Alpha)
- **负责人**: @PM

#### 变更摘要

**新增**:
- 产品交付清单 (`DELIVERY_CHECKLIST.md`)
- 发布说明 (`RELEASE_NOTES.md`)
- 版本历史文档 (`docs/maintenance/version_history.md`)
- Makefile 常用命令封装
- README.md 文档索引和项目徽章

**变更**:
- 版本号从 `v0.1.0-alpha` 更新为 `v0.1.0-alpha.1`
- 统一所有文档的版本标识

#### 交付物状态

| 类别 | 完成率 | 关键交付物 |
|------|--------|-----------|
| 源代码 | 11% | 目录结构、配置模块 |
| 文档 | 83% | SRS、SDD、用户手册、测试计划等 |
| 测试 | 33% | 测试计划、目录结构 |
| 部署 | 71% | CI/CD、pyproject.toml、Makefile |

---

### 2.2 v0.1.0-alpha

- **发布日期**: 2026-05-07
- **代号**: Genesis
- **状态**: 初始框架
- **负责人**: @PM

#### 变更摘要

**新增**:
- 完整的GB/T标准目录结构
- README.md - 项目介绍与快速开始
- CONTRIBUTING.md - 团队协作规范指南
- SRS.md - 软件需求规格说明书(框架版)
- SDD.md - 概要设计说明书(框架版)
- user_manual.md - 用户操作手册
- quick_start.md - 快速入门指南
- theory_guide.md - 理论背景指南
- test_plan.md - 测试计划(含60+测试用例)
- CI/CD流水线配置 (lint + test + security + build)
- GitHub Issue模板 (Bug/Feature/Document)
- PR模板与Checklist
- Python包结构 (src/core/ src/frontend/ tests/)
- pyproject.toml 项目元数据配置
- .gitignore 标准化忽略规则
- PRODUCT_DELIVERY_STANDARD.md 产品交付规范
- GITHUB_COLLABORATION_GUIDE.md GitHub协作指南
- CHANGELOG.md 变更日志
- LICENSE MIT开源许可证

**技术债务**:
- 核心算法代码待迁移 (KuiBa → CFD_class标准化重构)
- Streamlit UI页面待实现
- 单元测试用例待编写 (目标覆盖率≥80%)
- 示例案例库待建立

**已知限制**:
- 当前仅为框架阶段，无实际可运行功能
- 文档为框架版，需后续补充详细内容
- CI/CD尚未经过实际push验证

---

## 3. 版本路线图

### 3.1 短期计划 (Alpha阶段)

| 版本 | 预计日期 | 目标 | 关键交付物 |
|------|---------|------|-----------|
| v0.1.0-alpha.1 | 2026-05-15 | ✅ 基础设施完善 | 交付清单、发布说明、Makefile |
| v0.2.0-alpha | 待定 | 核心算法实现 | 6种FVM格式、Riemann求解器、误差分析 |
| v0.3.0-alpha | 待定 | UI界面开发 | Streamlit 4页面、交互功能、动画引擎 |
| v0.4.0-alpha | 待定 | 报告与测试 | HTML报告生成器、完整测试覆盖、回归基准 |

### 3.2 中期计划 (Beta阶段)

| 版本 | 预计日期 | 目标 | 关键交付物 |
|------|---------|------|-----------|
| v0.5.0-beta | 待定 | 完整功能公测 | 全部功能可用、文档完善、性能优化 |
| v0.6.0-beta | 待定 | 用户反馈迭代 | Bug修复、UX改进、新增预设案例 |
| v0.7.0-beta | 待定 | 稳定性提升 | 长时间运行稳定、边缘情况处理 |

### 3.3 长期计划 (正式版)

| 版本 | 预计日期 | 目标 | 关键交付物 |
|------|---------|------|-----------|
| v1.0.0-rc.1 | 待定 | 发布候选 | 仅修复关键Bug |
| v1.0.0 | 待定 | 首个正式版 | 教学可用、文档齐全、质量达标 |
| v1.1.0 | 待定 | 功能增强 | 新增格式、增强可视化 |
| v2.0.0 | 待定 | 架构升级 | 可能的不兼容API变更 |

---

## 4. 版本变更详细记录

### 4.1 按版本分类

#### v0.1.0-alpha.1 (2026-05-15)

| 类型 | 内容 | 作者 |
|------|------|------|
| 新增 | DELIVERY_CHECKLIST.md - GB/T标准产品交付清单 | @PM/@TW |
| 新增 | RELEASE_NOTES.md - v0.1.0-alpha.1发布说明 | @PM |
| 新增 | docs/maintenance/version_history.md - 版本历史 | @TW |
| 新增 | Makefile - 常用开发命令封装 | @Arch |
| 更新 | README.md - 添加文档索引、项目徽章 | @TW |
| 更新 | VERSION - 更新为 v0.1.0-alpha.1 | @PM |
| 更新 | pyproject.toml - 版本号同步 | @Arch |

#### v0.1.0-alpha (2026-05-07)

| 类型 | 内容 | 作者 |
|------|------|------|
| 新增 | 完整仓库目录结构 | @Arch |
| 新增 | docs/requirements/SRS.md | @PM/@TW |
| 新增 | docs/design/SDD.md | @Arch |
| 新增 | docs/design/architecture.md | @Arch |
| 新增 | docs/user/user_manual.md | @TW |
| 新增 | docs/user/quick_start.md | @TW |
| 新增 | docs/user/theory_guide.md | @TW |
| 新增 | docs/test/test_plan.md | @QA |
| 新增 | docs/maintenance/changelog.md | @TW |
| 新增 | .github/workflows/ci.yml | @Arch |
| 新增 | .github/workflows/cd.yml | @Arch |
| 新增 | .github/ISSUE_TEMPLATE/ | @PM |
| 新增 | .github/PULL_REQUEST_TEMPLATE.md | @PM |
| 新增 | CONTRIBUTING.md | @PM/@TW |
| 新增 | PRODUCT_DELIVERY_STANDARD.md | @PM/@TW |
| 新增 | GITHUB_COLLABORATION_GUIDE.md | @PM |
| 新增 | README.md | @TW |
| 新增 | pyproject.toml | @Arch |
| 新增 | requirements.txt | @BE |
| 新增 | LICENSE | @PM |

---

## 5. 版本兼容性矩阵

### 5.1 向后兼容性

| 版本范围 | 兼容性保证 | 说明 |
|---------|-----------|------|
| v0.x.x-alpha | ❌ 不保证 | 快速迭代，API可能大幅变更 |
| v0.x.x-beta | ⚠️ 尽力保证 | 主要功能稳定，次要接口可能调整 |
| v1.0.0+ | ✅ 保证 | 遵循SemVer，Minor版本向下兼容 |

### 5.2 数据格式兼容性

| 版本 | 配置文件 | 报告格式 | 基准数据 |
|------|---------|---------|---------|
| v0.1.0-alpha.1 | 无 | 无 | 无 |
| v0.2.0-alpha+ | 计划支持JSON/YAML配置 | 计划支持HTML报告 | 计划支持CSV/NumPy格式 |

---

## 6. 版本维护策略

### 6.1 维护周期

| 版本类型 | 活跃维护期 | 安全更新期 | 终止支持 |
|---------|-----------|-----------|---------|
| Alpha | 至下个Alpha发布 | 无 | Beta发布时 |
| Beta | 至正式版发布 | 无 | RC发布时 |
| 正式版 (Minor) | 6个月 | 12个月 | 下个Minor发布+6个月 |
| 正式版 (Major) | 12个月 | 24个月 | 下个Major发布+12个月 |

### 6.2 版本分支策略

```
main          ●────●────●────●────●────●────●
              ↑    ↑    ↑    ↑    ↑    ↑
             v0.1  v0.2 v0.5 v1.0 v1.1 v2.0

develop       ●────●────●────●────●────●
              ↑         ↑         ↑
           alpha.1   alpha.3   beta.1

release/vX.Y  ●────● (仅正式版创建release分支)
```

---

## 7. 附录

### 7.1 相关文档链接

| 文档 | 路径 | 说明 |
|------|------|------|
| 变更日志 | [changelog.md](./changelog.md) | 详细变更记录 |
| 发布说明 | [RELEASE_NOTES.md](../../RELEASE_NOTES.md) | 当前版本发布说明 |
| 交付清单 | [DELIVERY_CHECKLIST.md](../../DELIVERY_CHECKLIST.md) | 产品交付清单 |
| 产品交付规范 | [PRODUCT_DELIVERY_STANDARD.md](../../PRODUCT_DELIVERY_STANDARD.md) | 交付标准与流程 |

### 7.2 版本查询命令

```bash
# 查看当前版本
cat VERSION

# 查看Git标签
git tag -l

# 查看当前分支最新提交
git log --oneline -1

# 查看版本历史
git log --oneline --decorate
```

---

## 版本历史

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-05-15 | 初始版本，建立完整的版本历史文档，包含版本号规范、发布记录、路线图、兼容性矩阵和维护策略 | @TW |

---

*文档结束*
