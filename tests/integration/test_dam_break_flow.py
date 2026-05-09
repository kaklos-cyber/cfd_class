"""
集成测试 - 完整溃坝流程

测试目标: 端到端模拟流程、多格式对比、异常处理
依据: test_plan.md TC-INT-01 ~ TC-INT-08
Issue: #D3
"""

import numpy as np
import pytest


class TestEndToEndDamBreak:
    """端到端溃坝模拟测试."""

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
            self.schemes = [
                LaxFriedrichsScheme,
                LaxWendroffScheme,
                MacCormackScheme,
                GodunovScheme,
                HLLOneScheme,
                MUSCLHancockScheme,
            ]
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

    @pytest.mark.integration
    def test_tc_int_01_dry_bed_end_to_end(self):
        """TC-INT-01: 端到端干底模拟完整流程无异常."""
        cfg = self.DamBreakConfig(nx=100, t_end=0.1, h_L=1.0, h_R=0.0)
        U0 = self._make_initial_state(cfg)
        scheme = self.schemes[0]()
        result = scheme.evolve(U0, cfg)
        assert len(result) > 0
        t_final = max(result.keys())
        assert t_final > 0

    @pytest.mark.integration
    def test_tc_int_02_all_schemes_run(self):
        """TC-INT-02: 六格式并行运行均正常."""
        cfg = self.DamBreakConfig(nx=50, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        results = {}
        for scheme_cls in self.schemes:
            scheme = scheme_cls()
            result = scheme.evolve(U0, cfg)
            results[scheme.name] = result
            assert len(result) > 0, f"{scheme.name} 无输出"
        assert len(results) == 6

    @pytest.mark.integration
    def test_tc_int_03_result_consistency(self):
        """TC-INT-03: 相同输入相同输出."""
        cfg = self.DamBreakConfig(nx=50, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        scheme = self.schemes[0]()
        result1 = scheme.evolve(U0, cfg)
        result2 = scheme.evolve(U0, cfg)
        assert list(result1.keys()) == list(result2.keys())
        for t in result1:
            np.testing.assert_array_equal(result1[t], result2[t])

    @pytest.mark.integration
    def test_tc_int_04_config_serialization(self):
        """TC-INT-04: DamBreakConfig可pickle序列化."""
        import pickle
        cfg = self.DamBreakConfig()
        serialized = pickle.dumps(cfg)
        cfg_restored = pickle.loads(serialized)
        assert cfg_restored.h_L == cfg.h_L
        assert cfg_restored.nx == cfg.nx

    @pytest.mark.integration
    def test_tc_int_05_progress_callback(self):
        """TC-INT-05: 进度回调被调用."""
        cfg = self.DamBreakConfig(nx=50, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        scheme = self.schemes[0]()
        calls = []

        def callback(current_time, end_time):
            calls.append((current_time, end_time))

        scheme.evolve(U0, cfg, progress_callback=callback)
        assert len(calls) > 0

    @pytest.mark.integration
    def test_tc_int_06_invalid_parameter_handling(self):
        """TC-INT-06: 无效参数给出友好错误."""
        with pytest.raises(ValueError):
            self.DamBreakConfig(cfl=2.0)
        with pytest.raises(ValueError):
            self.DamBreakConfig(nx=5)

    @pytest.mark.integration
    @pytest.mark.slow
    def test_tc_int_07_long_time_simulation(self):
        """TC-INT-07: 长时间模拟 t_end=1.0 正常完成."""
        cfg = self.DamBreakConfig(nx=100, t_end=1.0)
        U0 = self._make_initial_state(cfg)
        scheme = self.schemes[0]()
        result = scheme.evolve(U0, cfg)
        assert len(result) > 0

    @pytest.mark.integration
    def test_tc_int_08_coarse_grid(self):
        """TC-INT-08: 粗网格 nx=50 不崩溃."""
        cfg = self.DamBreakConfig(nx=50, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        for scheme_cls in self.schemes:
            scheme = scheme_cls()
            result = scheme.evolve(U0, cfg)
            assert len(result) > 0


class TestMultiSchemeComparison:
    """多格式对比集成测试."""

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
            from src.core.analysis.error_analysis import compute_error
            self.DamBreakConfig = DamBreakConfig
            self.schemes = [
                LaxFriedrichsScheme,
                LaxWendroffScheme,
                MacCormackScheme,
                GodunovScheme,
                HLLOneScheme,
                MUSCLHancockScheme,
            ]
            self.compute_error = compute_error
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

    @pytest.mark.integration
    def test_all_schemes_produce_different_results(self):
        """不同格式产生不同结果（一阶 vs 二阶）."""
        cfg = self.DamBreakConfig(nx=100, t_end=0.1)
        U0 = self._make_initial_state(cfg)
        final_results = {}
        for scheme_cls in self.schemes:
            scheme = scheme_cls()
            result = scheme.evolve(U0, cfg)
            t_final = max(result.keys())
            final_results[scheme.name] = result[t_final]

        lf_result = final_results.get("Lax-Friedrichs")
        lw_result = final_results.get("Lax-Wendroff")
        if lf_result is not None and lw_result is not None:
            diff = np.max(np.abs(lf_result - lw_result))
            assert diff > 1e-6, "一阶和二阶格式结果应不同"

    @pytest.mark.integration
    def test_tvd_schemes_no_oscillations(self):
        """TVD格式在激波处无振荡."""
        cfg = self.DamBreakConfig(nx=200, t_end=0.1, h_L=2.0, h_R=1.0)
        U0 = self._make_initial_state(cfg)
        tvd_schemes = [s for s in self.schemes if s().tvd]
        for scheme_cls in tvd_schemes:
            scheme = scheme_cls()
            result = scheme.evolve(U0, cfg)
            t_final = max(result.keys())
            U_final = result[t_final]
            h = U_final[0, :]
            total_variation = np.sum(np.abs(np.diff(h)))
            initial_tv = np.sum(np.abs(np.diff(U0[0, :])))
            assert total_variation <= initial_tv * 1.01, f"{scheme.name} 违反TVD性质"
