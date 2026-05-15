"""Unit tests for HLL approximate Riemann solver."""

import numpy as np
import pytest

from src.core.solvers.hll import HLLSolver


class TestHLLSolver:
    """Test suite for HLLSolver."""

    def test_init(self):
        """Test solver initialization."""
        solver = HLLSolver()
        assert solver.g == 9.81

    def test_init_custom_g(self):
        """Test solver with custom gravity."""
        solver = HLLSolver(g=9.8)
        assert solver.g == 9.8

    def test_compute_flux_symmetric(self):
        """Test flux for symmetric case."""
        solver = HLLSolver()
        flux = solver.compute_flux(1.0, 0.0, 1.0, 0.0)
        assert len(flux) == 2
        assert flux[0] == pytest.approx(0.0, abs=1e-10)

    def test_compute_flux_dam_break(self):
        """Test flux for dam break case."""
        solver = HLLSolver()
        flux = solver.compute_flux(1.0, 0.0, 0.1, 0.0)
        assert len(flux) == 2
        assert flux[0] > 0

    def test_compute_flux_dry_bed(self):
        """Test flux with dry bed."""
        solver = HLLSolver()
        flux = solver.compute_flux(0.0, 0.0, 1.0, 0.0)
        assert len(flux) == 2

    def test_compute_flux_with_velocity(self):
        """Test flux with non-zero velocity."""
        solver = HLLSolver()
        flux = solver.compute_flux(1.0, 2.0, 0.5, -1.0)
        assert len(flux) == 2

    def test_wave_speeds_direction(self):
        """Test wave speeds have correct signs for dam break."""
        solver = HLLSolver()
        s_l, s_r = solver._compute_wave_speeds(1.0, 0.0, 0.1, 0.0)
        assert s_l < s_r

    def test_wave_speeds_symmetric(self):
        """Test wave speeds for symmetric case."""
        solver = HLLSolver()
        s_l, s_r = solver._compute_wave_speeds(1.0, 0.0, 1.0, 0.0)
        assert s_l < 0
        assert s_r > 0

    def test_compute_flux_vectorized(self):
        """Test vectorized flux computation."""
        solver = HLLSolver()
        h = np.ones(10)
        h[:5] = 2.0
        u = np.zeros(10)

        mass_flux, mom_flux = solver.compute_flux_vectorized(h, u)
        assert len(mass_flux) == 11
        assert len(mom_flux) == 11

    def test_flux_consistency(self):
        """Test that flux is consistent with physical flux."""
        solver = HLLSolver()
        h = 1.0
        u = 2.0

        flux = solver.compute_flux(h, u, h, u)
        expected_mass = h * u
        expected_mom = h * u**2 + 0.5 * solver.g * h**2

        assert flux[0] == pytest.approx(expected_mass, abs=1e-10)
        assert flux[1] == pytest.approx(expected_mom, abs=1e-10)

    def test_zero_depth_both_sides(self):
        """Test with zero depth on both sides."""
        solver = HLLSolver()
        flux = solver.compute_flux(0.0, 0.0, 0.0, 0.0)
        assert len(flux) == 2
        assert np.all(np.isfinite(flux))

    def test_supercritical_flow(self):
        """Test with supercritical flow."""
        solver = HLLSolver()
        flux = solver.compute_flux(1.0, 5.0, 0.8, 4.5)
        assert len(flux) == 2
        assert np.all(np.isfinite(flux))
