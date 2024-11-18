import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re

def fixedpoint_method(X0: float, Tol: float, Niter: int, Fun: str, GFun: str, error_type: str = "absolute", png_filename: str = "static/imgs/false_position_method/false_position_plot.png", html_filename: str = "static/imgs/false_position_method/false_position_plot.html"):
    # Lists to store iteration data
    iteraciones = []
    x_list = []
    g_x_list = []
    f_x_list = []
    error_list = []
    try:
        # Initial setup
        c = 0
        error = Tol + 1  # Initialize error greater than tolerance
        x_current = X0
        
        try:
            # Evaluate the functions with the initial value
            f_x = eval(Fun)
            g_x = eval(GFun)
        except DivideByZeroError:
            return {"message": "División por cero en la evaluación de la función. Intente con otro valor inicial."}

        if f_x == 0:
            return {"root": g_x, "message": f"{x_current} es raíz de f(x)"}

        iteraciones.append(c)
        x_list.append(x_current)
        g_x_list.append(g_x)
        f_x_list.append(f_x)
        error_list.append("N/A")

        while error > Tol and c < Niter:
            # Evaluate g(x) for the iteration and f(x) to track root behavior
            x = x_current
            g_x = eval(GFun)
            f_x = eval(Fun)

            # Compute error
            if error_type == "absolute":
                error = abs(g_x - x_current)
            else:
                error = abs(g_x - x_current) / abs(g_x)

            # Store iteration data
            iteraciones.append(c)
            x_list.append(x_current)
            g_x_list.append(g_x)
            f_x_list.append(f_x)
            error_list.append(error)

            # Check if the function value is close to zero
            if error < Tol:
                result = {"root": g_x, "message": f"{g_x} es una aproximación de una raíz de f(x) con tolerancia {Tol} en {c} iteraciones"}
                break
            # Update for next iteration
            x_current = g_x
            c += 1

        else:
            # If the loop finishes without finding a root
            result = {"message": f"Fracaso en {Niter} iteraciones"}

        # Store results in a DataFrame for output
        resultados = pd.DataFrame({
            'Iteración': iteraciones,
            'Xi': [str(x) for x in x_list],
            'g(Xi)': [str(x) for x in g_x_list],
            'f(Xi)': [str(f) for f in f_x_list],
            'Error': [str(e) for e in error_list]
        })

        # Plotting with Matplotlib (PNG)
        x_vals = np.linspace(X0 - 2, X0 + 2, 1000)
        f_vals = []
        g_vals = []
        for x in x_vals:
            safe_fun = re.sub(r'\bx\b', f'({x})', Fun)
            safeg_fun = re.sub(r'\bx\b', f'({x})', GFun) # Replace standalone 'x'
            f_vals.append(eval(safe_fun, {"np": np}))
            g_vals.append(eval(safeg_fun, {"np": np})) # Evaluate the expression    

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, f_vals, label=f'f(x) = {Fun}', color='blue')
        plt.plot(x_vals, g_vals, label=f'g(x) = {GFun}', color='orange')
        plt.axhline(0, color='black', linewidth=0.5)

        # Highlight iterations
        for i, x in enumerate(x_list[:-1]):
            plt.plot([x, x], [x, g_x_list[i]], 'r--')  # Vertical line
            plt.plot([x, g_x_list[i]], [g_x_list[i], g_x_list[i]], 'r--')  # Horizontal line
        
        # Add points for f(x_i) on the f(x) curve
        f_x_iter_vals = []
        for i in range(len(x_list)):
            x = x_list[i]
            f_x_iter_vals.append(eval(Fun))
        
        plt.scatter(x_list, f_x_iter_vals, color='purple', label='f(x) at Iterations', zorder=5)
        # Final approximation
        plt.plot(x_list[-1], g_x_list[-1], 'ro', label="Aproximación Final")

        plt.xlabel('x')
        plt.ylabel('f(x) / g(x)')
        plt.title('Método de Punto Fijo')
        plt.legend()
        plt.grid(True)

        # Save the plot as a PNG
        plt.savefig(png_filename, format='png')
        plt.close()

        # Plotting with Plotly (HTML for interactivity)
        fig = go.Figure()

        # Function plot
        fig.add_trace(go.Scatter(x=x_vals, y=f_vals, mode='lines', name=f'f(x) = {Fun}', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x_vals, y=g_vals, mode='lines', name=f'g(x) = {GFun}', line=dict(color='orange')))

        # Iteration points
        fig.add_trace(go.Scatter(x=x_list, y=g_x_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))
        fig.add_trace(go.Scatter(
        x=x_list,
        y=f_vals,
        mode='markers',
        name='f(x) at Iterations',
        marker=dict(color='purple', size=8)
        ))
        # Final approximation/root
        fig.add_trace(go.Scatter(x=[x_list[-1]], y=[g_x_list[-1]], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

        fig.update_layout(title='Método de Punto Fijo',
                        xaxis_title='x', yaxis_title='f(x) / g(x)',
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

