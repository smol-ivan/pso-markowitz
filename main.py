import numpy as np

from pso import get_covariance, pso
from utils import load_data


def main():
    mean_return, std_devs, corr_matrix = load_data("./data/port1.txt")
    covar_matrix = get_covariance(std_devs, corr_matrix)

    best_fitness, best_position = pso(mean_return, std_devs, covar_matrix)

    print(f"Mejor posicion: {best_position}")
    print(f"Reisgo/varianza: {best_fitness * 100:.2f}%")
    print(f"Retorno: {np.dot(best_position, mean_return) * 100:.2f}%")
    print(f"Peso del portafolio: {best_position.sum()}")


main()
