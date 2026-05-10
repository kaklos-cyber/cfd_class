from typing import Callable, Dict, Optional

import numpy as np
from numpy.typing import NDArray

from src.core.config import DamBreakConfig
from src.core.schemes.base_scheme import BaseScheme


class LaxFriedrichsScheme(BaseScheme):
    def __init__(self) -> None:
        super().__init__(name="Lax-Friedrichs", order=1, tvd=True)

    def evolve(
        self,
        U0: NDArray[np.float64],
        config: DamBreakConfig,
        progress_callback: Optional[Callable[[float, float], None]] = None,
    ) -> Dict[float, NDArray[np.float64]]:
        U = U0.copy()
        nx = config.x
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
            alpha = dx / dt

            F_half = np.zeros_like(F)
            for i in range(nx - 1):
                F_half[:, i] = 0.5 * (F[:, i] + F[:, i + 1]) - 0.5 * alpha * (
                    U[:, i + 1] - U[:, i]
                )

            U_new = U.copy()
            for i in range(1, nx - 1):
                U_new[:, i] = U[:, i] - (dt / dx) * (F_half[:, i] - F_half[:, i - 1])

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
