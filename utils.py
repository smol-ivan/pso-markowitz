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
