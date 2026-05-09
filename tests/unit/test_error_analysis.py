"""
误差分析模块单元测试

测试目标: src/core/analysis/error_analysis.py
依据: test_plan.md TC-EA-01 ~ TC-EA-08
Issue: #D2
"""

import numpy as np
import pytest


class TestComputeError:
    """误差计算函数测试."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.analysis.error_analysis import compute_error
            self.compute_error = compute_error
        except ImportError:
            pytest.skip("compute_error 尚未实现")

    def test_tc_ea_01_l1_norm(self):
        """TC-EA-01: L1范数计算."""
        nx = 100
        x = np.linspace(0, 1, nx)
        exact = np.sin(2 * np.pi * x)
        numerical = exact + 0.01
        error = self.compute_error(numerical, exact, p=1)
        assert error > 0
        expected = np.sum(np.abs(numerical - exact)) / nx
        assert abs(error - expected) < 1e-10

    def test_tc_ea_02_l2_norm(self):
        """TC-EA-02: L2范数计算."""
        nx = 100
        x = np.linspace(0, 1, nx)
        exact = np.sin(2 * np.pi * x)
        numerical = exact + 0.01
        error = self.compute_error(numerical, exact, p=2)
        assert error > 0

    def test_tc_ea_03_linf_norm(self):
        """TC-EA-03: L∞范数计算."""
        nx = 100
        exact = np.zeros(nx)
        numerical = np.zeros(nx)
        numerical[50] = 1.0
        error = self.compute_error(numerical, exact, p=float("inf"))
        assert error == 1.0

    def test_tc_ea_04_zero_error(self):
        """TC-EA-04: 完全相同时误差=0."""
        nx = 100
        arr = np.random.rand(nx)
        error = self.compute_error(arr, arr, p=1)
        assert error == 0.0
        error = self.compute_error(arr, arr, p=2)
        assert error == 0.0
        error = self.compute_error(arr, arr, p=float("inf"))
        assert error == 0.0

    def test_tc_ea_05_different_shapes_raises(self):
        """不同形状数组应报错."""
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([1.0, 2.0])
        with pytest.raises((ValueError, AssertionError)):
            self.compute_error(a, b, p=1)


class TestEstimateOrder:
    """收敛阶估计函数测试."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.analysis.error_analysis import estimate_order
            self.estimate_order = estimate_order
        except ImportError:
            pytest.skip("estimate_order 尚未实现")

    def test_tc_ea_06_first_order(self):
        """TC-EA-07: 一阶收敛验证."""
        nx_list = [50, 100, 200, 400]
        errors = [0.04, 0.02, 0.01, 0.005]
        order = self.estimate_order(nx_list, errors)
        assert abs(order - 1.0) < 0.2

    def test_tc_ea_07_second_order(self):
        """TC-EA-08: 二阶收敛验证."""
        nx_list = [50, 100, 200, 400]
        errors = [0.0016, 0.0004, 0.0001, 0.000025]
        order = self.estimate_order(nx_list, errors)
        assert abs(order - 2.0) < 0.2

    def test_tc_ea_08_grid_sequence(self):
        """TC-EA-06: 网格序列验证."""
        nx_list = [50, 100, 200, 400, 800]
        errors = [1.0 / nx for nx in nx_list]
        order = self.estimate_order(nx_list, errors)
        assert order > 0

    def test_tc_ea_09_monotonic_decreasing(self):
        """误差应单调递减."""
        nx_list = [50, 100, 200]
        errors = [0.1, 0.05, 0.025]
        order = self.estimate_order(nx_list, errors)
        assert 0.5 < order < 2.0

    def test_tc_ea_10_insufficient_points(self):
        """点数不足时应处理."""
        nx_list = [100]
        errors = [0.01]
        with pytest.raises((ValueError, TypeError)):
            self.estimate_order(nx_list, errors)
