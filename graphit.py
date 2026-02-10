import os
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ------------------------------------------------------
# Cargar frontera eficiente analítica (Markowitz)
# ------------------------------------------------------
def load_portef_file(path):
    """
    Lee archivos portef*.txt con formato:
    return   variance
    """
    df = pd.read_csv(path, sep=r"\s+", header=None, names=["return", "variance"])
    df["risk"] = df["variance"] ** 0.5
    return df


# ------------------------------------------------------
# Generación de gráficas comparativas
# ------------------------------------------------------
def graph_generator(df_pso, df_portef, file_name, output_dir):
    fig, ax = plt.subplots()

    # Frontera PSO
    sns.scatterplot(
        data=df_pso, x="risk", y="return", ax=ax, color="teal", s=60, label="PSO"
    )

    # Frontera eficiente analítica
    if df_portef is not None:
        sns.lineplot(
            data=df_portef,
            x="risk",
            y="return",
            ax=ax,
            color="black",
            linestyle="--",
            linewidth=2,
            label="Markowitz (sin restricciones)",
        )

    ax.set_title("Comparación de Fronteras Eficientes", pad=15)
    ax.set_xlabel(r"Risk ($\sigma$)")
    ax.set_ylabel(r"Expected Return ($E[r]$)")
    ax.legend()

    save_path = os.path.join(output_dir, f"{file_name}.pdf")
    plt.savefig(save_path)
    plt.close()


# ------------------------------------------------------
# Main
# ------------------------------------------------------
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

    results_dir = Path("./results/")
    portef_dir = Path("./data/")
    output_dir = "./graficas"

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for res_file in results_dir.iterdir():
        if res_file.suffix != ".csv":
            continue

        # Resultados PSO
        df_pso = pd.read_csv(res_file)

        # Buscar archivo portef correspondiente
        # ejemplo: result_1.csv -> portef1.txt
        idx = "".join(filter(str.isdigit, res_file.stem))
        portef_file = portef_dir / f"portef{idx}.txt"

        df_portef = None
        if portef_file.exists():
            df_portef = load_portef_file(portef_file)

        graph_generator(df_pso, df_portef, res_file.stem, output_dir)


if __name__ == "__main__":
    main()
