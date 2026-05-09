import pytest
import numpy as np

from src.core.solvers.riemann_solver import (
    exact_riemann_solution,
    hll_flux,
    evaluate_riemann_solution,
)


class TestRiemannSolver:
    def test_dry_ritter_solution(self):
        U_L = np.array([1.0, 0.0])
        U_R = np.array([0.0, 0.0])
        g = 9.81

        sol = exact_riemann_solution(U_L, U_R, g)

        assert sol["type"] == "dry_ritter"
        c_L = np.sqrt(g * 1.0)
        expected_S_L = -c_L
        expected_S_star = 2 * c_L / 3
        assert sol["S_L"] == pytest.approx(expected_S_L)
        assert sol["S_star"] == pytest.approx(expected_S_star)

    def test_wet_case_symmetry(self):
        U_L = np.array([2.0, 0.0])
        U_R = np.array([1.0, 0.0])
        g = 9.81

        sol = exact_riemann_solution(U_L, U_R, g)

        assert sol["type"] == "wet_general"
        assert sol["h_star"] > 0
        assert sol["u_star"] > 0

    def test_hll_flux_wet(self):
        U_L = np.array([1.0, 0.0])
        U_R = np.array([0.5, 0.0])
        g = 9.81

        F = hll_flux(U_L, U_R, g)

        assert F.shape == (2,)
        assert np.isfinite(F[0])
        assert np.isfinite(F[1])

    def test_hll_flux_dry(self):
        U_L = np.array([1.0, 0.0])
        U_R = np.array([1e-12, 0.0])
        g = 9.81

        F = hll_flux(U_L, U_R, g)

        assert np.isfinite(F[0])
        assert np.isfinite(F[1])

    def test_evaluate_riemann_solution(self):
        U_L = np.array([1.0, 0.0])
        U_R = np.array([0.0, 0.0])
        g = 9.81

        sol = exact_riemann_solution(U_L, U_R, g)
        x = np.array([-5.0, 0.0, 5.0])
        t = 0.5

        U = evaluate_riemann_solution(sol, x, t, U_L, U_R, g)

        assert U.shape == (2, 3)
        assert U[0, 0] == pytest.approx(1.0)
        assert U[0, -1] < 1e-10
