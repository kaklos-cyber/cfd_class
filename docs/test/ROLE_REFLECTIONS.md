# CFD-Class 项目各角色收获与体会

---

## 1. PM (项目经理)

### 收获
- **流程管控经验**: 通过PR审核机制（#29的REQUEST_CHANGES），学会了如何在代码冲突时果断要求rebase，避免技术债务累积
- **跨角色协调能力**: 协调FE、BE、QA三方工作，确保PR#28、PR#31、fix-test-framework-rebase分支有序合并
- **质量标准建立**: 制定了"纯测试PR"原则，明确区分功能代码与测试代码的提交规范

### 体会
- "代码冲突不是技术问题，是流程问题。提前定义好分支策略（Git Flow）比事后解决冲突更重要"
- "45/100的评分虽然严厉，但让团队明白了'rebase到develop'不是可选项而是必选项"
- "Issue #19-#21与#25-#27的重复说明需求管理需要更严格的去重机制"

---

## 2. Arch (架构师)

### 收获
- **MVC架构验证**: 验证了前端（Streamlit）+ 后端（NumPy/SciPy）+ 核心引擎的分层设计可以支撑9种FVM格式+3种Riemann求解器
- **API设计教训**: `get_scheme()`工厂函数的缺失暴露了"后端开发不考虑前端调用方式"的问题，后续需要在架构层面定义公共API层
- **扩展性验证**: MUSCL-Hancock等复杂格式的接入证明了`BaseScheme`抽象类的设计合理性

### 体会
- "架构不是画出来的，是测出来的。QA的前后端集成测试让我发现了HLL vs HLLScheme这种命名不一致"
- "`evolve()` vs `run_simulation()`的方法名分歧说明架构文档必须包含API契约"
- "1274行专业测试不是负担，是架构正确性的证明"

---

## 3. FE (前端开发)

### 收获
- **API适配经验**: 学会了如何通过参数映射（`L→domain_length`）和适配器模式（`ExactRiemann`包装`ExactRiemannSolver`）解决前后端不匹配
- **Streamlit工程化**: 掌握了多页面结构（pages/目录）、session_state管理、以及如何避免循环导入（`pages/__init__.py`的教训）
- **防御式编程**: 从"假设后端API稳定"转变为"添加try-except和参数校验"

### 体会
- "我以为`from src.core.schemes import HLL`是对的，直到QA的测试报ImportError。原来后端叫HLLScheme"
- "`pages/__init__.py`里的`from .pages import *`让我花了2小时 debug 循环导入，以后再也不写这种代码了"
- "前端参数用`h_L`而后端用`h_l`，这种大小写差异在代码审查时很难发现，需要自动化测试兜底"

---

## 4. BE (后端开发)

### 收获
- **工厂模式实践**: 为9种FVM格式实现了`get_scheme()`和`get_all_schemes()`，支持大小写不敏感的名称匹配
- **向后兼容设计**: 通过类名别名（`HLL = HLLScheme`）和`evolve()`方法，在不破坏原有API的前提下支持前端调用
- **求解器封装**: 创建了`ExactRiemann`适配器类，将底层`ExactRiemannSolver`的复杂接口包装为前端友好的形式

### 体会
- "我写`run_simulation(h0, u0, cfl, dx, t_end)`时没考虑前端会传一个config对象。`evolve(config)`的添加让我理解了'面向调用者设计'"
- "`_SCHEME_REGISTRY`字典虽然简单，但解决了前端'我想用字符串名称获取格式实例'的需求"
- "后端不应该假设前端知道所有参数名。`DamBreakConfig`的`from_dict()`方法需要更健壮的参数过滤"

---

## 5. QA (测试/质量保证 - 本角色)

### 收获
- **测试金字塔实践**: 从单元测试（82个）→集成测试（43个）→回归防护（10个）→Smoke测试（16个），建立了完整的测试体系
- **前后端集成测试**: 发现了6类API不匹配问题（类名、方法名、参数名、导入路径、工厂函数、循环导入），证明了"单元测试各自通过不代表集成能工作"
- **Git工作流**: 学会了rebase、解决冲突、以及如何在"不修改src/core/"的约束下完成测试任务

### 体会
- "PM要求'删除所有src/core/文件'时，我最初不理解。后来明白develop已有PR#31的更好实现，我的重复代码是技术债务"
- "`test_frontend_hll_class_name_mismatch`这个测试从'验证bug存在'改为'验证bug已修复'，让我理解了测试的生命周期"
- "177个测试0失败不是终点。当FE修复了API后，我的测试也需要更新——测试代码也是代码，需要维护"
- "性能测试中的`@pytest.mark.slow`让我学会了如何区分CI快速测试和本地完整测试"

---

## 6. DevOps (运维/部署)

### 收获
- **CI/CD配置**: 配置了pytest自动化测试流水线，支持`-m "not slow"`快速模式和完整模式
- **分支管理**: 管理了`main`→`develop`→`feature/fix`的多级分支结构，确保PR#28、PR#31、fix-test-framework-rebase有序合并
- **环境一致性**: 解决了Streamlit依赖缺失导致的Smoke测试跳过问题，明确了生产环境依赖清单

### 体会
- "QA的`fix-test-framework-rebase`分支推送到远程时，我检查了commit历史——3个清晰的commit比1个巨大的commit更容易回滚"
- "`pyproject.toml`中的pytest配置需要注册自定义mark（如`slow`），否则会有PytestUnknownMarkWarning"
- "前端修复分支`fix/frontend-backend-api-alignment`和我的测试分支合并时，需要确保测试文件不被覆盖——这是CI流水线需要防范的"

---

## 团队协作总结

| 角色 | 核心贡献 | 关键教训 |
|------|----------|----------|
| PM | 流程管控、质量标准 | 严厉的审核（45/100）比放任更能提升质量 |
| Arch | MVC架构、API契约 | 架构文档必须包含调用示例 |
| FE | 前端页面、参数映射 | 不要假设后端API符合你的预期 |
| BE | 核心引擎、工厂函数 | 面向调用者设计API |
| QA | 177个测试、bug文档化 | 测试需要随代码进化而更新 |
| DevOps | CI/CD、分支管理 | Commit清晰度和环境一致性同样重要 |

---

*文档版本: v1.0*
*日期: 2026-05-13*
*作者: CFD-Class Team*
