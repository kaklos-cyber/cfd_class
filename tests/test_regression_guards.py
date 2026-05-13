"""Regression Guard Tests.

These tests prevent previously discovered bugs from reoccurring.
They serve as safety nets against regression.
"""

from pathlib import Path

import numpy as np
import pytest

from src.core.config import DamBreakConfig
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.hll import HLLScheme
from src.core.schemes.muscl import MUSCLScheme


def get_scheme(name: str):
    """Return scheme instance by name (frontend-compatible API)."""
    scheme_map = {
        "Lax-Friedrichs": LaxFriedrichsScheme,
        "Lax-Wendroff": LaxWendroffScheme,
        "MacCormack": MacCormackScheme,
        "Beam-Warming": BeamWarmingScheme,
        "Fromm": FrommScheme,
        "Godunov": GodunovScheme,
        "HLL": HLLScheme,
        "MUSCL-Hancock": MUSCLScheme,
        "Upwind": UpwindScheme,
    }
    if name not in scheme_map:
        raise ValueError(f"Unknown scheme: {name}")
    return scheme_map[name]()


class TestNoSelfImportRegression:
    """Prevent self-import circular dependency regression."""

    def test_pages_init_no_circular_import(self):
        """FIXED: pages/__init__.py no longer has circular import."""
        pages_init = Path("src/frontend/pages/__init__.py")
        if not pages_init.exists():
            pytest.skip("pages/__init__.py not found")

        content = pages_init.read_text()

        assert "from .pages import" not in content, (
            "REGRESSION: pages/__init__.py contains circular import"
        )


class TestPlotDataShapeConsistency:
    """Prevent plotting data shape mismatch regression."""

    def test_simulation_result_x_y_same_length(self):
        """REGRESSION: Plotting code assumed x and y same length."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        x = config.x
        final_h = result.h[-1]

        assert len(x) == len(final_h), (
            f"REGRESSION: x length ({len(x)}) != h length ({len(final_h)})"
        )

    def test_simulation_result_h_is_1d_array(self):
        """REGRESSION: h[-1] was scalar instead of array."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        final_h = result.h[-1]

        assert isinstance(final_h, np.ndarray), (
            "REGRESSION: h[-1] is not ndarray"
        )
        assert final_h.ndim == 1, (
            f"REGRESSION: h[-1] has {final_h.ndim} dimensions, expected 1"
        )

    def test_all_schemes_produce_same_length_output(self):
        """REGRESSION: Different schemes produced different length outputs."""
        config = DamBreakConfig(nx=50, t_end=0.1)
        h0, u0 = config.initial_condition()
        x = config.x

        for name in [
            "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
            "Beam-Warming", "Fromm", "Godunov", "HLL",
            "MUSCL-Hancock", "Upwind",
        ]:
            scheme = get_scheme(name)
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )

            final_h = result.h[-1]
            assert len(final_h) == len(x), (
                f"REGRESSION: {name} output length ({len(final_h)}) "
                f"!= x length ({len(x)})"
            )


class TestConfigParameterValidation:
    """Prevent config parameter regression."""

    def test_config_rejects_schemes_key(self):
        """REGRESSION: DamBreakConfig accepted invalid 'schemes' key."""
        with pytest.raises((TypeError, ValueError)):
            DamBreakConfig(schemes=["LF"])

    def test_config_rejects_l_key(self):
        """REGRESSION: DamBreakConfig accepted 'L' instead of 'domain_length'."""
        with pytest.raises(TypeError):
            DamBreakConfig(L=10.0)

    def test_config_requires_domain_length(self):
        """REGRESSION: domain_length was optional or had wrong default."""
        config = DamBreakConfig()
        assert config.domain_length > 0
        assert config.domain_length == 1000.0


class TestExactSolverRegression:
    """Prevent exact solver regression."""

    def test_exact_solver_module_path(self):
        """REGRESSION: Frontend imported from exact_riemann instead of exact."""
        from src.core.solvers.exact import ExactRiemannSolver

        solver = ExactRiemannSolver()
        assert solver is not None

    def test_exact_solver_sample_solution_shape(self):
        """REGRESSION: sample_solution returned wrong shape."""
        from src.core.solvers.exact import ExactRiemannSolver

        config = DamBreakConfig(nx=50, t_end=0.1)
        solver = ExactRiemannSolver(g=config.g)
        x = config.x

        h_exact, u_exact = solver.sample_solution(
            config.h_l, config.u_l, config.h_r, config.u_r,
            x, config.t_end, config.x_dam
        )

        assert len(h_exact) == config.nx
        assert len(u_exact) == config.nx


class TestSchemeMethodRegression:
    """Prevent scheme method regression."""

    def test_scheme_has_both_methods(self):
        """FIXED: Scheme now has both run_simulation() and evolve()."""
        scheme = get_scheme("Lax-Friedrichs")

        assert hasattr(scheme, "run_simulation")
        assert hasattr(scheme, "evolve")

    def test_scheme_run_simulation_signature(self):
        """Verify run_simulation signature."""
        import inspect

        scheme = get_scheme("Lax-Friedrichs")
        sig = inspect.signature(scheme.run_simulation)
        params = list(sig.parameters.keys())

        assert "h0" in params
        assert "u0" in params
        assert "cfl" in params
        assert "dx" in params
        assert "t_end" in params
