"""Frontend-friendly adapter for the exact Riemann solver.

Provides a simplified interface that accepts DamBreakConfig and returns
results in the format expected by the frontend.
"""

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from src.core.solvers.exact import ExactRiemannSolver

if TYPE_CHECKING:
    from src.core.config import DamBreakConfig


class ExactRiemann:
    """Frontend adapter for the exact Riemann solver.

    Wraps ExactRiemannSolver to provide a config-based interface
    that returns results in the frontend's expected format.

    Example:
        >>> from src.core.config import DamBreakConfig
        >>> from src.core.solvers.exact_riemann import ExactRiemann
        >>> config = DamBreakConfig(nx=100, t_end=10.0)
        >>> solver = ExactRiemann(config)
        >>> exact_solution = solver.solve(config)
        >>> h = exact_solution[0]  # water depth array
        >>> u = exact_solution[1]  # velocity array
    """

    def __init__(self, config: "DamBreakConfig"):
        """Initialize solver with configuration.

        Args:
            config: DamBreakConfig with physical and numerical parameters
        """
        self.config = config
        self._solver = ExactRiemannSolver(g=config.g)

    def solve(
        self,
        config: "DamBreakConfig",
    ) -> NDArray[np.float64]:
        """Solve exact Riemann problem and return frontend-friendly output.

        Args:
            config: DamBreakConfig (can be different from init config)

        Returns:
            np.ndarray of shape (2, nx) where:
                - array[0] = water depth h at each grid point
                - array[1] = velocity u at each grid point
        """
        h_l = config.h_l
        u_l = config.u_l
        h_r = config.h_r
        u_r = config.u_r
        x = config.x
        t = config.t_end
        x0 = config.x_dam

        h, u = self._solver.sample_solution(h_l, u_l, h_r, u_r, x, t, x0)

        return np.vstack([h, u])

    def solve_at_time(
        self,
        t: float,
    ) -> NDArray[np.float64]:
        """Solve exact Riemann problem at a specific time.

        Uses the configuration stored during initialization.

        Args:
            t: Time [s] at which to evaluate the solution

        Returns:
            np.ndarray of shape (2, nx) where:
                - array[0] = water depth h at each grid point
                - array[1] = velocity u at each grid point
        """
        h_l = self.config.h_l
        u_l = self.config.u_l
        h_r = self.config.h_r
        u_r = self.config.u_r
        x = self.config.x
        x0 = self.config.x_dam

        h, u = self._solver.sample_solution(h_l, u_l, h_r, u_r, x, t, x0)

        return np.vstack([h, u])
