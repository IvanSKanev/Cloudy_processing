#!/usr/bin/env python3
"""
make_all_plots.py

A small runner script that imports your three plotting functions and calls them.
- plot_ew_contours_general(...) from EW_Contour_plotting.py
- inci_plot() from inci_trans_plotting.py
- trans_plot() from inci_trans_plotting.py

Usage examples:

1) Call everything with explicit arguments for the EW contour plot:
   python make_all_plots.py \
     --file-path ./your_emission_lines.tsv \
     --Nx 41 --Ny 41 \
     --x-min 7 --x-max 14 \
     --y-min 17 --y-max 24 \
     --ref-col "Inci 1215.00A " \
     --log-min 0 --log-max 3 --n-levels 12

2) If you just want to run inci_plot and trans_plot (and skip the contours), omit --file-path:
   python make_all_plots.py

Notes:
- This script only *wraps* your existing functions; it does not change how they work.
- For plot_ew_contours_general, you must provide the required parameters. The script
  exposes them as CLI options so you don't need to edit code each time.
"""

import argparse
import sys
from pathlib import Path

# Import your functions
try:
    from EW_Contour_plotting import plot_ew_contours_general
except Exception as e:
    print("Could not import plot_ew_contours_general from EW_Contour_plotting.py:", e, file=sys.stderr)
    plot_ew_contours_general = None

try:
    from inci_trans_plotting import inci_plot, trans_plot
except Exception as e:  
    print("Could not import inci_plot/trans_plot from inci_trans_plotting.py:", e, file=sys.stderr)
    inci_plot = None
    trans_plot = None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run all plotting routines.")
    parser.add_argument("--file-path", type=str, default=None,
                        help="Path to the EW/emission lines data file (tab-separated). If omitted, the EW contour plot is skipped.")
    parser.add_argument("--Nx", type=int, help="Number of x-points.", default=None)
    parser.add_argument("--Ny", type=int, help="Number of y-points.", default=None)
    parser.add_argument("--x-min", type=float, help="Minimum x value for grid.", default=None)
    parser.add_argument("--x-max", type=float, help="Maximum x value for grid.", default=None)
    parser.add_argument("--y-min", type=float, help="Minimum y value for grid.", default=None)
    parser.add_argument("--y-max", type=float, help="Maximum y value for grid.", default=None)
    parser.add_argument("--ref-col", type=str, default="Inci 1215.00A ",
                        help='Reference column name used for normalization, default: "Inci 1215.00A "')
    parser.add_argument("--log-min", type=float, default=0.0, help="Minimum log level for contours (default: 0).")
    parser.add_argument("--log-max", type=float, default=3.0, help="Maximum log level for contours (default: 3).")
    parser.add_argument("--n-levels", type=int, default=12, help="Number of contour levels (default: 12).")
    parser.add_argument("--skip-inci", action="store_true", help="Skip inci_plot() call.")
    parser.add_argument("--skip-trans", action="store_true", help="Skip trans_plot() call.")

    args = parser.parse_args(argv)

    # 1) EW Contours (optional if file-path provided)
    if args.file_path is not None:
        missing = [name for name in ("Nx", "Ny", "x_min", "x_max", "y_min", "y_max")
                   if getattr(args, name.replace("-", "_"), None) is None]
        if missing:
            print(
                "For plot_ew_contours_general, you must supply: --Nx --Ny --x-min --x-max --y-min --y-max.\n"
                f"Missing: {', '.join(missing)}",
                file=sys.stderr,
            )
        elif plot_ew_contours_general is None:
            print("plot_ew_contours_general is unavailable (import failed).", file=sys.stderr)
        else:
            # Call the contour plot function
            try:
                plot_ew_contours_general(
                    file_path=args.file_path,
                    Nx=args.Nx,
                    Ny=args.Ny,
                    x_min=args.x_min,
                    x_max=args.x_max,
                    y_min=args.y_min,
                    y_max=args.y_max,
                    ref_col=args.ref_col,
                    log_levels=(args.log_min, args.log_max),
                    n_levels=args.n_levels,
                )
            except Exception as e:
                print("Error while running plot_ew_contours_general:", e, file=sys.stderr)

    # 2) inci_plot
    if not args.skip_inci:
        if inci_plot is None:
            print("inci_plot is unavailable (import failed).", file=sys.stderr)
        else:
            try:
                inci_plot()
            except Exception as e:
                print("Error while running inci_plot():", e, file=sys.stderr)

    # 3) trans_plot
    if not args.skip_trans:
        if trans_plot is None:
            print("trans_plot is unavailable (import failed).", file=sys.stderr)
        else:
            try:
                trans_plot()
            except Exception as e:
                print("Error while running trans_plot():", e, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




# Input command for running the script, with included trans and inci spectra:
# python make_all_plots.py \  
# --file-path emission_lines_1hden_2phi.txt \  
# --Nx 29 --Ny 29 \          
#  --x-min 7.0 --x-max 14.0 \
#  --y-min 17.0 --y-max 24.0 \
#  --ref-col "Inci 1215.00A " \
#  --log-min 0 --log-max 3 --n-levels 12


# Input command for running the script, without trans and inci spectra:
# python make_all_plots.py \  
# --file-path emission_lines_1hden_2phi.txt \  
# --Nx 29 --Ny 29 \          
#  --x-min 7.0 --x-max 14.0 \
#  --y-min 17.0 --y-max 24.0 \
#  --ref-col "Inci 1215.00A " \
#  --log-min 0 --log-max 3 --n-levels 12
# --skip-inci --skip-trans