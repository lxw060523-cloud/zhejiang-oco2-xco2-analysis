"""
Extract and quality-filter OCO-2 XCO2 observations over Zhejiang Province
from NASA OCO2_L2_Lite_FP (v11.1r) NetCDF4 (.nc4) files and export to CSV chunks.
"""

import os
import xarray as xr
import pandas as pd
from tqdm import tqdm


def extract_zhejiang_xco2(
    input_folder: str = os.path.join(".", "data", "raw_nc4"),
    output_folder: str = os.path.join(".", "data", "csv_chunks"),
    min_lat: float = 27.15,
    max_lat: float = 31.00,
    min_lon: float = 118.01,
    max_lon: float = 123.00,
    chunk_size: int = 1_000_000,
) -> None:
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.isdir(input_folder):
        raise FileNotFoundError(f"Input directory not found: {input_folder}")

    files = sorted(f for f in os.listdir(input_folder) if f.endswith(".nc4"))
    print(f"Detected {len(files)} NetCDF4 (.nc4) files. Starting extraction...")

    chunk_index = 1
    files_written = 0
    row_buffer = []

    for filename in tqdm(files, desc="Processing .nc4 files"):
        file_path = os.path.join(input_folder, filename)
        try:
            with xr.open_dataset(file_path) as ds:
                lat = ds["latitude"].values
                lon = ds["longitude"].values
                xco2 = ds["xco2"].values
                time = ds["time"].values

                # Spatial bounding box for Zhejiang Province
                mask = (
                    (lat >= min_lat)
                    & (lat <= max_lat)
                    & (lon >= min_lon)
                    & (lon <= max_lon)
                )

                # Standard OCO-2 quality filtering (aligned with manuscript workflow)
                if "xco2_quality_flag" in ds:
                    mask &= ds["xco2_quality_flag"].values == 0
                if "warn_level" in ds:
                    mask &= ds["warn_level"].values < 15

                if mask.sum() == 0:
                    continue

                filtered_rows = list(
                    zip(time[mask], lat[mask], lon[mask], xco2[mask])
                )
                row_buffer.extend(filtered_rows)

                # Export in chunks to manage memory usage
                while len(row_buffer) >= chunk_size:
                    df = pd.DataFrame(
                        row_buffer[:chunk_size],
                        columns=["time", "latitude", "longitude", "xco2"],
                    )
                    df["time"] = pd.to_datetime(
                        df["time"], errors="coerce"
                    ).dt.strftime("%Y-%m-%d %H:%M:%S")
                    output_path = os.path.join(
                        output_folder, f"oco2_zhejiang_part_{chunk_index}.csv"
                    )
                    df.to_csv(output_path, index=False, encoding="utf-8-sig")
                    chunk_index += 1
                    files_written += 1
                    row_buffer = row_buffer[chunk_size:]
        except Exception as exc:
            print(f"Failed to process {filename}: {exc}")

    # Export remaining buffered records
    if row_buffer:
        df = pd.DataFrame(
            row_buffer, columns=["time", "latitude", "longitude", "xco2"]
        )
        df["time"] = pd.to_datetime(df["time"], errors="coerce").dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        output_path = os.path.join(
            output_folder, f"oco2_zhejiang_part_{chunk_index}.csv"
        )
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        files_written += 1

    print(
        f"Extraction complete. Generated {files_written} CSV file(s) in {output_folder}."
    )


if __name__ == "__main__":
    extract_zhejiang_xco2()
