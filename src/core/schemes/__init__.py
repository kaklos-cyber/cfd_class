"""
有限体积数值格式包

Supported schemes:
- First-Order Upwind: Robust but diffusive
- Lax-Friedrichs: Centered diffusion
- HLL: Approximate Riemann solver
- Lax-Wendroff: Second-order predictor-corrector
- MacCormack: NASA predictor-corrector
- Beam-Warming: One-sided backward difference
- Fromm: Averaged scheme
- Godunov: Exact Riemann solver
- MUSCL-Hancock: TVD high-resolution
"""

from src.core.schemes.base_scheme import BaseScheme, SimulationResult
from src.core.schemes.upwind import UpwindScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.hll import HLLScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.beam_warming import BeamWarmingScheme
from src.core.schemes.fromm import FrommScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.muscl import MUSCLScheme

# Scheme aliases (frontend-friendly, without "Scheme" suffix)
Upwind = UpwindScheme
LaxFriedrichs = LaxFriedrichsScheme
HLL = HLLScheme
LaxWendroff = LaxWendroffScheme
MacCormack = MacCormackScheme
BeamWarming = BeamWarmingScheme
Fromm = FrommScheme
Godunov = GodunovScheme
MUSCLHancock = MUSCLScheme

# Scheme registry for factory function
_SCHEME_REGISTRY = {
    "First-Order Upwind": UpwindScheme,
    "Upwind": UpwindScheme,
    "Lax-Friedrichs": LaxFriedrichsScheme,
    "HLL": HLLScheme,
    "Lax-Wendroff": LaxWendroffScheme,
    "MacCormack": MacCormackScheme,
    "Beam-Warming": BeamWarmingScheme,
    "Fromm": FrommScheme,
    "Godunov": GodunovScheme,
    "MUSCL-Hancock": MUSCLScheme,
    "MUSCL": MUSCLScheme,
}


def get_scheme(name: str, **kwargs) -> BaseScheme:
    """Get a scheme instance by name.

    Factory function that creates scheme instances from string names.
    Supports both full names and short aliases.

    Args:
        name: Scheme name (e.g., "HLL", "MUSCL-Hancock", "Godunov")
        **kwargs: Additional arguments passed to scheme constructor
                  (e.g., g=9.81, limiter="minmod")

    Returns:
        BaseScheme: Instance of the requested scheme

    Raises:
        ValueError: If the scheme name is not recognized

    Examples:
        >>> scheme = get_scheme("HLL")
        >>> scheme = get_scheme("MUSCL-Hancock", limiter="superbee")
        >>> scheme = get_scheme("Godunov", g=9.8)
    """
    if name not in _SCHEME_REGISTRY:
        available = ", ".join(sorted(_SCHEME_REGISTRY.keys()))
        raise ValueError(
            f"Unknown scheme '{name}'. Available schemes: {available}"
        )
    scheme_cls = _SCHEME_REGISTRY[name]
    return scheme_cls(**kwargs)


def list_schemes() -> list[str]:
    """List all available scheme names.

    Returns:
        List of scheme names that can be passed to get_scheme().
    """
    return sorted(_SCHEME_REGISTRY.keys())


__all__ = [
    # Base classes
    "BaseScheme",
    "SimulationResult",
    # Scheme classes
    "UpwindScheme",
    "LaxFriedrichsScheme",
    "HLLScheme",
    "LaxWendroffScheme",
    "MacCormackScheme",
    "BeamWarmingScheme",
    "FrommScheme",
    "GodunovScheme",
    "MUSCLScheme",
    # Aliases
    "Upwind",
    "LaxFriedrichs",
    "HLL",
    "LaxWendroff",
    "MacCormack",
    "BeamWarming",
    "Fromm",
    "Godunov",
    "MUSCLHancock",
    # Factory functions
    "get_scheme",
    "list_schemes",
]
