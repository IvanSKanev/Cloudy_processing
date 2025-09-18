import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_ew_contours_general(file_path,
                             Nx,                     # number of x-points
                             Ny,                     # number of y-points
                             x_min,                  # minimum of x-linspace
                             x_max,                  # maximum of x-linspace
                             y_min,                  # minimum of y-linspace
                             y_max,                  # maximum of y-linspace,
                             ref_col="Inci 1215.00A ",
                             log_levels=(0, 3),
                             n_levels=12):
    """
    A function for plotting EW contours and saving each plot in EW_plots/.
    """

    # ------------------------------------------------
    # 0) Resolve save directory next to this script
    # ------------------------------------------------
    try:
        base_dir = Path(__file__).resolve().parent
    except NameError:
        # Fallback (e.g., if run in a notebook)
        base_dir = Path.cwd()
    save_dir = base_dir / "EW_plots"
    save_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------
    # 1) Read data
    # ------------------------------------------------
    df = pd.read_csv(file_path, sep="\t", encoding="ISO-8859-1", engine="python")
    total_rows = len(df)

    # Sanity check that Nx * Ny == total_rows
    if Nx * Ny != total_rows:
        raise ValueError(
            f"Specified Nx * Ny = {Nx * Ny}, but your file has {total_rows} rows. "
            "They must match."
        )

    # ------------------------------------------------
    # 2) Verify the reference flux column
    # ------------------------------------------------
    if ref_col not in df.columns:
        raise ValueError(f"Error: '{ref_col}' column not found in dataset.")

    # Convert reference flux to numeric array
    H1_1215_flux = pd.to_numeric(df[ref_col], errors="coerce").values

    # ------------------------------------------------
    # 3) Construct x, y arrays
    # ------------------------------------------------
    x = np.linspace(x_min, x_max, Nx)
    y = np.linspace(y_min, y_max, Ny)

    # ------------------------------------------------
    # 4) Loop over columns and plot
    # ------------------------------------------------
    for col_name in df.columns:
        # Skip reference column and line-list column
        if col_name == ref_col or col_name == "#lineslist":
            continue

        # Convert flux to numeric
        flux_vals = pd.to_numeric(df[col_name], errors="coerce").values

        # Ensure emission line values ≥ 1 BEFORE normalization
        flux_vals = np.where(np.isnan(flux_vals), 1, flux_vals)
        flux_vals[flux_vals < 1] = 1

        # Normalize line flux by reference flux
        # (avoid div-by-zero by flooring ref flux at 1 as well)
        H_safe = np.where(np.isnan(H1_1215_flux) | (H1_1215_flux < 1), 1, H1_1215_flux)
        flux_normalized = flux_vals / H_safe

        # Log-transform
        log_flux = np.log10(flux_normalized * 1215.0)

        # Reshape to Nx-by-Ny
        Z = log_flux.reshape(Nx, Ny)

        # Transpose so Z[i, j] -> x[i], y[j]
        rotZ = Z.T

        # Make contour levels
        levels = np.linspace(log_levels[0], log_levels[1], n_levels)

        # Plot contour
        plt.figure(figsize=(8, 6))
        CS = plt.contour(x, y, rotZ, levels=levels, cmap="copper")
        plt.clabel(CS, inline=True, fontsize=10)
        plt.xlabel(r"log $n_{H}$")
        plt.ylabel(r"log $\Phi_{H}$")
        plt.title(col_name)
        plt.grid(True)

        # ---------- Save each plot ----------
        safe_name = re.sub(r'[^-\w().\s]', '_', str(col_name)).strip().replace(' ', '_')
        out_path = save_dir / f"{safe_name}.png"
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()
