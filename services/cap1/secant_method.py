import pandas as pd
import math
import numpy as np

def secant_method(Xi: float, Xs: float, Tol: float, Niter: int, Fun: str):
    # Listas para almacenar los valores de la función y los errores
    iteraciones = []
    xi_list = []
    f_xi_list = []
    error_list = []
    
    # Evaluación inicial
    x = Xi
    fi = eval(Fun)
    x = Xs
    fs = eval(Fun)
    
    # Comprobación inicial de raíces en los extremos
    if fi == 0:
        return {"root": Xi, "message": f"{Xi} es raíz de f(x)"}
    elif fs == 0:
        return {"root": Xs, "message": f"{Xs} es raíz de f(x)"}
    else:
        c = 0
        # Primera aproximación por método de la secante
        Xm = Xi - (fi * (Xs - Xi)) / (fs - fi)
        
        x = Xm
        fe = eval(Fun)

        # Almacenamos la primera iteración
        iteraciones.append(c)
        xi_list.append(Xm)
        f_xi_list.append(fe)
        error_list.append(100)  # Primer error inicial grande

        # Iteración hasta que el error sea menor que la tolerancia o se alcance la raíz exacta
        while error_list[c] > Tol and fe != 0 and c < Niter:
            Xi_old = Xi  # Guardar el valor anterior
            Xi = Xs  # Actualizamos Xi a Xs
            Xs = Xm  # Actualizamos Xs al nuevo Xm
            fi = fs
            fs = fe

            # Verificación de división por cero
            Xm = Xi - (fi * (Xs - Xi)) / (fs - fi)
            
            x = Xm
            fe = eval(Fun)

            # Cálculo del error
            Error = abs(Xm - Xs)/Xm

            # Almacenamos los resultados de cada iteración
            c += 1
            iteraciones.append(c)
            xi_list.append(Xm)
            f_xi_list.append(fe)
            error_list.append(Error)

        # Verificación de la raíz o aproximación
        if fe == 0:
            return {"root": Xm, "message": f"{Xm} es raíz de f(x)"}
        elif Error < Tol:
            return {"root": Xm, "message": f"{Xm} es una aproximación de una raíz de f(x) con una tolerancia {Tol}"}
        else:
            return {"message": f"Fracaso en {Niter} iteraciones"}

        # Crear la tabla de resultados
        resultados = pd.DataFrame({
            'Iteración': iteraciones,
            'xi': xi_list,
            'f(xi)': f_xi_list,
            'E (relativo)': error_list
        })

        # Convertir la tabla a un diccionario para devolver
        return resultados.to_dict(orient='records')
