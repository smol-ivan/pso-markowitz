import argparse
import os
from math import sqrt
from pathlib import Path

import numpy as np

from pso import OptimizationMode, get_covariance, pso
from utils import get_limits_return_target, get_limits_risk_target, load_data, save_result_csv


def main():
    # main.py n_particulas iteraciones c1 c2 modo target
    parser = argparse.ArgumentParser(
        prog="psoMarkowitz",
        description="Porfolio Optimization following the Model developed by Markowitz, implementation made with Particle Swarp Optimization",
        epilog="Handmade with love ♡ (˘▽˘>ԅ( ˘⌣˘)",
    )
    parser.add_argument(
        "--n_swarm", "-n", default=100, help="How beeeg the population it is", type=int
    )
    parser.add_argument(
        "--iter",
        "-i",
        default=200,
        help="How many loops, be mindful so the algorithm has time to covergence for accurate results",
        type=int,
    )
    parser.add_argument("--C1", help="Personal influence", type=float, default=0.5)
    parser.add_argument("--C2", help="Social influence", type=float, default=0.5)
    parser.add_argument(
        "--mode",
        help="How are we gonna make money? by target return or target risk. Choose wisely ...",
        choices=[mode.value for mode in OptimizationMode],
        default=OptimizationMode.MINIMIZE_RISK.value,
    )
    parser.add_argument("--target_value", help="Self explaining title LOL", type=float)
    # hacer que con un flag se pueda llamar una funcion que imprima los valores minimos/maximos a tomar, dado un modo y ya, se podria imprimir para todos los archivos o que se reciva path a uno
    parser.add_argument(
        "--limits_return",
        "-lre",
        help="Print min and max values for target return",
        action="store_true",
    )
    parser.add_argument(
        "--limits_risk",
        "-lri",
        help="Print min and max values for target risk",
        action="store_true",
    )
    parser.add_argument(
        "--save-result",
        help="Save result to CSV file in results/ folder",
        action="store_true",
    )
    parser.add_argument("data_file", help="Path to portfolio data file", type=str)
    args = parser.parse_args()

    print(args)
    mean_return, std_devs, corr_matrix = load_data(args.data_file)

    if not args.limits_return and not args.limits_risk:
        covar_matrix = get_covariance(std_devs, corr_matrix)

        best_fitness, best_position = pso(
            mean_return,
            covar_matrix,
            args.iter,
            args.n_swarm,
            OptimizationMode(args.mode),
            args.C1,
            args.C2,
            args.target_value,
        )
        
        portfolio_return = np.dot(best_position, mean_return)
        portfolio_risk = sqrt(np.dot(best_position, np.dot(covar_matrix, best_position)))
        
        if args.save_result:
            save_result_csv(
                args.mode,
                args.data_file,
                args.target_value,
                portfolio_risk,
                portfolio_return,
            )

        print(f"Mejor posicion: {best_position}")
        print(f"Reisgo/varianza: {best_fitness * 100:.2f}%")
        print(f"Retorno: {np.dot(best_position, mean_return) * 100:.2f}%")
        print(f"Peso del portafolio: {best_position.sum()}")

    elif args.limits_return:
        get_limits_return_target(mean_return)
    elif args.limits_risk:
        get_limits_risk_target(std_devs)


main()
