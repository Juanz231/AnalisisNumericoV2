import pandas as pd
import math
import numpy as np

def newton_method(x0: float, Tol: float, Niter: int, Fun: str, Fun_prime: str):
    # Lists to store iteration data
    iteraciones = []
    xi_list = []
    f_xi_list = []
    error_list = []
    
    # Initial evaluation
    x = x0
    fx = eval(Fun)
    fpx = eval(Fun_prime)
    
    if fx == 0:
        return {"root": x0, "message": f"{x0} es raíz de f(x)"}
    elif fpx == 0:
        return {"message": "Derivada cero en el punto inicial, no se puede continuar"}

    c = 0
    error = Tol + 1  # Initialize error to enter the loop
    
    # Iterate until error < tolerance or root is found
    while error > Tol and fx != 0 and fpx != 0 and c < Niter:
        # Newton-Raphson formula
        x_new = x - fx / fpx
        
        # Update function values
        x = x_new
        fx = eval(Fun)
        fpx = eval(Fun_prime)

        # Calculate relative error
        error = abs(x - x0) / abs(x)
        
        # Store iteration results
        iteraciones.append(c)
        xi_list.append(x)
        f_xi_list.append(fx)
        error_list.append(error)
        
        # Prepare for next iteration
        x0 = x
        c += 1

    # Check if we found a root or reached tolerance
    if fx == 0:
        return {"root": x, "message": f"{x} es raíz de f(x)"}
    elif error < Tol:
        return {"root": x, "message": f"{x} es una aproximación de una raíz de f(x) con una tolerancia {Tol}"}
    else:
        return {"message": f"Fracaso en {Niter} iteraciones"}
    
    # Create the table of results
    resultados = pd.DataFrame({
        'Iteración': iteraciones,
        'xi': xi_list,
        'f(xi)': f_xi_list,
        'E (relativo)': error_list
    })

    # Convert the table to a dictionary for returning
    return resultados.to_dict(orient='records')
