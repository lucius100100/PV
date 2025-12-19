import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def load_pv_data(filename, folder_name='Data'):
    """Load PV data."""

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    
    file_path = os.path.join(script_dir, folder_name, filename)
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    #dynamic header row
    header_row_index = None
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for i, line in enumerate(f):
                if line.strip().lower().startswith('timestamp'):
                    header_row_index = i
                    break
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            for i, line in enumerate(f):
                if line.strip().lower().startswith('timestamp'):
                    header_row_index = i
                    break

    if header_row_index is None:
        print(f"Error: Header missing in {filename}")
        return None
    
    try:
        #skip_blank_lines=False to match line counts
        df = pd.read_csv(file_path, header=header_row_index, skip_blank_lines=False, encoding='utf-8-sig')
        
        df.columns = df.columns.str.strip()
        
        #timestamp
        col_map = {c.lower(): c for c in df.columns}
        if 'timestamp' in col_map:
            df.rename(columns={col_map['timestamp']: 'timestamp'}, inplace=True)
        
        #empty rows and rows where timestamp is invalid
        df.dropna(how='all', inplace=True)
        df = df[df['timestamp'].notna()]

        #DateTime
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y %H:%M:%S')
        df = df.set_index('timestamp')
        df = df.sort_index()
        
        print(f"Loaded: {filename} ({len(df)} rows)")
        return df
        
    except Exception as e:
        print(f"Failed to load {filename}: {e}")
        return None

file_names = [
    "2025_09_04_to_2025_09_30-PVBlocks-IMEC1-CURVES_INCLUDED.csv",
    "2025_10_11_Oct_Nov_IMEC1-CURVES_INCLUDED (1).csv",
    "2025_12_Dec-PVBlocks-IMEC1-CURVES_INCLUDED.csv"
]

dataframes = []

for fname in file_names:
    df = load_pv_data(fname)
    if df is not None:
        dataframes.append(df)

if dataframes:
    #concatanate
    full_df = pd.concat(dataframes)
    full_df = full_df.sort_index()
    
    #columns
    all_cols = full_df.columns
    cols_to_plot = []
    
    print("Processing columns for plotting...")
    
    for col in all_cols:
        if 'Currents' in col or 'Voltages' in col:
            continue
            
        #convert column to numeric, forcing errors to NaN
        full_df[col] = pd.to_numeric(full_df[col], errors='coerce')

        if full_df[col].notna().any():
            cols_to_plot.append(col)

    #subplot length based on amount of variables
    num_plots = len(cols_to_plot)
    
    #plotting
    if num_plots > 0:

        fig, axes = plt.subplots(nrows=num_plots, ncols=1, figsize=(12, 2 * num_plots), sharex=True)
        
        if num_plots == 1:
            axes = [axes]
        
        for ax, col_name in zip(axes, cols_to_plot):

            ax.plot(full_df.index, full_df[col_name], label=col_name, marker='.', markersize=2, linestyle='-', linewidth=0.5)
            
            ax.set_ylim(full_df[col_name].min() - 0.05 * (full_df[col_name].max() - full_df[col_name].min()), full_df[col_name].max() + 0.05 * (full_df[col_name].max() - full_df[col_name].min()))
            ax.legend(loc='upper right', fontsize='small')
            ax.grid(True)

        axes[0].set_xlim(full_df.index.min(), full_df.index.max())
        axes[-1].set_xlabel('Date')
        plt.suptitle(f'PV data overview ({full_df.index.min().date()} to {full_df.index.max().date()})', y=1.005)
        
        plt.tight_layout()
        plt.savefig('data_overview.png')
        plt.show()
    else:
        print("No numeric data columns found to plot.")

else:
    print("No data loaded.")