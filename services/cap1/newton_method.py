import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re

def newton_method(x0: float, Tol: float, Niter: int, Fun: str, Fun_prime: str, error_type: str = "absolute", 
                  png_filename: str = "static/imgs/newton_method/newton_plot.png", 
                  html_filename: str = "static/imgs/newton_method/newton_plot.html"):
    try:
        iteraciones = []
        xi_list = []
        f_xi_list = []
        error_list = []


        x = x0
        try:
            fx = eval(Fun)
            fpx = eval(Fun_prime)
        except ZeroDivisionError:
            return {"message": "División por cero detectada en la derivada"}

        if fx == 0:
            return {"root": x0, "message": f"{x0} es raíz de f(x)"}
        elif fpx == 0:
            return {"message": "Derivada cero en el punto inicial, no se puede continuar"}

        c = 0
        error = 1 + Tol  # Initialize error to enter the loop
        iteraciones.append(c)
        xi_list.append(x)
        f_xi_list.append(fx)
        error_list.append("N/A")  # No error on
        while error > Tol and fx != 0 and fpx != 0 and c < Niter:
            # Newton-Raphson formula
            #
            c += 1
            x_old = x
            x_new = x - fx / fpx
            
            # Update function values
            x = x_new
            try:
                fx = eval(Fun)
                fpx = eval(Fun_prime)
            except ZeroDivisionError:
                return {"message": "División por cero detectada en la derivada"}

            # Calculate relative error
            if error_type == "absolute":
                error = abs(x - x_old)
            else:
                error = abs(x - x_old) / abs(x)
            
            # Store iteration results
            iteraciones.append(c)
            xi_list.append(x)
            f_xi_list.append(fx)
            error_list.append(error)
            
            # Prepare for next iteration
            x0 = x

            if error < Tol:
                result = {"root": x, "message": f"{x} es una aproximación de una raíz de f(x) con una tolerancia {Tol}"}
                break
        else:
            result = {"message": f"Fracaso en {Niter} iteraciones"}

        resultados = pd.DataFrame({
            'Iteración': iteraciones,
            'Xi': [str(x) for x in xi_list],
            'f(Xi)': [str(fx) for fx in f_xi_list],
            'Error': [str(e) for e in error_list]
        })

        if xi_list[-1] < x0:
            x_vals = np.linspace(xi_list[-1] - 2, x0 + 2, 1000)
        else:
            x_vals = np.linspace(x0 - 2, xi_list[-1] + 2, 1000)
        f_vals = []
        for x in x_vals:
            f_vals.append(eval(Fun))

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, f_vals, label=f'f(x) = {Fun}', color='blue')
        plt.axhline(0, color='black', linewidth=0.5)

        for i, x in enumerate(xi_list[:-1]):
            plt.plot([xi_list[i], xi_list[i]], [0, f_xi_list[i]], 'r--')  # Vertical line
            plt.scatter(xi_list[i], f_xi_list[i], color='purple', zorder=5)  # Point

        plt.scatter(xi_list[-1], 0, color='green', label="Aproximación Final", zorder=5)

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de Newton')
        plt.legend()
        plt.grid(True)

        plt.savefig(png_filename, format='png')
        plt.close()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=x_vals, y=f_vals, mode='lines', name=f'f(x) = {Fun}', line=dict(color='blue')))

        fig.add_trace(go.Scatter(x=xi_list, y=f_xi_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))

        fig.add_trace(go.Scatter(x=[xi_list[-1]], y=[0], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

        fig.update_layout(title='Método de Newton',
                            xaxis_title='x', yaxis_title='f(x)',
                            template="plotly_white")

        fig.write_html(html_filename)
    except Exception as e:
        return {"message": str(e)}
    else:
        return {
            "result": result,
            "iterations": resultados.to_dict(orient='records'),
            "png_path": png_filename,
            "html_path": html_filename
        }

