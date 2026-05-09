"""
性能测试套件

测试目标: 响应时间和资源占用
依据: test_plan.md TC-PERF-01 ~ TC-PERF-10
Issue: #D3
"""

import time

import numpy as np
import pytest


class TestPerformance:
    """性能测试."""

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

    @pytest.mark.performance
    def test_tc_perf_01_small_scale(self):
        """TC-PERF-01: 小规模模拟 nx=100 < 1秒."""
        cfg = self.DamBreakConfig(nx=100, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        start = time.time()
        scheme.evolve(U0, cfg)
        elapsed = time.time() - start
        assert elapsed < 1.0, f"小规模模拟耗时 {elapsed:.2f}s > 1s"

    @pytest.mark.performance
    @pytest.mark.slow
    def test_tc_perf_02_medium_scale(self):
        """TC-PERF-02: 中等规模 nx=500 < 5秒."""
        cfg = self.DamBreakConfig(nx=500, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        start = time.time()
        scheme.evolve(U0, cfg)
        elapsed = time.time() - start
        assert elapsed < 5.0, f"中等规模模拟耗时 {elapsed:.2f}s > 5s"

    @pytest.mark.performance
    @pytest.mark.slow
    def test_tc_perf_03_large_scale(self):
        """TC-PERF-03: 大规模 nx=2000 < 30秒."""
        cfg = self.DamBreakConfig(nx=2000, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        start = time.time()
        scheme.evolve(U0, cfg)
        elapsed = time.time() - start
        assert elapsed < 30.0, f"大规模模拟耗时 {elapsed:.2f}s > 30s"

    @pytest.mark.performance
    def test_tc_perf_07_memory_peak(self):
        """TC-PERF-07: 内存占用 nx=2000 < 512MB."""
        import tracemalloc
        cfg = self.DamBreakConfig(nx=2000, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        scheme = self.Scheme()
        tracemalloc.start()
        scheme.evolve(U0, cfg)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / (1024 * 1024)
        assert peak_mb < 512, f"内存峰值 {peak_mb:.1f}MB > 512MB"
