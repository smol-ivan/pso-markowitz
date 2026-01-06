import os
from pathlib import Path

import numpy as np


def load_data(
    filename,
):
    try:
        with open(filename, "r") as f:
            line = f.readline()
            if not line:
                raise ValueError("File is empty")
            n_assets = int(line.strip())

            assets_data = []
            for _ in range(n_assets):
                assets_data.append(list(map(float, f.readline().split())))

            assets = np.array(assets_data)
            mean_return = assets[:, 0]
            std_devs = assets[:, 1]

            corr_matrix = np.eye(n_assets)
            for line in f:
                parts = line.split()
                if not parts:
                    break
                i, j, val = int(parts[0]), int(parts[1]), float(parts[2])
                corr_matrix[i - 1, j - 1] = val
                corr_matrix[j - 1, i - 1] = val

        return mean_return, std_devs, corr_matrix
    except FileNotFoundError:
        print(f"[ERROR]: The file {filename} is nowhere to be found")
        raise
    except Exception as e:
        print(f"[ERROR]: We dont know whats happening: {e}.")
        raise


def get_limits_return_target(mean_return):
    minimum = mean_return.min()
    maximum = mean_return.max()
    print(f"L_INF={minimum}")
    print(f"L_SUP={maximum}")


def get_limits_risk_target(std_devs):
    minimum = std_devs.min()
    maximum = std_devs.max()
    print(f"L_INF={minimum}")
    print(f"L_SUP={maximum}")


def save_result_csv(mode, data_file, target_value, risk, portfolio_return):
    """
    Save optimization result to CSV file in results/ folder.
    Filename format: {min/max}_{return/risk}_{portfolio_number}.csv
    """
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Extract portfolio number from filename (e.g., "port1.txt" -> "1")
    portfolio_num = Path(data_file).stem.replace("port", "")
    
    # Determine prefix based on mode
    if mode == "minimize_risk":
        prefix = "min_return"
    else:  # maximize_return
        prefix = "max_risk"
    
    # Create filename
    filename = results_dir / f"{prefix}_p{portfolio_num}.csv"
    
    # Check if file exists to decide on header
    file_exists = filename.exists()
    
    # Write or append to CSV
    with open(filename, "a") as f:
        if not file_exists:
            f.write("target_value,risk,return\n")
        f.write(f"{target_value},{risk},{portfolio_return}\n")
