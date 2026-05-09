"""
Pytest 全局配置和共享 fixtures

依据: test_plan.md (CFD-CLASS-TP-001)
角色: @QA
"""

from typing import Callable, Dict, List, Optional

import numpy as np
import pytest
from numpy.typing import NDArray


# ---------------------------------------------------------------------------
# 路径配置
# ---------------------------------------------------------------------------
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# ---------------------------------------------------------------------------
# 自定义标记
# ---------------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "scheme: marks tests related to numerical schemes")
    config.addinivalue_line("markers", "solver: marks tests related to Riemann solvers")
    config.addinivalue_line("markers", "config: marks tests related to configuration")
    config.addinivalue_line("markers", "integration: marks integration tests")
    config.addinivalue_line("markers", "performance: marks performance/benchmark tests")
    config.addinivalue_line("markers", "regression: marks regression tests")


# ---------------------------------------------------------------------------
# 共享 Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def default_config():
    """返回默认的 DamBreakConfig 实例."""
    try:
        from src.core.config import DamBreakConfig
        return DamBreakConfig()
    except ImportError:
        pytest.skip("DamBreakConfig 尚未实现")


@pytest.fixture
def dry_bed_config():
    """干底工况配置 (h_R=0)."""
    try:
        from src.core.config import DamBreakConfig
        return DamBreakConfig(h_L=1.0, h_R=0.0, u_L=0.0, u_R=0.0)
    except ImportError:
        pytest.skip("DamBreakConfig 尚未实现")


@pytest.fixture
def wet_bed_config():
    """湿底工况配置 (h_R>0)."""
    try:
        from src.core.config import DamBreakConfig
        return DamBreakConfig(h_L=2.0, h_R=1.0, u_L=0.0, u_R=0.0)
    except ImportError:
        pytest.skip("DamBreakConfig 尚未实现")


@pytest.fixture
def small_grid_config():
    """小网格配置，用于快速测试."""
    try:
        from src.core.config import DamBreakConfig
        return DamBreakConfig(nx=50, t_end=0.1)
    except ImportError:
        pytest.skip("DamBreakConfig 尚未实现")


@pytest.fixture
def medium_grid_config():
    """中等网格配置."""
    try:
        from src.core.config import DamBreakConfig
        return DamBreakConfig(nx=200, t_end=0.5)
    except ImportError:
        pytest.skip("DamBreakConfig 尚未实现")


@pytest.fixture
def dam_break_initial_state(default_config):
    """生成标准溃坝问题的初始守恒变量 U0.

    U[0, :] = h (水深)
    U[1, :] = hu (动量)
    """
    if default_config is None:
        pytest.skip("依赖的 default_config fixture 不可用")
    cfg = default_config
    nx = cfg.nx
    U0 = np.zeros((2, nx), dtype=np.float64)
    x_grid = cfg.x_grid
    mid = (cfg.x_min + cfg.x_max) / 2
    left_mask = x_grid <= mid
    U0[0, left_mask] = cfg.h_L
    U0[0, ~left_mask] = cfg.h_R
    U0[1, left_mask] = cfg.h_L * cfg.u_L
    U0[1, ~left_mask] = cfg.h_R * cfg.u_R
    return U0


@pytest.fixture
def all_schemes():
    """返回所有可用的数值格式类列表."""
    try:
        from src.core.schemes import (
            GodunovScheme,
            HLLOneScheme,
            LaxFriedrichsScheme,
            LaxWendroffScheme,
            MacCormackScheme,
            MUSCLHancockScheme,
        )
        return [
            LaxFriedrichsScheme,
            LaxWendroffScheme,
            MacCormackScheme,
            GodunovScheme,
            HLLOneScheme,
            MUSCLHancockScheme,
        ]
    except ImportError:
        pytest.skip("数值格式尚未实现")


@pytest.fixture
def tvd_schemes():
    """返回所有 TVD 格式类列表."""
    try:
        from src.core.schemes import (
            GodunovScheme,
            HLLOneScheme,
            LaxFriedrichsScheme,
            MUSCLHancockScheme,
        )
        return [
            LaxFriedrichsScheme,
            GodunovScheme,
            HLLOneScheme,
            MUSCLHancockScheme,
        ]
    except ImportError:
        pytest.skip("TVD 数值格式尚未实现")


@pytest.fixture
def progress_callback():
    """返回一个用于测试的进度回调函数."""
    calls = []

    def callback(current_time: float, end_time: float) -> None:
        calls.append((current_time, end_time))

    callback.calls = calls
    return callback
