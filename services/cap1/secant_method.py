
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def secant_method(Xi: float, Xs: float, Tol: float, Niter: int, Fun: str, 
                  png_filename: str = "static/imgs/secant_method/secant_plot.png", 
                  html_filename: str = "static/imgs/secant_method/secant_plot.html"):
    # Lists for storing iteration data
    iteraciones = []
    xi_list = []
    f_xi_list = []
    error_list = []
    
    # Initial evaluation
    x = Xi
    fi = eval(Fun)
    x = Xs
    fs = eval(Fun)
    
    # Check if initial guesses are roots
    if fi == 0:
        return {"root": Xi, "message": f"{Xi} es raíz de f(x)"}
    elif fs == 0:
        return {"root": Xs, "message": f"{Xs} es raíz de f(x)"}
    else:
        c = 0
        Xm = Xi - (fi * (Xs - Xi)) / (fs - fi)
        x = Xm
        fe = eval(Fun)

        # Store initial iteration
        iteraciones.append(c)
        xi_list.append(Xm)
        f_xi_list.append(fe)
        error_list.append(1)  # Arbitrary large initial error

        # Iterate until convergence
        while error_list[-1] > Tol and fe != 0 and c < Niter:
            Xi_old = Xi
            Xi = Xs
            Xs = Xm
            fi = fs
            fs = fe

            # Avoid division by zero
            if fs - fi == 0:
                return {"message": "División por cero detectada durante el cálculo"}
            
            Xm = Xi - (fi * (Xs - Xi)) / (fs - fi)
            x = Xm
            fe = eval(Fun)

            Error = abs(Xm - Xs) / abs(Xm)

            c += 1
            iteraciones.append(c)
            xi_list.append(Xm)
            f_xi_list.append(fe)
            error_list.append(Error)

        # Check for convergence or failure
            if fe == 0:
                result = {"root": Xm, "message": f"{Xm} es raíz de f(x)"}
                break
            elif error_list[-1] < Tol:
                result = {"root": Xm, "message": f"{Xm} es una aproximación de una raíz de f(x) con una tolerancia {Tol}"}
                break
        else:
            result = {"message": f"Fracaso en {Niter} iteraciones"}
        
        # Create a DataFrame for results
        resultados = pd.DataFrame({
            'Iteración': iteraciones,
            'Xi': xi_list,
            'f(Xi)': f_xi_list,
            'Error': error_list
        })

        # Plotting with Matplotlib (PNG)
        x_vals = np.linspace(min(Xi, Xs) - 5, max(Xi, Xs) + 5, 1000)
        f_vals = [eval(Fun) for x in x_vals]

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, f_vals, label=f'f(x) = {Fun}', color='blue')
        plt.axhline(0, color='black', linewidth=0.5)

        # Highlight iterations
        for i, x in enumerate(xi_list[:-1]):
            plt.plot([xi_list[i], xi_list[i]], [0, f_xi_list[i]], 'r--')  # Vertical line
            plt.scatter(xi_list[i], f_xi_list[i], color='purple', zorder=5)  # Point

        # Final approximation
        plt.scatter(xi_list[-1], 0, color='green', label="Aproximación Final", zorder=5)

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de la Secante')
        plt.legend()
        plt.grid(True)

        # Save the plot as a PNG
        plt.savefig(png_filename, format='png')
        plt.close()

        # Plotting with Plotly (HTML for interactivity)
        fig = go.Figure()

        # Function plot
        fig.add_trace(go.Scatter(x=x_vals, y=f_vals, mode='lines', name=f'f(x) = {Fun}', line=dict(color='blue')))

        # Iteration points
        fig.add_trace(go.Scatter(x=xi_list, y=f_xi_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))

        # Final approximation/root
        fig.add_trace(go.Scatter(x=[xi_list[-1]], y=[0], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

        fig.update_layout(title='Método de la Secante',
                          xaxis_title='x', yaxis_title='f(x)',
                          template="plotly_white")

        fig.write_html(html_filename)

        # Return results and plot paths
        return {
            "result": result,
            "iterations": resultados.to_dict(orient='records'),
            "png_path": png_filename,
            "html_path": html_filename
        }

