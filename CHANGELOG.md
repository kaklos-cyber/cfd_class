# Changelog

All notable changes to the CFD-Class project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0-alpha.2] - 2026-05-21

### Added
- 重新打包产品交付包，版本更新为 v0.1.0-alpha.2
- 完善软件包元数据和构建配置
- 清理构建产物，确保干净的打包环境

### Changed
- 更新版本号至 v0.1.0-alpha.2
- 优化 pyproject.toml 构建配置

## [0.1.0-alpha.1] - 2026-05-15

### Added
- GB/T标准文档体系完善：新增安装手册、操作手册、维护手册、测试报告模板、项目开发计划、项目状态报告
- 文档导航索引 (`docs/README.md`)：提供完整的文档清单和使用指南
- 统一文档编号体系 (CFD-CLASS-XXX-NNN)：所有20份文档均获得标准编号
- 统一文档控制信息：所有文档补充作者、审核人、批准人、分发范围

### Changed
- 统一所有文档版本为 v1.0，日期统一为 2026-05-15
- 统一文档格式为 GB/T 8567-2006 标准格式
- 更新所有文档的交叉引用链接

### Fixed
- 修复文档间交叉引用路径
- 修正文档编号不一致问题

## [0.1.0-alpha] - 2026-05-07

### Added
- Project initialization with standardized structure
- Core documentation per GB/T 8567-2006 standard
- GitHub Actions CI/CD pipeline configuration
- Issue and Pull Request templates for team collaboration
- Python 3.10+ support with type annotations
- MIT License

### To Do (Future Releases)
- Implement 6 FVM numerical schemes (LF, LW, MC, Godunov, HLL, MUSCL-Hancock)
- Develop Streamlit-based UI with 4 main pages (Home, Simulation, Animation, Report)
- Create exact Riemann solver for validation
- Add unit tests with ≥80% coverage
- Build example cases library
- Generate HTML reports for comparative analysis
