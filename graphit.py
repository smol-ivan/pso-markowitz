import os
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.figsize": (7, 5),
            "font.size": 12,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )

    input_dir = Path("./results/")
    output_dir = "./graficas"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for res_file in input_dir.iterdir():
        # full_path = os.path.join(result_dir, resultado)
        df = pd.read_csv(res_file)
        graph_generator(df, res_file.name, output_dir)


def graph_generator(df, file_name, output_dir):
    fig, ax = plt.subplots()

    sns.scatterplot(data=df, x="risk", y="return", ax=ax, color="teal", s=60)

    ax.set_title("Frontera eficiente", pad=15)
    ax.set_xlabel(r"Risk ($\sigma$)")
    ax.set_ylabel(r"Expected Return ($E[r]$)")

    save_path = os.path.join(output_dir, f"{file_name}.pdf")
    plt.savefig(save_path)
    plt.close()


if __name__ == "__main__":
    main()
