"""Core computation engine module.

Contains:
- config: Simulation parameter configuration management
- schemes: Finite volume numerical schemes
- solvers: Riemann solvers and exact solutions
- analysis: Error analysis and convergence assessment
"""

from src.core.config import DamBreakConfig

__all__ = ["DamBreakConfig"]
