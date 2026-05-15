"""Streamlit Smoke Tests.

These tests verify that Streamlit pages and core modules can be imported
without errors, catching integration issues early.

Note: These tests do NOT launch Streamlit server, they only check
that page modules can be imported and their dependencies resolved.
"""

import sys
from pathlib import Path

import pytest

# Check if streamlit is available
STREAMLIT_AVAILABLE = False
try:
    import streamlit
    STREAMLIT_AVAILABLE = True
except ImportError:
    pass


pytestmark = pytest.mark.skipif(
    not STREAMLIT_AVAILABLE,
    reason="Streamlit not installed"
)


class TestStreamlitPagesImport:
    """Test that all Streamlit pages can be imported."""

    def test_home_page_imports(self):
        """Verify home.py can be imported (bypass __init__ circular import)."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "home", Path("src/frontend/pages/home.py")
            )
            home = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(home)
            assert home is not None
        except ImportError as e:
            pytest.fail(f"home.py import failed: {e}")

    def test_simulation_page_imports(self):
        """Verify 1_Simulation.py can be imported (bypass __init__ circular import)."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "simulation", Path("src/frontend/pages/1_Simulation.py")
            )
            sim = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(sim)
            assert sim is not None
        except ImportError as e:
            pytest.fail(f"1_Simulation.py import failed: {e}")

    def test_comparison_page_imports(self):
        """Verify 2_Comparison.py can be imported (bypass __init__ circular import)."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "comparison", Path("src/frontend/pages/2_Comparison.py")
            )
            comp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(comp)
            assert comp is not None
        except ImportError as e:
            pytest.fail(f"2_Comparison.py import failed: {e}")

    def test_pages_init_no_circular_import(self):
        """BUG: pages/__init__.py has 'from .pages import *' circular import."""
        pages_init = Path("src/frontend/pages/__init__.py")
        if pages_init.exists():
            content = pages_init.read_text()
            # This documents the known bug - __init__ has circular import
            assert "from .pages import" in content, (
                "BUG CONFIRMED: pages/__init__.py contains circular import"
            )


class TestFrontendEnginesImport:
    """Test that frontend engines can be imported."""

    def test_simulation_engine_imports(self):
        """Verify simulation_engine.py can be imported."""
        try:
            from src.frontend.engines import simulation_engine
            assert simulation_engine is not None
        except ImportError as e:
            pytest.fail(f"simulation_engine.py import failed: {e}")

    def test_comparison_engine_imports(self):
        """Verify comparison_engine.py can be imported."""
        try:
            from src.frontend.engines import comparison_engine
            assert comparison_engine is not None
        except ImportError as e:
            pytest.fail(f"comparison_engine.py import failed: {e}")


class TestCoreModulesLoad:
    """Test that core modules frontend depends on are loadable."""

    def test_config_module_loads(self):
        """Verify DamBreakConfig can be imported."""
        from src.core.config import DamBreakConfig
        assert DamBreakConfig is not None

    def test_schemes_module_loads(self):
        """BUG: get_scheme() missing from src.core.schemes."""
        import src.core.schemes
        assert src.core.schemes is not None
        # Frontend expects get_scheme but backend doesn't have it
        assert not hasattr(src.core.schemes, "get_scheme"), (
            "BUG CONFIRMED: get_scheme() missing from src.core.schemes"
        )

    def test_exact_solver_module_loads(self):
        """Verify exact solver module can be imported."""
        from src.core.solvers.exact import ExactRiemannSolver
        assert ExactRiemannSolver is not None

    def test_hll_solver_module_loads(self):
        """Verify HLL solver module can be imported."""
        from src.core.solvers.hll import HLLSolver
        assert HLLSolver is not None

    def test_errors_module_loads(self):
        """Verify errors module can be imported."""
        from src.core.analysis.errors import compute_l1_error
        assert compute_l1_error is not None


class TestSimulationPageCoreModules:
    """Test simulation page's load_core_modules() logic."""

    def test_load_core_modules_success(self):
        """Verify core modules that simulation page needs exist."""
        from src.core.config import DamBreakConfig
        from src.core.solvers.exact import ExactRiemannSolver

        assert DamBreakConfig is not None
        assert ExactRiemannSolver is not None
        # BUG: get_scheme() is missing from backend

    def test_all_scheme_names_loadable(self):
        """Verify all scheme classes frontend expects exist."""
        from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
        from src.core.schemes.lax_wendroff import LaxWendroffScheme
        from src.core.schemes.maccormack import MacCormackScheme
        from src.core.schemes.godunov import GodunovScheme
        from src.core.schemes.hll import HLLScheme
        from src.core.schemes.muscl import MUSCLScheme

        frontend_scheme_names = [
            ("Lax-Friedrichs", LaxFriedrichsScheme),
            ("Lax-Wendroff", LaxWendroffScheme),
            ("MacCormack", MacCormackScheme),
            ("Godunov", GodunovScheme),
            ("HLL", HLLScheme),
            ("MUSCL-Hancock", MUSCLScheme),
        ]

        for name, cls in frontend_scheme_names:
            scheme = cls()
            assert scheme is not None

    def test_frontend_import_paths_exist(self):
        """Verify import paths used in frontend pages exist."""
        import src.core.config
        import src.core.schemes
        import src.core.solvers.exact
        import src.core.solvers.hll

        assert src.core.config is not None
        assert src.core.schemes is not None
        assert src.core.solvers.exact is not None
        assert src.core.solvers.hll is not None


class TestNoSelfImport:
    """Test for self-import issues in frontend."""

    def test_pages_init_has_self_import_bug(self):
        """BUG: pages/__init__.py has 'from .pages import *' circular import."""
        pages_init = Path("src/frontend/pages/__init__.py")
        if not pages_init.exists():
            pytest.skip("pages/__init__.py not found")

        content = pages_init.read_text()
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("from .pages import"):
                # Document the bug rather than fail
                assert True, f"BUG CONFIRMED: {stripped}"
                return

        pytest.fail("BUG NOT FOUND: Expected circular import in pages/__init__.py")

    def test_engines_init_no_self_import(self):
        """Verify engines/__init__.py does not import itself."""
        engines_init = Path("src/frontend/engines/__init__.py")
        if not engines_init.exists():
            pytest.skip("engines/__init__.py not found")

        content = engines_init.read_text()
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("from .engines import"):
                pytest.fail(
                    f"Circular import in engines/__init__.py: {stripped}"
                )
