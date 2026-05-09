from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional

import numpy as np
from numpy.typing import NDArray

from src.core.config import DamBreakConfig

EPS_H = 1e-12


class BaseScheme(ABC):
    def __init__(self, name: str, order: int, tvd: bool = False) -> None:
        self.name = name
        self.order = order
        self.tvd = tvd

    @abstractmethod
    def evolve(
        self,
        U0: NDArray[np.float64],
        config: DamBreakConfig,
        progress_callback: Optional[Callable[[float, float], None]] = None,
    ) -> Dict[float, NDArray[np.float64]]:
        pass

    def _compute_dt(self, U: NDArray[np.float64], config: DamBreakConfig) -> float:
        h = U[0, :]
        safe_h = np.maximum(h, EPS_H)
        u = U[1, :] / safe_h
        c = np.sqrt(config.g * safe_h)
        max_speed = np.max(np.abs(u) + c)
        return float(config.cfl * config.dx / max_speed)

    def _apply_bc(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        U[:, 0] = U[:, 1]
        U[:, -1] = U[:, -2]
        return U

    def _enforce_positivity(self, U: NDArray[np.float64]) -> NDArray[np.float64]:
        U[0, :] = np.maximum(U[0, :], EPS_H)
        return U

    @staticmethod
    def _compute_flux(U: NDArray[np.float64], g: float) -> NDArray[np.float64]:
        h = U[0, :]
        hu = U[1, :]
        safe_h = np.maximum(h, EPS_H)
        u = hu / safe_h
        F0 = hu
        F1 = hu * u + 0.5 * g * h * h
        return np.array([F0, F1], dtype=np.float64)
