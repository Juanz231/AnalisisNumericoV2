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
        # Initial setup
        c = 0
        error = Tol + 1  # Initialize error greater than tolerance
        x_current = X0
        error_list.append("N/A")  # No error on the first iteration
        
        while error > Tol and c < Niter:
            # Store the current value of x
            x_old = x_current
            x = x_old
            # Evaluate g(x) and f(x) at the current x
            g_x = eval(GFun)  # g(x)
            f_x = eval(Fun)   # f(x)

            # Compute the error based on the selected type
            if error_type == "absolute":
                error = abs(g_x - x_old)  # Use x_old for the previous value
            else:  # relative error
                if abs(g_x) > 1e-12:  # Prevent division by zero
                    error = abs(g_x - x_old) / abs(g_x)
                else:
                    error = float('inf')  # Set a large error if division is unstable
            

            # Update x_current for the next iteration
            x_current = g_x

            # Increment iteration count
            c += 1

            # Store iteration data
            iteraciones.append(c)
            x_list.append(x_old)
            g_x_list.append(g_x)
            f_x_list.append(f_x)
            
            # Compute the absolute error
            # Update x_current for the next iteration
            x_current = g_x

            # Increment iteration count
            c += 1

            # Check for root
            if error < Tol:
                result = {"root": g_x, "message": f"{g_x} es una aproximación de una raíz de f(x) con tolerancia {Tol} y un error de {str(error)} en {c} iteraciones"}
                break
            
            error_list.append(error)

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
        if x_list[-1] < X0:
            x_vals = np.linspace(x_list[-1] - 2, X0 + 2, 1000)
        else:
            x_vals = np.linspace(X0 - 2, x_list[-1] + 2, 1000)
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
        plt.plot(x_vals, x_vals, label='y = x', color='green', linestyle='dashed')
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
        fig.add_trace(go.Scatter(x=x_vals, y=x_vals, mode='lines', name='y = x', line=dict(color='green', dash='dash')))
        # Iteration points
        fig.add_trace(go.Scatter(x=x_list, y=g_x_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))
        fig.add_trace(go.Scatter(
        x=x_list,
        y=f_x_list,
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
        print(e)
        return {"message": str(e)}

    else:
        # Return the result and paths to the saved files
        return {
            "result": result,
            "iterations": resultados.to_dict(orient='records'),
            "png_path": png_filename,
            "html_path": html_filename
        }

