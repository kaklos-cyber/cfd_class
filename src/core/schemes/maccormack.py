from typing import Callable, Dict, Optional

import numpy as np
from numpy.typing import NDArray

from src.core.config import DamBreakConfig
from src.core.schemes.base_scheme import BaseScheme


class MacCormackScheme(BaseScheme):
    def __init__(self) -> None:
        super().__init__(name="MacCormack", order=2, tvd=False)

    def evolve(
        self,
        U0: NDArray[np.float64],
        config: DamBreakConfig,
        progress_callback: Optional[Callable[[float, float], None]] = None,
    ) -> Dict[float, NDArray[np.float64]]:
        U = U0.copy()
        nx = config.nx
        dx = config.dx
        g = config.g

        time_history: Dict[float, NDArray[np.float64]] = {}
        time_history[0.0] = U.copy()

        t = 0.0
        snapshot_interval = config.t_end / 50

        while t < config.t_end:
            dt = self._compute_dt(U, config)
            if t + dt > config.t_end:
                dt = config.t_end - t

            F = self._compute_flux(U, g)
            U_star = U.copy()
            for i in range(1, nx - 1):
                U_star[:, i] = U[:, i] - (dt / dx) * (F[:, i + 1] - F[:, i])
            U_star = self._apply_bc(U_star)

            F_star = self._compute_flux(U_star, g)
            U_new = U.copy()
            for i in range(1, nx - 1):
                U_new[:, i] = 0.5 * (U[:, i] + U_star[:, i]) - (
                    0.5 * (dt / dx) * (F_star[:, i] - F_star[:, i - 1])
                )

            U = self._apply_bc(U_new)
            U = self._enforce_positivity(U)
            t += dt

            if (
                len(time_history) == 0
                or t >= list(time_history.keys())[-1] + snapshot_interval
            ):
                time_history[round(t, 6)] = U.copy()

            if progress_callback:
                progress_callback(t, config.t_end)

        return time_history
