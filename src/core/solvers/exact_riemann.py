"""Exact Riemann solver adapter for frontend compatibility.

Provides the ExactRiemann class interface expected by the frontend engines,
wrapping the underlying ExactRiemannSolver from src.core.solvers.exact.
"""

import numpy as np
from numpy.typing import NDArray

from src.core.solvers.exact import ExactRiemannSolver


class ExactRiemann:
    """Frontend-compatible exact Riemann solver adapter.

    Wraps ExactRiemannSolver to provide the config-based API expected
    by simulation_engine.py and comparison_engine.py.

    Usage:
        solver = ExactRiemann(config)
        result = solver.solve(config)  # returns (2, nx) array [h; u]
    """

    def __init__(self, config):
        """Initialize with DamBreakConfig.

        Args:
            config: DamBreakConfig instance containing simulation parameters
        """
        self.config = config
        self._solver = ExactRiemannSolver(
            g=config.g,
        )

    def solve(self, config=None):
        """Solve exact Riemann problem and return solution array.

        Args:
            config: DamBreakConfig (uses self.config if None)

        Returns:
            NDArray of shape (2, nx) containing [h_values; u_values]
            at final time t_end across all cell centers
        """
        cfg = config or self.config

        x = cfg.x
        t = cfg.t_end
        x0 = cfg.x_dam

        h, u = self._solver.sample_solution(
            h_l=cfg.h_l,
            u_l=cfg.u_l,
            h_r=cfg.h_r,
            u_r=cfg.u_r,
            x=x,
            t=t,
            x0=x0,
        )

        return np.vstack([h, u])
