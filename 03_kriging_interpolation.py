"""
Perform Ordinary Kriging spatial interpolation on extracted OCO-2 XCO2 CSV data
and export a contour map with original sounding locations.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging


def run_kriging_interpolation(
    csv_file: str = os.path.join(".", "data", "csv_chunks", "oco2_zhejiang_part_1.csv"),
    output_png: str = os.path.join(".", "outputs", "kriging_xco2_map.png"),
    grid_resolution: int = 200,
    variogram_model: str = "spherical",
) -> None:
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"Input CSV file not found: {csv_file}")

    os.makedirs(os.path.dirname(output_png), exist_ok=True)

    # 1. Load extracted XCO2 CSV data
    data = pd.read_csv(csv_file)
    print("Loaded CSV columns:", list(data.columns))

    required_cols = {"longitude", "latitude", "xco2"}
    if not required_cols.issubset(data.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    lon = data["longitude"].values
    lat = data["latitude"].values
    xco2 = data["xco2"].values

    # 2. Construct interpolation grid
    grid_lon_1d = np.linspace(np.min(lon), np.max(lon), grid_resolution)
    grid_lat_1d = np.linspace(np.min(lat), np.max(lat), grid_resolution)
    grid_lon, grid_lat = np.meshgrid(grid_lon_1d, grid_lat_1d)

    # 3. Execute Ordinary Kriging
    # variogram_model can be set to "spherical", "gaussian", or "exponential"
    ok = OrdinaryKriging(
        lon,
        lat,
        xco2,
        variogram_model=variogram_model,
        verbose=False,
        enable_plotting=False,
    )
    z, ss = ok.execute("grid", grid_lon_1d, grid_lat_1d)

    # 4. Plot interpolated XCO2 surface and sounding locations
    plt.figure(figsize=(8, 6))
    levels = np.linspace(390, 440, 21)
    contour = plt.contourf(
        grid_lon,
        grid_lat,
        z,
        levels=levels,
        cmap="jet",
        extend="both",
    )

    plt.scatter(
        lon,
        lat,
        c=xco2,
        edgecolor="k",
        s=20,
        cmap="jet",
        vmin=390,
        vmax=440,
    )

    plt.colorbar(contour, label="XCO2 (ppm)")
    plt.title("Ordinary Kriging Interpolation of OCO-2 XCO2")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()

    # 5. Save figure
    plt.savefig(output_png, dpi=300)
    plt.close()
    print(f"Interpolation map saved to {output_png}")


if __name__ == "__main__":
    run_kriging_interpolation()
