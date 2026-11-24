# OCO-2 XCO2 Processing and Ordinary Kriging Scripts (Zhejiang Province, 2019–2023)

This repository contains the core data acquisition, regional extraction, and Ordinary Kriging spatial interpolation scripts supporting the manuscript:

> **Assessing Regional Carbon–Economic Sustainability: Spatiotemporal Evolution of XCO2 Linked to Economic Development in China’s Zhejiang Province Based on OCO-2 Data**

## Repository Structure

```text
.
├── 01_download_oco2.bat           # Windows batch script for downloading NASA OCO-2 .nc4 files via wget
├── 02_extract_zhejiang_xco2.py    # Extracts quality-filtered XCO2 soundings over Zhejiang Province to CSV
├── 03_kriging_interpolation.py    # Performs Ordinary Kriging interpolation and plots XCO2 spatial maps
├── requirements.txt               # Python package dependencies
└── README.md
```

## Data Sources

1. **Satellite XCO2 Data:** NASA Orbiting Carbon Observatory-2 (OCO-2) Level 2 Lite File Product (`OCO2_L2_Lite_FP`, version `11.1r`), publicly available from NASA GES DISC:  
   https://disc.gsfc.nasa.gov/datasets/OCO2_L2_Lite_FP_11.1r/summary
2. **Socioeconomic Data:** County-level Gross Domestic Product (GDP) and Gross Industrial Output Value Above Designated Size (2019–2023) are third-party official statistics publicly available from the *China Statistical Yearbook* and the *Zhejiang Statistical Yearbook*. Administrative boundary adjustments for Linping and Qiantang Districts follow the procedure documented in Section 2.2.2 of the manuscript.

## Prerequisites

- **Python:** Version 3.9 or higher
- **Install Python dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **wget (for Step 1 only):** Required for batch downloading from NASA GES DISC (Windows users can install GNU Wget and add it to the system `PATH`).
- **NASA Earthdata Account:** Required to generate an authenticated `cookie.txt` and download link list (`file_list.txt`) from NASA GES DISC. Do **not** commit your personal `cookie.txt` to any public repository.

## Usage

### Step 1: Download OCO-2 NetCDF4 Files
1. Filter the `OCO2_L2_Lite_FP` (v11.1r) dataset for 2019–2023 on NASA GES DISC and save the download URL list as `file_list.txt` in the repository root.
2. Save your NASA Earthdata session cookies to `cookie.txt` in the repository root.
3. Run the batch script:
   ```cmd
   01_download_oco2.bat
   ```
   Downloaded `.nc4` files will be saved to `./data/raw_nc4/`.

### Step 2: Extract Regional XCO2 Observations
Run the extraction script to filter soundings within Zhejiang Province (`27.15°N–31.00°N`, `118.01°E–123.00°E`) with standard OCO-2 quality filtering (`xco2_quality_flag == 0`, and `warn_level < 15` when present):
```bash
python 02_extract_zhejiang_xco2.py
```
Extracted records are exported as chunked CSV files (`time, latitude, longitude, xco2`) in `./data/csv_chunks/`.

### Step 3: Ordinary Kriging Interpolation and Visualization
Run the interpolation script on a seasonal or annual CSV file (default: `./data/csv_chunks/oco2_zhejiang_part_1.csv`):
```bash
python 03_kriging_interpolation.py
```
The interpolated XCO2 map is saved to `./outputs/kriging_xco2_map.png` (300 DPI). Parameters such as `grid_resolution` and `variogram_model` (`"spherical"`, `"gaussian"`, `"exponential"`) can be adjusted in the script.

## Notes on Workflow Scope
These scripts cover core OCO-2 data acquisition, regional extraction, quality filtering, and Ordinary Kriging interpolation. Subsequent county-level administrative masking, seasonal aggregation into 50 km × 50 km grids, and socioeconomic regression analyses follow the methodology detailed in Section 2.3 of the manuscript.
