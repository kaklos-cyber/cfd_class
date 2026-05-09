from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class DamBreakConfig:
    h_L: float = 1.0
    h_R: float = 0.0
    u_L: float = 0.0
    u_R: float = 0.0
    g: float = 9.81
    cfl: float = 0.9
    nx: int = 200
    t_end: float = 0.5
    x_min: float = -5.0
    x_max: float = 5.0

    def __post_init__(self) -> None:
        if self.h_L <= 0:
            raise ValueError("h_L must be positive")
        if self.h_R < 0:
            raise ValueError("h_R must be non-negative")
        if self.cfl <= 0 or self.cfl > 1.0:
            raise ValueError("CFL must be in (0, 1]")
        if self.nx < 10:
            raise ValueError("nx must be >= 10")
        if self.x_max <= self.x_min:
            raise ValueError("x_max must be greater than x_min")
        if self.t_end <= 0:
            raise ValueError("t_end must be positive")

    @property
    def dx(self) -> float:
        return (self.x_max - self.x_min) / self.nx

    @property
    def x_grid(self) -> NDArray[np.float64]:
        return np.linspace(
            self.x_min + self.dx / 2,
            self.x_max - self.dx / 2,
            self.nx,
        )

    def create_initial_condition(self) -> NDArray[np.float64]:
        x = self.x_grid
        h = np.where(x < 0, self.h_L, self.h_R)
        hu = np.where(x < 0, self.h_L * self.u_L, self.h_R * self.u_R)
        return np.array([h, hu], dtype=np.float64)
