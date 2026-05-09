import pytest
import numpy as np

from src.core.config import DamBreakConfig


class TestDamBreakConfig:
    def test_default_values(self):
        config = DamBreakConfig()
        assert config.h_L == 1.0
        assert config.h_R == 0.0
        assert config.u_L == 0.0
        assert config.u_R == 0.0
        assert config.g == 9.81
        assert config.cfl == 0.9
        assert config.nx == 200
        assert config.t_end == 0.5
        assert config.x_min == -5.0
        assert config.x_max == 5.0

    def test_invalid_h_L(self):
        with pytest.raises(ValueError):
            DamBreakConfig(h_L=0.0)
        with pytest.raises(ValueError):
            DamBreakConfig(h_L=-1.0)

    def test_invalid_h_R(self):
        with pytest.raises(ValueError):
            DamBreakConfig(h_R=-0.1)

    def test_invalid_cfl(self):
        with pytest.raises(ValueError):
            DamBreakConfig(cfl=0.0)
        with pytest.raises(ValueError):
            DamBreakConfig(cfl=1.1)

    def test_invalid_nx(self):
        with pytest.raises(ValueError):
            DamBreakConfig(nx=5)

    def test_frozen_config(self):
        config = DamBreakConfig()
        with pytest.raises(AttributeError):
            config.h_L = 2.0

    def test_dx_property(self):
        config = DamBreakConfig(nx=100, x_min=0, x_max=10)
        assert config.dx == pytest.approx(0.1)

    def test_x_grid_property(self):
        config = DamBreakConfig(nx=10, x_min=0, x_max=10)
        expected = np.linspace(0.5, 9.5, 10)
        np.testing.assert_array_almost_equal(config.x_grid, expected)

    def test_create_initial_condition(self):
        config = DamBreakConfig(nx=10, x_min=-5, x_max=5)
        U0 = config.create_initial_condition()
        assert U0.shape == (2, 10)
        assert U0[0, 0] == 1.0
        assert U0[0, -1] == 0.0
