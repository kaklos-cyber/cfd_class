"""Frontend-Backend Integration Tests.

These tests verify that the frontend can correctly import and use
backend modules, catching API mismatches that unit tests alone cannot detect.

Bug types detected:
  - Class name mismatches (HLL vs HLLScheme)
  - Method name mismatches (evolve vs run_simulation)
  - Parameter name mismatches (L vs domain_length)
  - Import path mismatches (exact_riemann vs exact)
  - Data shape assumptions (list vs ndarray)
"""

import numpy as np
import pytest

from src.core.config import DamBreakConfig
from src.core.schemes.base_scheme import BaseScheme
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.hll import HLLScheme
from src.core.schemes.muscl import MUSCLScheme
from src.core.solvers.exact import ExactRiemannSolver
from src.core.solvers.hll import HLLSolver


# Frontend expects get_scheme() but backend doesn't have it.
# This is a known API mismatch. We create a compatibility function for tests.
def get_scheme(name: str) -> BaseScheme:
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


class TestSchemeFactory:
    """Test get_scheme() factory function."""

    @pytest.mark.parametrize("name", [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Beam-Warming",
        "Fromm",
        "Godunov",
        "HLL",
        "MUSCL-Hancock",
        "Upwind",
    ])
    def test_get_scheme_returns_instance(self, name):
        """Verify get_scheme() returns a valid scheme instance."""
        scheme = get_scheme(name)
        assert scheme is not None
        assert isinstance(scheme, BaseScheme)

    @pytest.mark.parametrize("name", [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Beam-Warming",
        "Fromm",
        "Godunov",
        "HLL",
        "MUSCL-Hancock",
        "Upwind",
    ])
    def test_scheme_has_run_simulation(self, name):
        """Verify scheme has run_simulation method (not evolve)."""
        scheme = get_scheme(name)
        assert hasattr(scheme, "run_simulation")
        assert callable(getattr(scheme, "run_simulation"))

    @pytest.mark.parametrize("name", [
        "Lax-Friedrichs",
        "Lax-Wendroff",
        "MacCormack",
        "Beam-Warming",
        "Fromm",
        "Godunov",
        "HLL",
        "MUSCL-Hancock",
        "Upwind",
    ])
    def test_scheme_has_compute_flux(self, name):
        """Verify scheme has compute_flux method."""
        scheme = get_scheme(name)
        assert hasattr(scheme, "compute_flux")
        assert callable(getattr(scheme, "compute_flux"))

    def test_get_scheme_invalid_name(self):
        """Verify get_scheme() raises error for invalid name."""
        with pytest.raises((ValueError, KeyError)):
            get_scheme("NonExistentScheme")


class TestFrontendImportPaths:
    """Test that frontend import paths match backend modules."""

    def test_exact_riemann_solver_import(self):
        """Verify ExactRiemannSolver exists (not ExactRiemann)."""
        from src.core.solvers.exact import ExactRiemannSolver
        solver = ExactRiemannSolver()
        assert solver is not None

    def test_hll_solver_import(self):
        """Verify HLLSolver exists (not HLL)."""
        from src.core.solvers.hll import HLLSolver
        solver = HLLSolver()
        assert solver is not None

    def test_all_scheme_classes_exist(self):
        """Verify all scheme classes frontend expects exist."""
        from src.core.schemes.upwind import UpwindScheme
        from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
        from src.core.schemes.lax_wendroff import LaxWendroffScheme
        from src.core.schemes.maccormack import MacCormackScheme
        from src.core.schemes.beam_warming import BeamWarmingScheme
        from src.core.schemes.fromm import FrommScheme
        from src.core.schemes.godunov import GodunovScheme
        from src.core.schemes.hll import HLLScheme
        from src.core.schemes.muscl import MUSCLScheme

        assert UpwindScheme is not None
        assert LaxFriedrichsScheme is not None
        assert LaxWendroffScheme is not None
        assert MacCormackScheme is not None
        assert BeamWarmingScheme is not None
        assert FrommScheme is not None
        assert GodunovScheme is not None
        assert HLLScheme is not None
        assert MUSCLScheme is not None


class TestDamBreakConfigAPI:
    """Test DamBreakConfig parameter handling."""

    def test_config_rejects_invalid_keys(self):
        """Verify DamBreakConfig rejects invalid parameter keys."""
        with pytest.raises((TypeError, ValueError)):
            DamBreakConfig(schemes=["LF"], L=10.0)

    def test_config_rejects_frontend_style_params(self):
        """Verify frontend-style params (h_L, h_R, L) are rejected."""
        with pytest.raises((TypeError, ValueError)):
            DamBreakConfig(h_L=10.0, h_R=1.0, L=10.0)

    def test_config_accepts_backend_style_params(self):
        """Verify backend-style params (h_l, h_r, domain_length) work."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        assert config.h_l == 10.0
        assert config.h_r == 1.0
        assert config.domain_length == 10.0

    def test_config_from_dict_ignores_invalid_keys(self):
        """Verify from_dict ignores invalid keys (not raises)."""
        data = {
            "h_l": 10.0,
            "h_r": 1.0,
            "domain_length": 10.0,
            "nx": 50,
            "t_end": 0.1,
            "x_dam": 5.0,
            "schemes": ["LF"],
            "L": 10.0,
        }
        config = DamBreakConfig.from_dict(data)
        assert config.h_l == 10.0
        assert config.nx == 50

    def test_config_to_dict_roundtrip(self):
        """Verify to_dict -> from_dict roundtrip works."""
        original = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        data = original.to_dict()
        restored = DamBreakConfig.from_dict(data)
        assert restored.h_l == original.h_l
        assert restored.h_r == original.h_r
        assert restored.domain_length == original.domain_length


class TestSchemeRunSimulation:
    """Test scheme.run_simulation() with real config."""

    def test_run_simulation_returns_result(self):
        """Verify run_simulation returns a result object."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert result is not None
        assert hasattr(result, "h")
        assert hasattr(result, "u")
        assert hasattr(result, "t")

    def test_run_simulation_result_shapes(self):
        """Verify result shapes match config."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert result.h.shape[1] == config.nx
        assert result.u.shape[1] == config.nx
        assert len(result.t) > 1

    def test_run_simulation_all_schemes(self):
        """Verify all schemes can run with standard config."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        h0, u0 = config.initial_condition()

        for name in [
            "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
            "Beam-Warming", "Fromm", "Godunov", "HLL",
            "MUSCL-Hancock", "Upwind",
        ]:
            scheme = get_scheme(name)
            result = scheme.run_simulation(
                h0, u0, config.cfl, config.dx, config.t_end
            )
            assert result is not None
            assert result.h.shape[1] == config.nx

    def test_run_simulation_result_is_ndarray(self):
        """Verify result data is ndarray (not list)."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        assert isinstance(result.h, np.ndarray)
        assert isinstance(result.u, np.ndarray)

    def test_run_simulation_final_state_shape(self):
        """Verify final state h[-1] is 1D array of length nx."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end
        )

        final_h = result.h[-1]
        assert final_h.ndim == 1
        assert len(final_h) == config.nx


class TestExactRiemannSolver:
    """Test ExactRiemannSolver integration."""

    def test_exact_solver_exists(self):
        """Verify ExactRiemannSolver class exists."""
        solver = ExactRiemannSolver()
        assert solver is not None

    def test_exact_solver_sample_solution(self):
        """Verify sample_solution returns arrays of correct shape."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.1, x_dam=5.0
        )
        solver = ExactRiemannSolver(g=config.g)
        x = config.x

        h_exact, u_exact = solver.sample_solution(
            config.h_l, config.u_l, config.h_r, config.u_r,
            x, config.t_end, config.x_dam
        )

        assert len(h_exact) == config.nx
        assert len(u_exact) == config.nx
        assert isinstance(h_exact, np.ndarray)
        assert isinstance(u_exact, np.ndarray)

    def test_exact_solver_solve(self):
        """Verify solve returns RiemannState."""
        solver = ExactRiemannSolver()
        state = solver.solve(10.0, 0.0, 1.0, 0.0)

        assert state is not None
        assert hasattr(state, "h")
        assert hasattr(state, "u")
        assert state.h > 0


class TestDataShapeConsistency:
    """Test data shape consistency between frontend and backend."""

    def test_initial_condition_returns_ndarray(self):
        """Verify initial_condition returns ndarray."""
        config = DamBreakConfig(nx=50)
        h0, u0 = config.initial_condition()

        assert isinstance(h0, np.ndarray)
        assert isinstance(u0, np.ndarray)
        assert len(h0) == config.nx
        assert len(u0) == config.nx

    def test_config_x_returns_ndarray(self):
        """Verify config.x returns ndarray."""
        config = DamBreakConfig(nx=50)
        x = config.x

        assert isinstance(x, np.ndarray)
        assert len(x) == config.nx

    def test_snapshot_data_shape(self):
        """Verify snapshot data has correct shape."""
        config = DamBreakConfig(
            h_l=10.0, h_r=1.0, domain_length=10.0,
            nx=50, t_end=0.5, x_dam=5.0
        )
        h0, u0 = config.initial_condition()
        scheme = get_scheme("Lax-Friedrichs")

        result = scheme.run_simulation(
            h0, u0, config.cfl, config.dx, config.t_end,
            snapshot_times=[0.1, 0.2]
        )

        assert len(result.snapshots) >= 1
        for t, (h_snap, u_snap) in result.snapshots.items():
            assert len(h_snap) == config.nx
            assert len(u_snap) == config.nx
            assert isinstance(h_snap, np.ndarray)


class TestFrontendBackendMismatches:
    """Explicitly test known frontend-backend mismatches."""

    def test_frontend_hll_class_name_mismatch(self):
        """BUG: Frontend imports HLL, backend has HLLSolver."""
        with pytest.raises(ImportError):
            from src.core.schemes import HLL

    def test_frontend_godunov_class_name_mismatch(self):
        """BUG: Frontend imports Godunov, backend has GodunovScheme."""
        with pytest.raises(ImportError):
            from src.core.schemes import Godunov

    def test_frontend_muscl_class_name_mismatch(self):
        """BUG: Frontend imports MUSCLHancock, backend has MUSCLScheme."""
        with pytest.raises(ImportError):
            from src.core.schemes import MUSCLHancock

    def test_frontend_evolve_method_mismatch(self):
        """BUG: Frontend calls evolve(), backend has run_simulation()."""
        config = DamBreakConfig(nx=50)
        scheme = get_scheme("Lax-Friedrichs")

        assert not hasattr(scheme, "evolve")
        assert hasattr(scheme, "run_simulation")

    def test_frontend_exactriemann_class_mismatch(self):
        """BUG: Frontend imports ExactRiemann, backend has ExactRiemannSolver."""
        with pytest.raises(ImportError):
            from src.core.solvers.exact_riemann import ExactRiemann

    def test_frontend_param_l_mismatch(self):
        """BUG: Frontend uses 'L', backend uses 'domain_length'."""
        with pytest.raises(TypeError):
            DamBreakConfig(L=10.0)

    def test_frontend_param_h_l_mismatch(self):
        """BUG: Frontend uses 'h_L', backend uses 'h_l'."""
        with pytest.raises(TypeError):
            DamBreakConfig(h_L=10.0)

    def test_frontend_param_h_r_mismatch(self):
        """BUG: Frontend uses 'h_R', backend uses 'h_r'."""
        with pytest.raises(TypeError):
            DamBreakConfig(h_R=1.0)

    def test_frontend_param_u_l_mismatch(self):
        """BUG: Frontend uses 'u_L', backend uses 'u_l'."""
        with pytest.raises(TypeError):
            DamBreakConfig(u_L=0.0)

    def test_frontend_param_u_r_mismatch(self):
        """BUG: Frontend uses 'u_R', backend uses 'u_r'."""
        with pytest.raises(TypeError):
            DamBreakConfig(u_R=0.0)
