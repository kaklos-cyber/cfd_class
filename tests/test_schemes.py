import pytest
import numpy as np

from src.core.config import DamBreakConfig
from src.core.schemes import (
    BaseScheme,
    LaxFriedrichsScheme,
    LaxWendroffScheme,
    MacCormackScheme,
    GodunovScheme,
    HLLScheme,
    MUSCLHancockScheme,
    get_scheme_by_name,
)


class TestBaseScheme:
    def test_abstract_class(self):
        with pytest.raises(TypeError):
            BaseScheme("test", 1)

    def test_compute_dt(self):
        scheme = LaxFriedrichsScheme()
        config = DamBreakConfig()
        U = np.array([[1.0, 1.0, 1.0], [0.0, 0.0, 0.0]])

        dt = scheme._compute_dt(U, config)

        assert dt > 0
        assert np.isfinite(dt)

    def test_apply_bc(self):
        scheme = LaxFriedrichsScheme()
        U = np.array([[1.0, 2.0, 3.0, 4.0], [0.1, 0.2, 0.3, 0.4]])

        U_bc = scheme._apply_bc(U)

        assert U_bc[0, 0] == U_bc[0, 1]
        assert U_bc[0, -1] == U_bc[0, -2]


class TestLaxFriedrichsScheme:
    def test_initialization(self):
        scheme = LaxFriedrichsScheme()
        assert scheme.name == "Lax-Friedrichs"
        assert scheme.order == 1
        assert scheme.tvd is True

    def test_evolve(self):
        config = DamBreakConfig(nx=50, t_end=0.1)
        U0 = config.create_initial_condition()
        scheme = LaxFriedrichsScheme()

        result = scheme.evolve(U0, config)

        assert isinstance(result, dict)
        assert 0.0 in result
        assert max(result.keys()) >= 0.1


class TestSchemesIntegration:
    @pytest.mark.parametrize("scheme_class", [
        LaxFriedrichsScheme,
        LaxWendroffScheme,
        MacCormackScheme,
        GodunovScheme,
        HLLScheme,
        MUSCLHancockScheme,
    ])
    def test_all_schemes_run(self, scheme_class):
        config = DamBreakConfig(nx=100, t_end=0.2)
        U0 = config.create_initial_condition()
        scheme = scheme_class()

        result = scheme.evolve(U0, config)

        assert isinstance(result, dict)
        final_time = max(result.keys())
        U_final = result[final_time]

        assert U_final.shape == U0.shape
        assert np.all(U_final[0, :] >= 0)

    def test_get_scheme_by_name(self):
        scheme = get_scheme_by_name("Lax-Friedrichs")
        assert isinstance(scheme, LaxFriedrichsScheme)

        scheme = get_scheme_by_name("hll")
        assert isinstance(scheme, HLLScheme)

        with pytest.raises(ValueError):
            get_scheme_by_name("unknown")
