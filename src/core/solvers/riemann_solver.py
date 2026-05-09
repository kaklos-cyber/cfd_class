from typing import Dict

import numpy as np
from numpy.typing import NDArray

EPS_H = 1e-12


def exact_riemann_solution(
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float,
) -> Dict[str, float]:
    h_L, hu_L = U_L
    h_R, hu_R = U_R

    u_L = hu_L / h_L if h_L > EPS_H else 0.0
    u_R = hu_R / h_R if h_R > EPS_H else 0.0

    if h_R < EPS_H:
        return _solve_dry_ritter(h_L, u_L, g)

    if abs(h_L - h_R) < EPS_H and abs(u_L - u_R) < EPS_H:
        return {
            "S_L": u_L - np.sqrt(g * h_L),
            "S_R": u_R + np.sqrt(g * h_R),
            "S_star": u_L,
            "h_star": h_L,
            "u_star": u_L,
            "type": "uniform",
        }

    return _solve_wet_case(h_L, u_L, h_R, u_R, g)


def _solve_dry_ritter(
    h_L: float,
    u_L: float,
    g: float,
) -> Dict[str, float]:
    c_L = np.sqrt(g * h_L)
    S_L = u_L - c_L
    S_star = u_L / 3 + 2 * c_L / 3
    h_star = (2.0 / 3.0 * (c_L + u_L / 2.0)) ** 2 / g

    return {
        "S_L": S_L,
        "S_R": S_star,
        "S_star": S_star,
        "h_star": h_star,
        "u_star": S_star,
        "type": "dry_ritter",
    }


def _solve_wet_case(
    h_L: float,
    u_L: float,
    h_R: float,
    u_R: float,
    g: float,
) -> Dict[str, float]:
    c_L = np.sqrt(g * h_L)
    c_R = np.sqrt(g * h_R)

    def f(h: float) -> float:
        if h <= h_L:
            term_L = 2 * c_L * (1 - np.sqrt(h / h_L))
        else:
            term_L = (h - h_L) * np.sqrt(g / (2 * h + h_L))

        if h <= h_R:
            term_R = 2 * c_R * (1 - np.sqrt(h / h_R))
        else:
            term_R = (h - h_R) * np.sqrt(g / (2 * h + h_R))

        return float(term_L + term_R + (u_R - u_L))

    def df(h: float) -> float:
        if h <= h_L:
            df_L = -c_L / np.sqrt(g * h * h_L)
        else:
            df_L = np.sqrt(g / (2 * h + h_L)) * (
                1 - (h - h_L) / (2 * (2 * h + h_L))
            )

        if h <= h_R:
            df_R = -c_R / np.sqrt(g * h * h_R)
        else:
            df_R = np.sqrt(g / (2 * h + h_R)) * (
                1 - (h - h_R) / (2 * (2 * h + h_R))
            )

        return float(df_L + df_R)

    h_guess = 0.5 * (h_L + h_R)

    for _ in range(50):
        f_val = f(h_guess)
        df_val = df(h_guess)
        if abs(df_val) < EPS_H:
            break
        h_new = h_guess - f_val / df_val
        if h_new < EPS_H:
            h_new = EPS_H
        if abs(h_new - h_guess) < 1e-12:
            break
        h_guess = h_new

    h_star = h_guess

    if h_star <= h_L:
        S_L = u_L - c_L * (1 + 0.5 * (h_star - h_L) / h_L)
    else:
        S_L = u_L - np.sqrt(g * h_L) * np.sqrt(0.5 * (h_star + h_L) / h_L)

    if h_star <= h_R:
        S_R = u_R + c_R * (1 + 0.5 * (h_star - h_R) / h_R)
    else:
        S_R = u_R + np.sqrt(g * h_R) * np.sqrt(0.5 * (h_star + h_R) / h_R)

    u_star = 0.5 * (u_L + u_R) + 0.5 * (c_L - c_R) + 0.5 * (
        2 * c_L * (1 - np.sqrt(h_star / h_L))
        - 2 * c_R * (1 - np.sqrt(h_star / h_R))
    )

    return {
        "S_L": S_L,
        "S_R": S_R,
        "S_star": u_star,
        "h_star": h_star,
        "u_star": u_star,
        "type": "wet_general",
    }


def hll_flux(
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float,
) -> NDArray[np.float64]:
    h_L, hu_L = U_L
    h_R, hu_R = U_R

    u_L = hu_L / h_L if h_L > EPS_H else 0.0
    u_R = hu_R / h_R if h_R > EPS_H else 0.0

    c_L = np.sqrt(g * max(h_L, EPS_H))
    c_R = np.sqrt(g * max(h_R, EPS_H))

    S_L = min(u_L - c_L, u_R - c_R)
    S_R = max(u_L + c_L, u_R + c_R)

    F_L = np.array([hu_L, hu_L * u_L + 0.5 * g * h_L * h_L], dtype=np.float64)
    F_R = np.array([hu_R, hu_R * u_R + 0.5 * g * h_R * h_R], dtype=np.float64)

    if S_L >= 0:
        return F_L
    elif S_R <= 0:
        return F_R
    else:
        result = np.array(
            (S_R * F_L - S_L * F_R + S_L * S_R * (U_R - U_L)) / (S_R - S_L),
            dtype=np.float64,
        )
        return result


def evaluate_riemann_solution(
    solution: Dict[str, float],
    x: NDArray[np.float64],
    t: float,
    U_L: NDArray[np.float64],
    U_R: NDArray[np.float64],
    g: float,
) -> NDArray[np.float64]:
    h_L, hu_L = U_L
    h_R, hu_R = U_R
    u_L = hu_L / h_L if h_L > EPS_H else 0.0
    u_R = hu_R / h_R if h_R > EPS_H else 0.0

    S_L = solution["S_L"]
    S_R = solution["S_R"]
    S_star = solution["S_star"]
    h_star = solution["h_star"]
    u_star = solution["u_star"]

    h = np.zeros_like(x)
    u = np.zeros_like(x)

    if t <= 0:
        h = np.where(x < 0, h_L, h_R)
        u = np.where(x < 0, u_L, u_R)
        return np.array([h, h * u], dtype=np.float64)

    xi = x / t

    left_region = xi < S_L
    h[left_region] = h_L
    u[left_region] = u_L

    if solution["type"] == "dry_ritter":
        middle_region = (xi >= S_L) & (xi <= S_star)
        h[middle_region] = (2.0 / (3 * g)) * (
            u_L + np.sqrt(g * h_L) - 0.5 * xi[middle_region]
        ) ** 2
        u[middle_region] = (2.0 / 3.0) * (
            u_L + 2 * np.sqrt(g * h_L) + xi[middle_region]
        )

        right_region = xi > S_star
        h[right_region] = EPS_H
        u[right_region] = 0.0
    else:
        middle_left = (xi >= S_L) & (xi <= S_star)
        if h_star <= h_L:
            c_L = np.sqrt(g * h_L)
            h[middle_left] = h_L * (
                1 - 0.5 * (xi[middle_left] - u_L) / c_L
            ) ** 2
            u[middle_left] = u_L + c_L * (
                1 - np.sqrt(h[middle_left] / h_L)
            )
        else:
            h[middle_left] = h_star
            u[middle_left] = u_star

        middle_right = (xi > S_star) & (xi <= S_R)
        if h_star <= h_R:
            c_R = np.sqrt(g * h_R)
            h[middle_right] = h_R * (
                1 + 0.5 * (xi[middle_right] - u_R) / c_R
            ) ** 2
            u[middle_right] = u_R - c_R * (
                1 - np.sqrt(h[middle_right] / h_R)
            )
        else:
            h[middle_right] = h_star
            u[middle_right] = u_star

        right_region = xi > S_R
        h[right_region] = h_R
        u[right_region] = u_R

    h = np.maximum(h, EPS_H)
    return np.array([h, h * u], dtype=np.float64)
