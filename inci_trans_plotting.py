# Importing all libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
from pathlib import Path

# ------------------------------------------------
# Create save directory
# ------------------------------------------------
try:
    base_dir = Path(__file__).resolve().parent  # directory of script
except NameError:
    base_dir = Path.cwd()  # fallback if run in interactive
save_dir = base_dir / "Incident&Transmitted_spectrum"
save_dir.mkdir(parents=True, exist_ok=True)


# Defining the function to plot the transmitted continuum spectrum
def trans_plot():
    # Load data
    cont_file = np.loadtxt('continuum.cont', usecols=(0, 1, 2))
    nu = cont_file[:, 0]
    transmitted = cont_file[:, 2]

    # Apply conditions: photon energy > 1 and transmitted > 1
    mask = (nu > 1) & (transmitted > 1)
    filtered_nu = nu[mask]
    filtered_trans = transmitted[mask]

    # Take log of the filtered transmitted values
    trans_log = np.log10(filtered_trans)

    # Plot
    plt.figure(figsize=(12, 6))
    trans_line, = plt.plot(filtered_nu, trans_log, '.', label='Transmitted SED', color='blue')

    plt.xlabel('Photon energy [eV]', fontsize=20)
    plt.ylabel(r'log ($\nu F_\nu$)', fontsize=20)

    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xscale('log')

    # Define spectrum regions (for shading and legend)
    regions = [
        {'xmin': 0.9, 'xmax': 3, 'label': 'Visible', 'color': 'green'},
        {'xmin': 3, 'xmax': 100, 'label': 'Ultraviolet', 'color': 'blue'},
        {'xmin': 100, 'xmax': 1e4, 'label': 'X-rays', 'color': 'purple'},
        {'xmin': 1e4, 'xmax': 2*10**8, 'label': 'Gamma rays', 'color': 'violet'}
    ]

    # Add shaded regions
    for region in regions:
        plt.axvspan(region['xmin'], region['xmax'], color=region['color'], alpha=0.3)

    # Custom legend
    legend_patches = [mpatches.Patch(color=region['color'], label=region['label']) for region in regions]
    combined_legend = legend_patches + [trans_line]
    plt.legend(handles=combined_legend, loc='upper right', fontsize=19, frameon=True, edgecolor='black')

    # Ticks
    plt.tick_params(axis='both', which='major', length=10, width=2.5, labelsize=18)
    plt.tick_params(axis='both', which='minor', length=5, width=2)

    plt.xlim(0.9, 2 * 10**8)

    plt.tight_layout()
    out_file = save_dir / "transmitted_continuum_spectrum.png"
    plt.savefig(out_file, format="png", dpi=300)
    plt.show()


# Defining the function to plot the incident continuum spectrum
def inci_plot():
    # Load data
    cont_file = np.loadtxt('continuum.cont', usecols=(0, 1, 2))
    nu = cont_file[:, 0]
    incident = cont_file[:, 1]

    # Apply conditions: photon energy > 1 and incident > 1
    mask = (nu > 1) & (incident > 1)
    filtered_nu = nu[mask]
    filtered_trans = incident[mask]

    # Take log of the filtered incident values
    trans_log = np.log10(filtered_trans)

    # Plot
    plt.figure(figsize=(12, 6))
    trans_line, = plt.plot(filtered_nu, trans_log, '.', label='Incident SED', color='blue')

    plt.xlabel('Photon energy [eV]', fontsize=20)
    plt.ylabel(r'log ($\nu F_\nu$)', fontsize=20)

    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.xscale('log')

    # Define spectrum regions
    regions = [
        {'xmin': 0.9, 'xmax': 3, 'label': 'Visible', 'color': 'green'},
        {'xmin': 3, 'xmax': 100, 'label': 'Ultraviolet', 'color': 'blue'},
        {'xmin': 100, 'xmax': 1e4, 'label': 'X-rays', 'color': 'purple'},
        {'xmin': 1e4, 'xmax': 2*10**8, 'label': 'Gamma rays', 'color': 'violet'}
    ]

    # Add shaded regions
    for region in regions:
        plt.axvspan(region['xmin'], region['xmax'], color=region['color'], alpha=0.3)

    # Custom legend
    legend_patches = [mpatches.Patch(color=region['color'], label=region['label']) for region in regions]
    combined_legend = legend_patches + [trans_line]
    plt.legend(handles=combined_legend, loc='upper right', fontsize=19, frameon=True, edgecolor='black')

    # Ticks
    plt.tick_params(axis='both', which='major', length=10, width=2.5, labelsize=18)
    plt.tick_params(axis='both', which='minor', length=5, width=2)

    plt.xlim(0.9, 2 * 10**8)

    plt.tight_layout()
    out_file = save_dir / "incident_continuum_spectrum.png"
    plt.savefig(out_file, format="png", dpi=300)
    plt.show()
