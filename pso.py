from math import sqrt
from random import random
from typing import override

import numpy as np


def pso(mean_return, std_devs, covar_matrix):
    swarm = swarm_init(mean_return.shape[0], covar_matrix, mean_return)

    best_g_pos, best_g_val = get_best_particle(swarm)

    for i in range(100):
        for particle in swarm:
            update_particle(particle, best_g_pos, mean_return, covar_matrix)

        best_iter_pos, best_iter_val = get_best_particle(swarm)

        if best_iter_val < best_g_val:
            best_g_pos = best_iter_pos.copy()
            best_g_val = best_iter_val

    return best_g_val, best_g_pos
    # EActualmente el mejor valor es el fitnes, o sea el riesgo (varianza del partafolio)
    # la posicion es cuanto tenemos invertido en cada activo
    # el retorno se calcula con el producto punto


def swarm_init(n_assets, covar_matrix, mean_return, n_swarm=1000):
    swarm = []
    for i in range(n_swarm):
        position = np.random.rand(n_assets)
        position = normalization(position)
        velocity = np.zeros(n_assets)
        fitness = fitness_function(position, mean_return, covar_matrix)

        swarm.append(Particle(position, velocity, fitness))

    return swarm


def fitness_function(
    position,
    mean_return,
    covar_matrix,
):
    """
    We assume we need to minimize the risk by a given return_value
    TODO(Find min and max return values)
    TODO(Add maximize return given a risk value)
    """
    penalty = 1e4
    target_return = 0.01

    p_return: float = np.dot(position, mean_return)

    p_variance: float = np.dot(
        position, np.dot(covar_matrix, position)
    )  # also know as risk

    fitness: float = sqrt(p_variance)

    if p_return < target_return:
        diff = target_return - p_return
        fitness += penalty * (diff**2)

    return fitness
    # Se piensa en si el fitness es mejor
    # fitness > g_best_fitness
    # minimizamos el riesgo, valores ~0 son mejor


def update_particle(
    p,
    best_g_pos,
    mean_return,
    covar_matrix,
    C1=0.5,
    C2=1.0,
    INERTIA=0.8,
):
    """
    Actualizacion de velocidad tomando en cuenta los mejores particulas globales
    TODO(Ver si es necesario copiar el arreglo np para estas operaciones)
    """
    r1 = random()
    r2 = random()
    new_velocity = (
        (INERTIA * p.velocity)
        + (C1 * r1 * (p.best_pos - p.position))
        + (C2 * r2 * (best_g_pos - p.position))
    )
    p.velocity = new_velocity
    new_position = p.position + p.velocity
    p.position = normalization(new_position)

    new_fitness = fitness_function(p.position, mean_return, covar_matrix)
    # print(new_fitness)

    if new_fitness < p.best_val:
        p.best_val = new_fitness
        p.best_pos = p.position.copy()


class Particle:
    def __init__(
        self,
        position,
        velocity,
        fitness_value,
    ):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.best_pos = self.position.copy()
        self.best_val = fitness_value

    @override
    def __str__(self) -> str:
        return f"Position: {self.position}\nValue: {self.best_val}"


def normalization(position):
    position = np.maximum(0, position)

    total_weight = np.sum(position)
    if total_weight > 0:
        position /= total_weight

    return position


def get_covariance(std_devs, corr_matrix):
    return np.outer(std_devs, std_devs) * corr_matrix


def get_best_particle(swarm):
    best_p = min(swarm, key=lambda p: p.best_val)
    return best_p.best_pos, best_p.best_val
