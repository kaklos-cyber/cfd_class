# Frontend Public API Documentation

This document describes the public API layer designed for frontend consumption.

---

## 1. Schemes Package (`src.core.schemes`)

### Factory Function

#### `get_scheme(name: str, **kwargs) -> BaseScheme`

Create a scheme instance by string name.

**Supported names:**
| Name | Class | Order |
|------|-------|-------|
| `"First-Order Upwind"` / `"Upwind"` | `UpwindScheme` | 1st |
| `"Lax-Friedrichs"` | `LaxFriedrichsScheme` | 1st |
| `"HLL"` | `HLLScheme` | 1st |
| `"Lax-Wendroff"` | `LaxWendroffScheme` | 2nd |
| `"MacCormack"` | `MacCormackScheme` | 2nd |
| `"Beam-Warming"` | `BeamWarmingScheme` | 2nd |
| `"Fromm"` | `FrommScheme` | 2nd |
| `"Godunov"` | `GodunovScheme` | 1st |
| `"MUSCL-Hancock"` / `"MUSCL"` | `MUSCLScheme` | 2nd |

**Examples:**
```python
from src.core.schemes import get_scheme

# Basic usage
scheme = get_scheme("HLL")

# With parameters
scheme = get_scheme("MUSCL-Hancock", limiter="superbee")
scheme = get_scheme("Godunov", g=9.8)
```

#### `list_schemes() -> list[str]`

Return all available scheme names.

```python
from src.core.schemes import list_schemes

names = list_schemes()
# ['Beam-Warming', 'First-Order Upwind', 'Fromm', 'Godunov', 'HLL',
#  'Lax-Friedrichs', 'Lax-Wendroff', 'MacCormack', 'MUSCL', 'MUSCL-Hancock',
#  'Upwind']
```

### Aliases (without "Scheme" suffix)

```python
from src.core.schemes import HLL, Godunov, MUSCLHancock

scheme = HLL()           # same as HLLScheme()
scheme = Godunov()       # same as GodunovScheme()
scheme = MUSCLHancock()  # same as MUSCLScheme()
```

### BaseScheme.evolve() Method

#### `scheme.evolve(config: DamBreakConfig) -> dict[float, np.ndarray]`

Run simulation and return frontend-friendly output.

**Returns:**
- Dictionary mapping `time_float` → `np.ndarray` of shape `(2, nx)`
- `array[0]` = water depth `h`
- `array[1]` = velocity `u`

**Example:**
```python
from src.core.config import DamBreakConfig
from src.core.schemes import HLL

config = DamBreakConfig(nx=100, t_end=10.0)
scheme = HLL()
result = scheme.evolve(config)

for t, data in result.items():
    h = data[0]  # shape (nx,)
    u = data[1]  # shape (nx,)
```

---

## 2. Solvers Package (`src.core.solvers`)

### ExactRiemann Adapter

#### `ExactRiemann(config: DamBreakConfig)`

Frontend-friendly wrapper for the exact Riemann solver.

**Methods:**

##### `solve(config: DamBreakConfig) -> np.ndarray`

Solve and return result as `(2, nx)` array.

```python
from src.core.config import DamBreakConfig
from src.core.solvers import ExactRiemann

config = DamBreakConfig(nx=100, t_end=10.0)
solver = ExactRiemann(config)
exact = solver.solve(config)  # shape (2, nx)
h = exact[0]
u = exact[1]
```

##### `solve_at_time(t: float) -> np.ndarray`

Solve at a specific time using the stored config.

```python
exact_t5 = solver.solve_at_time(t=5.0)  # shape (2, nx)
```

---

## 3. Config Package (`src.core.config`)

### DamBreakConfig

```python
from src.core.config import DamBreakConfig

config = DamBreakConfig(
    h_l=10.0,           # Left water depth [m]
    h_r=1.0,            # Right water depth [m]
    u_l=0.0,            # Left velocity [m/s]
    u_r=0.0,            # Right velocity [m/s]
    g=9.81,             # Gravity [m/s^2]
    cfl=0.9,            # CFL number (0, 1]
    nx=100,             # Number of grid cells (>= 2)
    t_end=50.0,         # End time [s]
    x_dam=500.0,        # Dam position [m]
    domain_length=1000.0,  # Domain length [m]
    boundary_type="transmissive",  # "transmissive" | "reflective" | "periodic"
)
```

**Properties:**
- `config.dx` → Grid spacing [m]
- `config.x` → Cell center coordinates, shape `(nx,)`
- `config.eps_h` → Minimum water depth tolerance

**Methods:**
- `config.initial_condition()` → `(h, u)` arrays at t=0
- `config.to_dict()` → Dictionary representation
- `config.to_json()` → JSON string
- `DamBreakConfig.from_dict(data)` → Create from dict
- `DamBreakConfig.from_json(json_str)` → Create from JSON

---

## 4. Complete Usage Example

```python
import numpy as np
from src.core.config import DamBreakConfig
from src.core.schemes import get_scheme
from src.core.solvers import ExactRiemann

# 1. Create configuration
config = DamBreakConfig(
    h_l=10.0,
    h_r=1.0,
    nx=200,
    t_end=20.0,
    cfl=0.9,
)

# 2. Run numerical simulation
scheme = get_scheme("MUSCL-Hancock", limiter="minmod")
num_result = scheme.evolve(config)

# 3. Get exact solution for comparison
exact_solver = ExactRiemann(config)
exact_solution = exact_solver.solve(config)

# 4. Compare at final time
t_final = config.t_end
num_final = num_result[t_final]  # shape (2, nx)
exact_final = exact_solution      # shape (2, nx)

h_error = np.abs(num_final[0] - exact_final[0])
print(f"Max water depth error: {np.max(h_error):.4f} m")
```

---

## 5. Import Summary

```python
# Schemes
from src.core.schemes import (
    get_scheme, list_schemes,           # Factory functions
    BaseScheme, SimulationResult,        # Base classes
    UpwindScheme, LaxFriedrichsScheme,   # Class names
    HLLScheme, GodunovScheme,
    LaxWendroffScheme, MacCormackScheme,
    BeamWarmingScheme, FrommScheme,
    MUSCLScheme,
    Upwind, HLL, Godunov, MUSCLHancock,  # Aliases
)

# Solvers
from src.core.solvers import (
    ExactRiemannSolver,  # Low-level exact solver
    HLLSolver,           # Low-level HLL solver
    ExactRiemann,        # Frontend adapter
)

# Config
from src.core.config import DamBreakConfig
```
