"""
配置模块单元测试

测试目标: src/core/config.py - DamBreakConfig
依据: test_plan.md TC-CFG-01 ~ TC-CFG-10
Issue: #D2
"""

import numpy as np
import pytest


class TestDamBreakConfig:
    """DamBreakConfig 配置类测试套件."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            self.DamBreakConfig = DamBreakConfig
        except ImportError:
            pytest.skip("DamBreakConfig 尚未实现")

    def test_tc_cfg_01_default_values(self):
        """TC-CFG-01: 默认参数正确性."""
        cfg = self.DamBreakConfig()
        assert cfg.h_L == 1.0
        assert cfg.h_R == 0.0
        assert cfg.u_L == 0.0
        assert cfg.u_R == 0.0
        assert cfg.g == 9.81
        assert cfg.cfl == 0.9
        assert cfg.nx == 200
        assert cfg.t_end == 0.5
        assert cfg.x_min == -5.0
        assert cfg.x_max == 5.0

    def test_tc_cfg_02_custom_values(self):
        """TC-CFG-01: 自定义参数正确设置."""
        cfg = self.DamBreakConfig(
            h_L=2.5, h_R=1.0, u_L=1.0, u_R=-0.5,
            g=9.8, cfl=0.5, nx=100, t_end=1.0,
            x_min=-10.0, x_max=10.0
        )
        assert cfg.h_L == 2.5
        assert cfg.h_R == 1.0
        assert cfg.u_L == 1.0
        assert cfg.u_R == -0.5
        assert cfg.g == 9.8
        assert cfg.cfl == 0.5
        assert cfg.nx == 100
        assert cfg.t_end == 1.0
        assert cfg.x_min == -10.0
        assert cfg.x_max == 10.0

    def test_tc_cfg_03_dry_bed_valid(self):
        """TC-CFG-03: 干底工况合法性 (h_R=0 不报错)."""
        cfg = self.DamBreakConfig(h_R=0.0)
        assert cfg.h_R == 0.0

    def test_tc_cfg_04_negative_h_L_raises(self):
        """TC-CFG-04: 负水深检测 h_L<=0 时报错."""
        with pytest.raises(ValueError):
            self.DamBreakConfig(h_L=0.0)
        with pytest.raises(ValueError):
            self.DamBreakConfig(h_L=-1.0)

    def test_tc_cfg_05_negative_h_R_raises(self):
        """TC-CFG-04: 负水深检测 h_R<0 时报错."""
        with pytest.raises(ValueError):
            self.DamBreakConfig(h_R=-0.1)

    def test_tc_cfg_06_cfl_out_of_range(self):
        """TC-CFG-05: CFL范围检测 CFL>1或<=0时报错."""
        with pytest.raises(ValueError):
            self.DamBreakConfig(cfl=0.0)
        with pytest.raises(ValueError):
            self.DamBreakConfig(cfl=-0.1)
        with pytest.raises(ValueError):
            self.DamBreakConfig(cfl=1.1)

    def test_tc_cfg_07_nx_minimum(self):
        """TC-CFG-06: 网格数最小值 nx<10时报错."""
        with pytest.raises(ValueError):
            self.DamBreakConfig(nx=9)
        with pytest.raises(ValueError):
            self.DamBreakConfig(nx=0)

    def test_tc_cfg_08_dx_property(self):
        """TC-CFG-07: dx属性计算 dx=(x_max-x_min)/nx."""
        cfg = self.DamBreakConfig(x_min=-5.0, x_max=5.0, nx=200)
        expected_dx = (5.0 - (-5.0)) / 200
        assert abs(cfg.dx - expected_dx) < 1e-12

    def test_tc_cfg_09_x_grid_property(self):
        """TC-CFG-08: x_grid属性返回长度为nx的数组."""
        cfg = self.DamBreakConfig(nx=200)
        x_grid = cfg.x_grid
        assert isinstance(x_grid, np.ndarray)
        assert len(x_grid) == cfg.nx
        assert x_grid[0] == cfg.x_min + cfg.dx / 2
        assert x_grid[-1] == cfg.x_max - cfg.dx / 2

    def test_tc_cfg_10_frozen_immutability(self):
        """TC-CFG-09: frozen不可变性 尝试修改属性报错."""
        cfg = self.DamBreakConfig()
        with pytest.raises((AttributeError, TypeError)):
            cfg.h_L = 2.0

    def test_tc_cfg_11_extreme_values(self):
        """TC-CFG-10: 极端参数组合不崩溃."""
        cfg1 = self.DamBreakConfig(h_L=0.1, h_R=0.0, nx=10, cfl=0.1)
        assert cfg1.h_L == 0.1
        cfg2 = self.DamBreakConfig(h_L=10.0, h_R=10.0, nx=2000, cfl=0.95)
        assert cfg2.h_L == 10.0

    def test_tc_cfg_12_cfl_boundary(self):
        """TC-CFG-05: CFL边界值 CFL=1.0 和 CFL=0.01."""
        cfg_max = self.DamBreakConfig(cfl=1.0)
        assert cfg_max.cfl == 1.0
        cfg_min = self.DamBreakConfig(cfl=0.01)
        assert cfg_min.cfl == 0.01

    def test_tc_cfg_13_nx_boundary(self):
        """TC-CFG-06: nx边界值 nx=10 正常工作."""
        cfg = self.DamBreakConfig(nx=10)
        assert cfg.nx == 10
        assert len(cfg.x_grid) == 10

    def test_tc_cfg_14_x_grid_spacing(self):
        """TC-CFG-08: x_grid等间距验证."""
        cfg = self.DamBreakConfig(nx=100)
        diffs = np.diff(cfg.x_grid)
        assert np.allclose(diffs, cfg.dx, atol=1e-12)

    def test_tc_cfg_15_repr_str(self):
        """TC-CFG-01: 字符串表示可读."""
        cfg = self.DamBreakConfig()
        r = repr(cfg)
        assert "DamBreakConfig" in r or "h_L" in r



