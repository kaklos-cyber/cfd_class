"""
Riemann 求解器单元测试

测试目标: src/core/solvers/riemann_solver.py
依据: test_plan.md TC-RS-01 ~ TC-RS-08
Issue: #D2
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pytest


class TestExactRiemannSolver:
    """精确 Riemann 求解器测试."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.solvers.riemann_solver import exact_riemann_solution
            self.exact_riemann_solution = exact_riemann_solution
        except ImportError:
            pytest.skip("exact_riemann_solution 尚未实现")

    def test_tc_rs_01_dry_bed_ritter(self):
        """TC-RS-02: 干底Ritter解."""
        g = 9.81
        U_L = np.array([1.0, 0.0], dtype=np.float64)
        U_R = np.array([0.0, 0.0], dtype=np.float64)
        result = self.exact_riemann_solution(U_L, U_R, g)
        assert "h_star" in result
        assert "u_star" in result
        assert "S_L" in result
        assert "S_R" in result
        assert "type" in result
        assert result["type"] == "dry_ritter"

    def test_tc_rs_02_wet_bed(self):
        """TC-RS-01: 湿底精确解."""
        g = 9.81
        U_L = np.array([2.0, 0.0], dtype=np.float64)
        U_R = np.array([1.0, 0.0], dtype=np.float64)
        result = self.exact_riemann_solution(U_L, U_R, g)
        assert result["h_star"] > 0
        assert result["S_L"] < 0
        assert result["S_R"] > 0

    def test_tc_rs_03_wave_speeds_sign(self):
        """TC-RS-04: 波速符号正确."""
        g = 9.81
        U_L = np.array([1.0, 0.0], dtype=np.float64)
        U_R = np.array([0.5, 0.0], dtype=np.float64)
        result = self.exact_riemann_solution(U_L, U_R, g)
        assert result["S_L"] < result["S_R"]

    def test_tc_rs_04_uniform_flow(self):
        """TC-RS-06: 极限情况 h_L=h_R 时返回均匀流."""
        g = 9.81
        U_L = np.array([1.0, 0.0], dtype=np.float64)
        U_R = np.array([1.0, 0.0], dtype=np.float64)
        result = self.exact_riemann_solution(U_L, U_R, g)
        assert abs(result["h_star"] - 1.0) < 1e-6
        assert abs(result["u_star"]) < 1e-6

    def test_tc_rs_05_supercritical(self):
        """TC-RS-07: 超临界流处理."""
        g = 9.81
        U_L = np.array([1.0, 5.0], dtype=np.float64)
        U_R = np.array([0.5, 2.0], dtype=np.float64)
        result = self.exact_riemann_solution(U_L, U_R, g)
        assert "h_star" in result
        assert "u_star" in result

    def test_tc_rs_06_degenerate_cases(self):
        """TC-RS-08: 退化情况不崩溃."""
        g = 9.81
        cases = [
            np.array([0.01, 0.0], dtype=np.float64),
            np.array([10.0, 0.0], dtype=np.float64),
        ]
        for h_L in cases:
            U_L = h_L
            U_R = np.array([0.5, 0.0], dtype=np.float64)
            result = self.exact_riemann_solution(U_L, U_R, g)
            assert result is not None


class TestHLLFlux:
    """HLL 近似通量测试."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.solvers.riemann_solver import hll_flux
            self.hll_flux = hll_flux
        except ImportError:
            pytest.skip("hll_flux 尚未实现")

    def test_tc_rs_07_hll_flux_shape(self):
        """TC-RS-05: HLL通量返回合理值."""
        g = 9.81
        U_L = np.array([1.0, 0.0], dtype=np.float64)
        U_R = np.array([0.5, 0.0], dtype=np.float64)
        flux = self.hll_flux(U_L, U_R, g)
        assert isinstance(flux, np.ndarray)
        assert len(flux) == 2

    def test_tc_rs_08_hll_flux_consistency(self):
        """TC-RS-05: HLL通量一致性 U_L=U_R时返回F(U)."""
        g = 9.81
        U = np.array([1.0, 0.0], dtype=np.float64)
        flux = self.hll_flux(U, U, g)
        h, hu = U[0], U[1]
        expected_F = np.array([hu, hu**2 / h + 0.5 * g * h**2], dtype=np.float64)
        np.testing.assert_allclose(flux, expected_F, atol=1e-10)

    def test_tc_rs_09_hll_flux_physical(self):
        """TC-RS-05: HLL通量物理合理性."""
        g = 9.81
        U_L = np.array([2.0, 0.0], dtype=np.float64)
        U_R = np.array([1.0, 0.0], dtype=np.float64)
        flux = self.hll_flux(U_L, U_R, g)
        assert flux[0] >= 0
