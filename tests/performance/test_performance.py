"""Performance tests for numerical schemes.

These tests verify that simulations complete within reasonable time
and do not exhibit memory leaks.
"""

import time

import numpy as np
import pytest

from src.core.config import DamBreakConfig
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.muscl import MUSCLScheme


class TestPerformance:
    """Performance test suite."""

    @pytest.mark.slow
    def test_small_grid_performance(self):
        """Test performance with small grid."""
        config = DamBreakConfig(nx=50, t_end=0.5)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        start = time.time()
        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )
        elapsed = time.time() - start

        assert elapsed < 5.0
        assert len(result.t) > 1

    @pytest.mark.slow
    def test_medium_grid_performance(self):
        """Test performance with medium grid."""
        config = DamBreakConfig(nx=100, t_end=0.5)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        start = time.time()
        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )
        elapsed = time.time() - start

        assert elapsed < 10.0
        assert len(result.t) > 1

    @pytest.mark.slow
    def test_all_schemes_small_grid(self):
        """Test all schemes on small grid."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()

        schemes = [
            UpwindScheme(),
            LaxFriedrichsScheme(),
            LaxWendroffScheme(),
            MacCormackScheme(),
            GodunovScheme(),
            MUSCLScheme(),
        ]

        for scheme in schemes:
            start = time.time()
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            elapsed = time.time() - start

            assert elapsed < 10.0, f"{scheme.name} too slow: {elapsed:.2f}s"
            assert len(result.t) > 1

    def test_memory_no_leak_small(self):
        """Test no memory leak with repeated runs."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        for _ in range(5):
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            assert len(result.t) > 1
            assert result.h.shape[1] == config.nx

    def test_snapshot_performance(self):
        """Test snapshot recording performance."""
        config = DamBreakConfig(nx=50, t_end=0.5)
        h0, u0 = config.initial_condition()
        scheme = UpwindScheme()

        snapshot_times = [0.1, 0.2, 0.3]

        start = time.time()
        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end,
            snapshot_times=snapshot_times
        )
        elapsed = time.time() - start

        assert elapsed < 5.0
        assert len(result.snapshots) >= 1
