# Velostat_modeling

Python tools and example measurement data for modelling the force–resistance
behaviour of Velostat-based pressure sensors, including hysteresis (Takač-type
ZORC curves) and the Mullins effect (stress-softening after conditioning cycles).

## Repository structure

```
.
├── Data/
│   └── exemplary_dataset/
│       ├── Series 01.csv
│       ├── Series 02.csv
│       ├── Series 03.csv
│       ├── Series 05.csv
│       ├── Series 10.csv
│       └── Series 17.csv
├── takac_models.py     # Hysteresis (ZORC) curve models and loading/unloading models
└── velostat.py         # Pressure calculation and SI-prefix conversion helpers
```

## Requirements

- Python 3.8+
- NumPy (`takac_models.py`)
- Standard library only for `velostat.py` (`math`)
- Optional for analysis: pandas, matplotlib, SciPy (e.g. `scipy.optimize.curve_fit`)

```bash
pip install numpy pandas matplotlib scipy
```

## Module reference

### `takac_models.py`

Models of hysteresis loops based on the Takač ZORC (zero-offset rate-independent
curve) equations. `x` is the input vector (e.g. force), and all functions are
vectorised with NumPy.

**Helper functions**

| Function | Description |
|---|---|
| `relu_numpy(x)` | Element-wise `max(0, x)`. |
| `x_save(x)` | Clamps values to a minimum of 0.001 (`np.maximum(x, 0.001)`) to avoid division by zero in power-law terms. |

**Basic Takač model (symmetric about (0, 0))**

| Function | Description |
|---|---|
| `takac_b1(xm, a0)` | Offset term `(tanh(xm + a0) − tanh(xm − a0)) / 2` closing the loop at the turning point `xm`. |
| `takac_zorc_ascending(x, a0, A0, xm)` | Ascending (loading) branch: `tanh(x − a0) + A0·x + b1`. |
| `takac_zorc_descending(x, a0, A0, xm)` | Descending (unloading) branch: `tanh(x + a0) + A0·x − b1`. |

**Extended model (loop centre shifted to (x0, y0), amplitude A)**

| Function | Description |
|---|---|
| `takac_zorc_ascending_extended(x, a0, A0, xm, A=1, x0=0, y0=0)` | Ascending branch with amplitude and centre shift. |
| `takac_zorc_descending_extended(x, a0, A0, xm, A=1, x0=0, y0=0)` | Descending branch with amplitude and centre shift. |

**ReLU model (linear slope `A0` applied only on the right side of the loop)**

| Function | Description |
|---|---|
| `takac_zorc_ascending_relu(x, a0, A0, xm, A=1, x0=0, y0=0)` | Ascending branch; linear term uses `relu(x − x0)`. |
| `takac_zorc_descending_relu(x, a0, A0, xm, A=1, x0=0, y0=0)` | Descending branch; linear term uses `relu(x − x0)`. |

**Loading / unloading model for resistance vs. force**

| Function | Description |
|---|---|
| `takac_loading_curve(F, R0, A, F0, w)` | Loading: `R0 + A·tanh((F − F0)/w)`. |
| `takac_unloading_continuous(F, k, p, R_rev, F_rev)` | Unloading: `R_rev + k·(F^−p − F_rev^−p)`, continuous at the reversal point. |

**Parameters**

| Symbol | Meaning |
|---|---|
| `x` | Input vector. |
| `a0` | Hysteresis width. |
| `A0` | Slope of the line outside the hysteresis. |
| `xm` | Turning point on the x-axis. |
| `A` | Hysteresis amplitude (default 1). |
| `x0`, `y0` | Shift of the loop centre along the x and y axes (default 0). |
| `R0` | Vertical offset (centre level) of the loading curve. |
| `F0` | Centre of the loading curve on the force axis. |
| `w` | Width parameter: smaller value gives a steeper transition. |
| `k` | Scale factor of the power-law term; sets the unloading hysteresis amplitude. |
| `p` | Power exponent (degree of nonlinearity of the unloading curve). |
| `R_rev`, `F_rev` | Resistance and force at the reversal (maximum force) point. |

**Utility**

| Function | Description |
|---|---|
| `help_pl()` | Prints a short summary of the available functions and parameters (in Polish). |

### `velostat.py`

| Function | Description |
|---|---|
| `pole_oblicz_cisnienie(pole_mm2, sila_n)` | Pressure (Pa) for a given contact area in mm² and force in N. Raises `ValueError` for zero area. |
| `kolo_r_oblicz_cisnienie(r_mm, sila_n)` | Pressure (Pa) for a circular contact of radius `r_mm`. |
| `kwadrat_oblicz_cisnienie(a_mm, sila_n)` | Pressure (Pa) for a square contact of side `a_mm`. |
| `kolo_oblicz_cisnienie(bok_mm, sila_n)` | Pressure (Pa) for a circle circumscribed on a square of side `bok_mm` (area = πa²/2). |
| `konwertuj_przedrostki(wartosc, z_przedrostka, do_przedrostka)` | Converts a value between SI prefixes (Y … y, e.g. `'k'`, `'M'`, `'m'`, `'u'`, `''`). Raises `ValueError` for unknown prefixes. |

## Example data

`Data/exemplary_dataset/` contains example measurements of **a single sensing
field** from a series of tests on a **heat-laminated Velostat mat**. Each file is
one loading–unloading series: `Series 01`, `02`, `03`, `05`, `10`, `17`.

**The first 10 series are conditioning cycles.** Comparing early series (e.g. 01,
02, 03, 05, 10) with later ones (e.g. 17) lets you observe the **Mullins effect**:
the response in the first loadings differs from that of a stabilised material
(typically a change in resistance level and in the hysteresis loop).

### File format

CSV, semicolon-separated (`;`), decimal comma (`,`).

| Column | Unit | Description |
|---|---|---|
| `Time endur` | s | Absolute time since the test machine was started (does not start at zero for a given series). |
| `Force` | N | Measured force. Includes a small sensor offset at rest (about −0.35 N). |
| `Distance` | mm | Indenter displacement. |
| `Time DAQ` | s | Time from the DAQ card, starting at zero for each series (about 0.1 s sampling). |
| `Current` | A | Measured current. |
| `Voltage` | V | Supply voltage (about 5 V). |
| `Resistance` | Ω | Sensor resistance computed from voltage and current. |

Each series has a rest phase (resistance about 1.1 kΩ), a loading ramp with a
sharp resistance drop, a hold at maximum displacement (about 3.36 mm, about
14 N in `Series 02`, with resistance relaxing towards about 38 Ω), unloading,
and a return to rest.

### Loading the data

```python
import pandas as pd

df = pd.read_csv("Data/exemplary_dataset/Series 02.csv", sep=";", decimal=",")
print(df.head())
```

## Usage examples

**Fit a loading curve**

```python
import numpy as np
from scipy.optimize import curve_fit
from takac_models import takac_loading_curve

# F, R: force and resistance arrays from the loading phase
popt, _ = curve_fit(takac_loading_curve, F, R, p0=[R.mean(), R.std(), F.mean(), 1.0])
R_fit = takac_loading_curve(F, *popt)
```

**Hysteresis loop**

```python
import numpy as np
from takac_models import takac_zorc_ascending, takac_zorc_descending

x = np.linspace(-3, 3, 200)
y_up = takac_zorc_ascending(x, a0=0.5, A0=0.1, xm=3)
y_down = takac_zorc_descending(x, a0=0.5, A0=0.1, xm=3)
```

**Pressure and unit conversion**

```python
from velostat import kwadrat_oblicz_cisnienie, konwertuj_przedrostki

p_pa = kwadrat_oblicz_cisnienie(a_mm=10, sila_n=14)    # Pa
p_kpa = konwertuj_przedrostki(p_pa, "", "k")           # kPa
```

## Mullins effect analysis (suggested workflow)

1. Load the series files and select the loading phase (rising `Distance`).
2. Plot `Resistance` vs. `Force` (or vs. pressure) for each series on one chart.
3. Compare series 01–10 (conditioning) with later series (e.g. 17).
4. Quantify the change: resistance at fixed force, loop width, relaxation during the hold.
5. Fit `takac_loading_curve` / `takac_unloading_continuous` per series and track how the parameters evolve.

## Citation

If you use this code or data, please cite the related publication (to be added).

## License

To be added.
