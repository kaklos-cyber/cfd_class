from typing import Callable, Dict, Optional

import numpy as np
from numpy.typing import NDArray

from src.core.config import DamBreakConfig
from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.riemann_solver import exact_riemann_solution

EPS_H = 1e-12


class MUSCLHancockScheme(BaseScheme):
    def __init__(self) -> None:
        super().__init__(name="MUSCL-Hancock", order=2, tvd=True)

    @staticmethod
    def _minmod(a: float, b: float) -> float:
        if a * b > 0:
            return float(np.sign(a) * min(abs(a), abs(b)))
        return 0.0

    def _reconstruct(
        self,
        U: NDArray[np.float64],
        i: int,
        dx: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        nx = U.shape[1]
        U_L = np.zeros(2)
        U_R = np.zeros(2)

        for m in range(2):
            if i == 0:
                du = U[m, i + 1] - U[m, i]
                delta = self._minmod(du, du)
                U_L[m] = U[m, i] + delta / 2
                U_R[m] = U[m, i + 1] - delta / 2
            elif i == nx - 2:
                du = U[m, i + 1] - U[m, i]
                delta = self._minmod(du, du)
                U_L[m] = U[m, i] + delta / 2
                U_R[m] = U[m, i + 1] - delta / 2
            else:
                du1 = U[m, i] - U[m, i - 1]
                du2 = U[m, i + 1] - U[m, i]
                du3 = U[m, i + 2] - U[m, i + 1]

                delta_l = self._minmod(du1, du2)
                delta_r = self._minmod(du2, du3)

                U_L[m] = U[m, i] + delta_l / 2
                U_R[m] = U[m, i + 1] - delta_r / 2

        U_L[0] = max(U_L[0], EPS_H)
        U_R[0] = max(U_R[0], EPS_H)

        return U_L, U_R

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

            F_half = np.zeros((2, nx - 1))
            for i in range(nx - 1):
                U_L, U_R = self._reconstruct(U, i, dx)
                riemann_sol = exact_riemann_solution(U_L, U_R, g)

                S_L = riemann_sol["S_L"]
                S_R = riemann_sol["S_R"]
                h_star = riemann_sol["h_star"]
                u_star = riemann_sol["u_star"]

                if S_L >= 0:
                    h = U_L[0]
                    hu = U_L[1]
                    u = hu / h if h > EPS_H else 0.0
                elif S_R <= 0:
                    h = U_R[0]
                    hu = U_R[1]
                    u = hu / h if h > EPS_H else 0.0
                else:
                    h = h_star
                    hu = h_star * u_star
                    u = u_star

                F_half[0, i] = hu
                F_half[1, i] = hu * u + 0.5 * g * h * h

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
