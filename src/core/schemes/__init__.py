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

_SCHEME_REGISTRY = {
    "upwind": UpwindScheme,
    "Upwind": UpwindScheme,
    "lax-friedrichs": LaxFriedrichsScheme,
    "Lax-Friedrichs": LaxFriedrichsScheme,
    "LaxFriedrichs": LaxFriedrichsScheme,
    "hll": HLLScheme,
    "HLL": HLLScheme,
    "lax-wendroff": LaxWendroffScheme,
    "Lax-Wendroff": LaxWendroffScheme,
    "LaxWendroff": LaxWendroffScheme,
    "maccormack": MacCormackScheme,
    "MacCormack": MacCormackScheme,
    "beam-warming": BeamWarmingScheme,
    "Beam-Warming": BeamWarmingScheme,
    "BeamWarming": BeamWarmingScheme,
    "fromm": FrommScheme,
    "Fromm": FrommScheme,
    "godunov": GodunovScheme,
    "Godunov": GodunovScheme,
    "muscl": MUSCLScheme,
    "muscl-hancock": MUSCLScheme,
    "MUSCL-Hancock": MUSCLScheme,
    "MUSCLHancock": MUSCLScheme,
    "MUSCL": MUSCLScheme,
}

__all__ = [
    "BaseScheme",
    "SimulationResult",
    "UpwindScheme",
    "LaxFriedrichsScheme",
    "HLLScheme",
    "LaxWendroffScheme",
    "MacCormackScheme",
    "BeamWarmingScheme",
    "FrommScheme",
    "GodunovScheme",
    "MUSCLScheme",
    "get_scheme",
    "get_all_schemes",
]

HLL = HLLScheme
Godunov = GodunovScheme
LaxFriedrichs = LaxFriedrichsScheme
LaxWendroff = LaxWendroffScheme
MacCormack = MacCormackScheme
BeamWarming = BeamWarmingScheme
Fromm = FrommScheme
Upwind = UpwindScheme
MUSCLHancock = MUSCLScheme
MUSCL = MUSCLScheme


def get_scheme(name: str, **kwargs):
    """Get a scheme instance by name.

    Args:
        name: Scheme name (case-insensitive, supports multiple aliases)
        **kwargs: Additional arguments passed to scheme constructor

    Returns:
        Scheme instance

    Raises:
        ValueError: If scheme name is not recognized
    """
    name_lower = name.strip()
    if name_lower in _SCHEME_REGISTRY:
        return _SCHEME_REGISTRY[name_lower](**kwargs)

    for key, cls in _SCHEME_REGISTRY.items():
        if key.lower() == name_lower.lower():
            return cls(**kwargs)

    available = sorted(set(_SCHEME_REGISTRY.keys()))
    raise ValueError(
        f"Unknown scheme '{name}'. Available schemes: {available}"
    )


def get_all_schemes(**kwargs) -> dict:
    """Get all available scheme instances.

    Args:
        **kwargs: Arguments passed to all scheme constructors

    Returns:
        Dict mapping scheme name to instance
    """
    unique_classes = {}
    result = {}

    for name, cls in _SCHEME_REGISTRY.items():
        if cls not in unique_classes:
            unique_classes[cls] = name
            result[name] = cls(**kwargs)

    return result
