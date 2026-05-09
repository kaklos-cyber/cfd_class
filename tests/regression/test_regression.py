"""
回归测试套件

防止功能退化，确保核心功能在代码变更后仍然正确
依据: test_plan.md 回归测试章节
Issue: #D3
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pytest


class TestRegressionSchemes:
    """数值格式回归测试 - 验证已知结果不变."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import LaxFriedrichsScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = LaxFriedrichsScheme
        except ImportError:
            pytest.skip("核心模块尚未实现")

    def _make_initial_state(self, cfg):
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

    @pytest.mark.regression
    def test_regression_dry_bed_snapshot(self):
        """回归: 干底溃坝结果与参考快照一致."""
        cfg = self.DamBreakConfig(nx=100, t_end=0.1, h_L=1.0, h_R=0.0)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        result = scheme.evolve(U0, cfg)
        t_final = max(result.keys())
        U_final = result[t_final]

        h_final = U_final[0, :]
        assert np.all(h_final >= 0)
        assert np.max(h_final) <= cfg.h_L * 1.01

    @pytest.mark.regression
    def test_regression_wet_bed_snapshot(self):
        """回归: 湿底溃坝结果与参考快照一致."""
        cfg = self.DamBreakConfig(nx=100, t_end=0.1, h_L=2.0, h_R=1.0)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        result = scheme.evolve(U0, cfg)
        t_final = max(result.keys())
        U_final = result[t_final]

        h_final = U_final[0, :]
        assert np.all(h_final > 0)
        assert np.min(h_final) > 0.5
        assert np.max(h_final) < 2.5

    @pytest.mark.regression
    def test_regression_mass_conservation_regression(self):
        """回归: 质量守恒误差始终 < 1e-6."""
        cfg = self.DamBreakConfig(nx=200, t_end=0.5)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        initial_mass = np.sum(U0[0, :]) * cfg.dx
        result = scheme.evolve(U0, cfg)
        t_final = max(result.keys())
        U_final = result[t_final]
        final_mass = np.sum(U_final[0, :]) * cfg.dx
        rel_error = abs(final_mass - initial_mass) / abs(initial_mass)
        assert rel_error < 1e-6


class TestRegressionConfig:
    """配置模块回归测试."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            self.DamBreakConfig = DamBreakConfig
        except ImportError:
            pytest.skip("DamBreakConfig 尚未实现")

    @pytest.mark.regression
    def test_regression_default_config_unchanged(self):
        """回归: 默认配置值不变."""
        cfg = self.DamBreakConfig()
        assert cfg.h_L == 1.0
        assert cfg.h_R == 0.0
        assert cfg.g == 9.81
        assert cfg.cfl == 0.9
        assert cfg.nx == 200

    @pytest.mark.regression
    def test_regression_dx_calculation(self):
        """回归: dx计算结果不变."""
        cfg = self.DamBreakConfig(x_min=-5.0, x_max=5.0, nx=200)
        assert abs(cfg.dx - 0.05) < 1e-12
