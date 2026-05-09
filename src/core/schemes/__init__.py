from src.core.schemes.base_scheme import BaseScheme
from src.core.schemes.godunov import GodunovScheme
from src.core.schemes.hll import HLLScheme
from src.core.schemes.lax_friedrichs import LaxFriedrichsScheme
from src.core.schemes.lax_wendroff import LaxWendroffScheme
from src.core.schemes.maccormack import MacCormackScheme
from src.core.schemes.muscl_hancock import MUSCLHancockScheme

__all__ = [
    "BaseScheme",
    "LaxFriedrichsScheme",
    "LaxWendroffScheme",
    "MacCormackScheme",
    "GodunovScheme",
    "HLLScheme",
    "MUSCLHancockScheme",
]

SCHEMES = [
    LaxFriedrichsScheme,
    LaxWendroffScheme,
    MacCormackScheme,
    GodunovScheme,
    HLLScheme,
    MUSCLHancockScheme,
]


def get_scheme_by_name(name: str) -> BaseScheme:
    name_lower = name.lower()
    if name_lower == "lax-friedrichs":
        return LaxFriedrichsScheme()
    elif name_lower == "lax-wendroff":
        return LaxWendroffScheme()
    elif name_lower == "maccormack":
        return MacCormackScheme()
    elif name_lower == "godunov":
        return GodunovScheme()
    elif name_lower == "hll":
        return HLLScheme()
    elif name_lower == "muscl-hancock":
        return MUSCLHancockScheme()
    raise ValueError(f"Unknown scheme: {name}")
