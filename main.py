from math import sqrt
from typing import override

import numpy as np


def load_data(filename: str):
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


def get_covariance(std_devs, corr_matrix):
    return np.outer(std_devs, std_devs) * corr_matrix


def main():
    mean_return, std_devs, corr_matrix = load_data("./data/port1.txt")
    covar_matrix = get_covariance(std_devs, corr_matrix)

    poblation = poblation_init(mean_return.shape[0], corr_matrix, mean_return)
    print(poblation[0])
    print(poblation[1])


def poblation_init(n_assets, covar_matrix, mean_return, n_poblation=2):
    poblation = []
    for i in range(n_poblation):
        position = np.random.rand(n_assets)
        position = normalization(position)
        velocity = np.zeros(n_assets)
        fitness = fitness_function(position, mean_return, covar_matrix)

        poblation.append(Particle(position, velocity, fitness))

    return poblation


def fitness_function(position, mean_return, covar_matrix):
    """
    We assume we need to minimize the risk by a given return_value
    TODO(Find min and max return values)
    TODO(Add maximize return given a risk value)
    """
    penalty = 1e6
    target_return = 0.003

    p_return = np.dot(position, mean_return)

    p_variance = np.dot(position, np.dot(covar_matrix, position))  # also know as risk

    fitness = sqrt(p_variance)

    if p_return < target_return:
        diff = target_return - p_return
        fitness += penalty * (diff**2)

    return -fitness
    # Se piensa en si el fitness es mejor
    # fitness > g_best_fitness
    # minimizamos el riesgo, valores ~0 son mejor


class Particle:
    def __init__(self, position, velocity, fitness_value):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.best_pos = self.position.copy()
        self.best_val = fitness_value

    @override
    def __str__(self) -> str:
        return f"Position: {self.position}\nValue: {self.best_val}"


def normalization(particle):
    particle = np.maximum(0, particle)

    total_weight = np.sum(particle)
    if total_weight > 0:
        particle /= total_weight

    return particle


main()
