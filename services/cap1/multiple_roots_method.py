import pandas as pd
import math
import numpy as np

def multiple_roots_method(x0: float, Tol: float, Niter: int, Fun: str, Derivative1: str, Derivative2: str):
    # Lists to store iteration data
    iteraciones = []
    x_list = []
    f_x_list = []
    error_list = []

    # Initial setup
    x = x0
    fx = eval(Fun)  # Evaluate f(x) at x0
    f_prime = eval(Derivative1)  # Evaluate f'(x) at x0
    f_double_prime = eval(Derivative2)  # Evaluate f''(x) at x0

    # Check if the initial guess is already a root
    if fx == 0:
        return {"root": x0, "message": f"{x0} es raíz de f(x)"}

    # Initial iteration data
    iteraciones.append(0)
    x_list.append(x0)
    f_x_list.append(fx)
    error_list.append(None)  # First iteration has no error yet

    # Iterate until error is within tolerance or max iterations are reached
    for c in range(1, Niter + 1):
        # Prevent division by zero in the update formula
        denominator = f_prime**2 - fx * f_double_prime
        if denominator == 0:
            return {"message": "División por cero detectada en el denominador"}

        # Update x using the multiple roots formula
        x_new = x - (fx * f_prime) / denominator

        # Calculate error
        error = abs(x_new - x)

        # Update lists with current iteration data
        iteraciones.append(c)
        x_list.append(x_new)
        f_x_list.append(eval(Fun))
        error_list.append(error)

        # Update x and re-evaluate functions for the next iteration
        x = x_new
        fx = eval(Fun)
        f_prime = eval(Derivative1)
        f_double_prime = eval(Derivative2)

        # Stop if the root is found or tolerance is met
        if fx == 0:
            return {"root": x, "message": f"{x} es raíz de f(x)"}
        elif error < Tol:
            return {"root": x, "message": f"{x} es una aproximación de una raíz de f(x) con una tolerancia {Tol}"}

    # If max iterations reached without finding the root within tolerance
    return {"message": f"Fracaso en {Niter} iteraciones"}

    # Store results in a DataFrame for output
    resultados = pd.DataFrame({
        'Iteración': iteraciones,
        'x': x_list,
        'f(x)': f_x_list,
        'E (relativo)': error_list
    })

    # Convert the table to a dictionary to return as JSON
    return resultados.to_dict(orient='records')
