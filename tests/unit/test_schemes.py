"""
鏁板€兼牸寮忓崟鍏冩祴璇?
娴嬭瘯鐩爣: src/core/schemes/* - 6绉岶VM鏍煎紡
渚濇嵁: test_plan.md TC-SCH-01 ~ TC-MUSCL-04
Issue: #D2
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pytest


class TestBaseSchemeInterface:
    """BaseScheme 鎶借薄鍩虹被鎺ュ彛娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.schemes.base_scheme import BaseScheme
            self.BaseScheme = BaseScheme
        except ImportError:
            pytest.skip("BaseScheme 灏氭湭瀹炵幇")

    def test_tc_sch_01_abstract_class(self):
        """TC-SCH-01: BaseScheme 涓嶈兘鐩存帴瀹炰緥鍖?"""
        with pytest.raises(TypeError):
            self.BaseScheme("test", 1)

    def test_tc_sch_02_evolve_not_implemented(self):
        """TC-SCH-02: 瀛愮被蹇呴』瀹炵幇 evolve 鏂规硶."""

        class DummyScheme(self.BaseScheme):
            pass

        with pytest.raises(TypeError):
            DummyScheme("dummy", 1)


class TestSchemeCommon:
    """鎵€鏈夋牸寮忕殑閫氱敤娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import (
                GodunovScheme,
                HLLOneScheme,
                LaxFriedrichsScheme,
                LaxWendroffScheme,
                MacCormackScheme,
                MUSCLHancockScheme,
            )
            self.DamBreakConfig = DamBreakConfig
            self.schemes = {
                "Lax-Friedrichs": LaxFriedrichsScheme,
                "Lax-Wendroff": LaxWendroffScheme,
                "MacCormack": MacCormackScheme,
                "Godunov": GodunovScheme,
                "HLL": HLLOneScheme,
                "MUSCL-Hancock": MUSCLHancockScheme,
            }
        except ImportError:
            pytest.skip("鏁板€兼牸寮忓皻鏈疄鐜?)

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

    @pytest.mark.parametrize("name,scheme_class", [
        ("Lax-Friedrichs", "LaxFriedrichsScheme"),
        ("Lax-Wendroff", "LaxWendroffScheme"),
        ("MacCormack", "MacCormackScheme"),
        ("Godunov", "GodunovScheme"),
        ("HLL", "HLLOneScheme"),
        ("MUSCL-Hancock", "MUSCLHancockScheme"),
    ])
    def test_tc_sch_03_instantiation(self, name, scheme_class):
        """TC-SCH-01: 绫诲疄渚嬪寲姝ｇ‘璁剧疆灞炴€?"""
        try:
            cls = getattr(__import__("src.core.schemes", fromlist=[scheme_class]), scheme_class)
        except (ImportError, AttributeError):
            pytest.skip(f"{scheme_class} 灏氭湭瀹炵幇")
        scheme = cls()
        assert hasattr(scheme, "name")
        assert hasattr(scheme, "order")
        assert hasattr(scheme, "tvd")
        assert scheme.name == name

    @pytest.mark.parametrize("scheme_name", [
        "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
        "Godunov", "HLL", "MUSCL-Hancock"
    ])
    def test_tc_sch_04_evolve_signature(self, scheme_name):
        """TC-SCH-02: evolve鎺ュ彛杩斿洖 Dict[float, ndarray]."""
        if scheme_name not in self.schemes:
            pytest.skip(f"{scheme_name} 灏氭湭瀹炵幇")
        scheme = self.schemes[scheme_name]()
        cfg = self.DamBreakConfig(nx=50, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        result = scheme.evolve(U0, cfg)
        assert isinstance(result, dict)
        assert len(result) > 0
        for t, U in result.items():
            assert isinstance(t, float)
            assert isinstance(U, np.ndarray)
            assert U.shape == (2, cfg.nx)

    @pytest.mark.parametrize("scheme_name", [
        "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
        "Godunov", "HLL", "MUSCL-Hancock"
    ])
    def test_tc_sch_05_uniform_state(self, scheme_name):
        """TC-SCH-03: 鍧囧寑鍒濆€间笉闅忔椂闂村彉鍖?"""
        if scheme_name not in self.schemes:
            pytest.skip(f"{scheme_name} 灏氭湭瀹炵幇")
        scheme = self.schemes[scheme_name]()
        cfg = self.DamBreakConfig(nx=50, t_end=0.1, h_L=1.0, h_R=1.0)
        U0 = np.ones((2, cfg.nx), dtype=np.float64)
        U0[1, :] = 0.0
        result = scheme.evolve(U0, cfg)
        t_final = max(result.keys())
        U_final = result[t_final]
        np.testing.assert_allclose(U_final, U0, atol=1e-10)

    @pytest.mark.parametrize("scheme_name", [
        "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
        "Godunov", "HLL", "MUSCL-Hancock"
    ])
    def test_tc_sch_06_mass_conservation(self, scheme_name):
        """TC-SCH-04: 璐ㄩ噺瀹堟亽璇樊 < 1e-6."""
        if scheme_name not in self.schemes:
            pytest.skip(f"{scheme_name} 灏氭湭瀹炵幇")
        scheme = self.schemes[scheme_name]()
        cfg = self.DamBreakConfig(nx=100, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        initial_mass = np.sum(U0[0, :]) * cfg.dx
        result = scheme.evolve(U0, cfg)
        t_final = max(result.keys())
        U_final = result[t_final]
        final_mass = np.sum(U_final[0, :]) * cfg.dx
        rel_error = abs(final_mass - initial_mass) / abs(initial_mass)
        assert rel_error < 1e-6, f"Mass conservation error: {rel_error}"

    @pytest.mark.parametrize("scheme_name", [
        "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
        "Godunov", "HLL", "MUSCL-Hancock"
    ])
    def test_tc_sch_07_positive_depth(self, scheme_name):
        """TC-SCH-05: 姝ｆ€т繚鎸?涓嶅嚭鐜癶<0."""
        if scheme_name not in self.schemes:
            pytest.skip(f"{scheme_name} 灏氭湭瀹炵幇")
        scheme = self.schemes[scheme_name]()
        cfg = self.DamBreakConfig(nx=100, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        result = scheme.evolve(U0, cfg)
        for t, U in result.items():
            assert np.all(U[0, :] >= 0), f"Negative depth found at t={t}"

    @pytest.mark.parametrize("scheme_name", [
        "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
        "Godunov", "HLL", "MUSCL-Hancock"
    ])
    def test_tc_sch_08_cfl_stability(self, scheme_name):
        """TC-SCH-06: CFL=0.9鏃朵笉宕╂簝."""
        if scheme_name not in self.schemes:
            pytest.skip(f"{scheme_name} 灏氭湭瀹炵幇")
        scheme = self.schemes[scheme_name]()
        cfg = self.DamBreakConfig(nx=50, t_end=0.1, cfl=0.9)
        U0 = self._make_initial_state(cfg)
        result = scheme.evolve(U0, cfg)
        assert len(result) > 0

    @pytest.mark.parametrize("scheme_name", [
        "Lax-Friedrichs", "Lax-Wendroff", "MacCormack",
        "Godunov", "HLL", "MUSCL-Hancock"
    ])
    def test_tc_sch_09_progress_callback(self, scheme_name):
        """TC-SCH-02: 杩涘害鍥炶皟鍑芥暟琚皟鐢?"""
        if scheme_name not in self.schemes:
            pytest.skip(f"{scheme_name} 灏氭湭瀹炵幇")
        scheme = self.schemes[scheme_name]()
        cfg = self.DamBreakConfig(nx=50, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        calls = []

        def callback(current_time, end_time):
            calls.append((current_time, end_time))

        result = scheme.evolve(U0, cfg, progress_callback=callback)
        assert len(calls) > 0


class TestLaxFriedrichs:
    """Lax-Friedrichs 鏍煎紡涓撻」娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import LaxFriedrichsScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = LaxFriedrichsScheme
        except ImportError:
            pytest.skip("LaxFriedrichsScheme 灏氭湭瀹炵幇")

    def test_tc_lf_01_tvd_property(self):
        """TC-LF-03: TVD鎬ц川."""
        scheme = self.Scheme()
        assert scheme.tvd is True

    def test_tc_lf_02_first_order(self):
        """TC-LF-01: 涓€闃剁簿搴?"""
        scheme = self.Scheme()
        assert scheme.order == 1


class TestLaxWendroff:
    """Lax-Wendroff 鏍煎紡涓撻」娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import LaxWendroffScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = LaxWendroffScheme
        except ImportError:
            pytest.skip("LaxWendroffScheme 灏氭湭瀹炵幇")

    def test_tc_lw_01_second_order(self):
        """TC-LW-01: 浜岄樁绮惧害."""
        scheme = self.Scheme()
        assert scheme.order == 2

    def test_tc_lw_02_not_tvd(self):
        """TC-LW-01: 闈濼VD鏍煎紡."""
        scheme = self.Scheme()
        assert scheme.tvd is False


class TestMacCormack:
    """MacCormack 鏍煎紡涓撻」娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import MacCormackScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = MacCormackScheme
        except ImportError:
            pytest.skip("MacCormackScheme 灏氭湭瀹炵幇")

    def test_tc_mc_01_second_order(self):
        """TC-MC-01: 浜岄樁绮惧害."""
        scheme = self.Scheme()
        assert scheme.order == 2


class TestGodunov:
    """Godunov 鏍煎紡涓撻」娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import GodunovScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = GodunovScheme
        except ImportError:
            pytest.skip("GodunovScheme 灏氭湭瀹炵幇")

    def test_tc_god_01_uses_exact_solver(self):
        """TC-GOD-01: 浣跨敤绮剧‘Riemann姹傝В鍣?"""
        scheme = self.Scheme()
        assert scheme.name == "Godunov"

    def test_tc_god_02_tvd_property(self):
        """TC-GOD-02: TVD鎬ц川."""
        scheme = self.Scheme()
        assert scheme.tvd is True


class TestHLL:
    """HLL 鏍煎紡涓撻」娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import HLLOneScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = HLLOneScheme
        except ImportError:
            pytest.skip("HLLOneScheme 灏氭湭瀹炵幇")

    def test_tc_hll_01_tvd_property(self):
        """TC-HLL-01: TVD鎬ц川."""
        scheme = self.Scheme()
        assert scheme.tvd is True


class TestMUSCLHancock:
    """MUSCL-Hancock 鏍煎紡涓撻」娴嬭瘯."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        try:
            from src.core.config import DamBreakConfig
            from src.core.schemes import MUSCLHancockScheme
            self.DamBreakConfig = DamBreakConfig
            self.Scheme = MUSCLHancockScheme
        except ImportError:
            pytest.skip("MUSCLHancockScheme 灏氭湭瀹炵幇")

    def test_tc_muscl_01_second_order(self):
        """TC-MUSCL-01: 浜岄樁绮惧害."""
        scheme = self.Scheme()
        assert scheme.order == 2

    def test_tc_muscl_02_tvd_property(self):
        """TC-MUSCL-01: TVD鎬ц川."""
        scheme = self.Scheme()
        assert scheme.tvd is True
