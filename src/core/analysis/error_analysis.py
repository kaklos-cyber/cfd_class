from typing import Dict, List, Union

import numpy as np
from numpy.typing import NDArray


def compute_error(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    p: Union[int, float] = 2,
    dx: float = 1.0,
) -> float:
    diff = np.abs(numerical - exact)

    if p == float("inf") or p == np.inf:
        return float(np.max(diff))
    elif p == 1:
        return float(dx * np.sum(diff))
    elif p == 2:
        return float(np.sqrt(dx * np.sum(diff**2)))
    else:
        return float((dx * np.sum(diff**p)) ** (1.0 / p))


def compute_all_errors(
    numerical: NDArray[np.float64],
    exact: NDArray[np.float64],
    dx: float = 1.0,
) -> Dict[str, float]:
    return {
        "L1": compute_error(numerical, exact, p=1, dx=dx),
        "L2": compute_error(numerical, exact, p=2, dx=dx),
        "Linf": compute_error(numerical, exact, p=np.inf, dx=dx),
    }


def estimate_order(
    nx_list: List[int],
    errors: List[float],
) -> float:
    if len(nx_list) != len(errors):
        raise ValueError("nx_list and errors must have the same length")
    if len(nx_list) < 2:
        raise ValueError("need at least 2 data points to estimate order")

    log_nx = np.log(np.array(nx_list))
    log_errors = np.log(np.array(errors))

    coeffs = np.polyfit(log_nx, log_errors, 1)
    return float(-coeffs[0])


def compute_mass_conservation_error(
    U_initial: NDArray[np.float64],
    U_final: NDArray[np.float64],
    dx: float,
) -> float:
    mass_initial = dx * np.sum(U_initial[0, :])
    mass_final = dx * np.sum(U_final[0, :])
    return float(abs(mass_final - mass_initial) / mass_initial)
