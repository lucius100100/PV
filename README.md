# Perovskite solar data analysis

A Python analysis script for loading, cleaning, and plotting time-series data from Perovskite solar panel test runs (IMEC1).

## Directory structure

```text
.
├── Data/                                   # Folder containing raw CSV files
│   ├── 2025_09_04...CURVES_INCLUDED.csv    # September dataset
│   ├── 2025_10_11...CURVES_INCLUDED.csv    # Oct/Nov dataset
│   └── 2025_12_Dec...CURVES_INCLUDED.csv   # December dataset
├── PV.py                                   # Main processing and plotting script
└── README.md

```

## Requirements

- Python 3.10+
- pandas
- matplotlib

## Features
- Dynamic Loading: Automatically detects file paths relative to the script location.
- Robust Parsing: Handles metadata headers, BOM encoding (utf-8-sig), and blank lines automatically.
- Data Cleaning: Concatenates disjointed datasets into a single continuous time-series.
- Visualization: Generates stacked subplots for all numeric variables (Irradiance, Voltage, Temperature, etc.), sharing the same time axis.
