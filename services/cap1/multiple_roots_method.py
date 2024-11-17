import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re

def multiple_roots_method(
    x0: float, Tol: float, Niter: int, Fun: str, Derivative1: str, Derivative2: str, error_type: str = "absolute",
    png_filename: str = "static/imgs/multiple_roots_method/multiple_roots_plot.png",
    html_filename: str = "static/imgs/multiple_roots_method/multiple_roots_plot.html"
):
    try:
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

        error = 1 + Tol  # Initialize error to enter the loop
        # Initial iteration data
        iteraciones.append(0)
        x_list.append(x0)
        f_x_list.append(fx)
        error_list.append("N/A")  # First iteration has no error yet

        # Iterate until error is within tolerance or max iterations are reached
        for c in range(1, Niter + 1):
            # Prevent division by zero in the update formula
            denominator = f_prime**2 - fx * f_double_prime
            if denominator == 0:
                return {"message": "División por cero detectada en el denominador"}

            # Update x using the multiple roots formula
            x_new = x - (fx * f_prime) / denominator

            # Calculate error
            if error_type == "absolute":
                error = abs(x_new - x)
            else:
                error = abs(x_new - x) / abs(x_new)
            
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
            if error < Tol:
                result = {"root": x, "message": f"{x} es una aproximación de una raíz de f(x) con tolerancia {Tol} en {c} iteraciones"}
                break
        else:
            result = {"message": f"Fracaso en {Niter} iteraciones"}

        # Store results in a DataFrame for output
        resultados = pd.DataFrame({
            'Iteración': iteraciones,
            'Xi': x_list,
            'f(Xi)': f_x_list,
            'Error': error_list
        })

        # Plotting with Matplotlib (PNG)
        x_vals = np.linspace(x0 - 10, x0 + 10, 1000)
        f_vals = []
        for x in x_vals:
            f_vals.append(eval(Fun))

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, f_vals, label=f'f(x) = {Fun}', color='blue')
        plt.axhline(0, color='black', linewidth=0.5)

        # Highlight iterations
        for i, x in enumerate(x_list[:-1]):
            plt.plot([x, x], [f_x_list[i], 0], 'r--')  # Vertical line

        # Add iteration points
        plt.scatter(x_list, f_x_list, color='purple', label='f(x) at Iterations', zorder=5)

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de Raíces Múltiples')
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
        fig.add_trace(go.Scatter(x=x_list, y=f_x_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))

        # Final approximation/root
        fig.add_trace(go.Scatter(x=[x_list[-1]], y=[f_x_list[-1]], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

        fig.update_layout(title='Método de Raíces Múltiples',
                        xaxis_title='x', yaxis_title='f(x)',
                        template="plotly_white")

        fig.write_html(html_filename)
    except Exception as e:
        return {"message": str(e)}

    else:

        # Return the result and paths to the saved files
        return {
            "result": result,
            "iterations": resultados.to_dict(orient='records'),
            "png_path": png_filename,
            "html_path": html_filename
        }

