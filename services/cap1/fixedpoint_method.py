import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def fixedpoint_method(X0: float, Tol: float, Niter: int, Fun: str, GFun: str):
    # Lists to store iteration data
    iteraciones = []
    x_list = []
    g_x_list = []
    f_x_list = []
    error_list = []

    # Initial setup
    c = 0
    error = Tol + 1  # Initialize error greater than tolerance
    x_current = X0

    while error > Tol and c < Niter:
        # Evaluate g(x) for the iteration and f(x) to track root behavior
        g_x = eval(GFun.replace("x", str(x_current)))
        f_x = eval(Fun.replace("x", str(x_current)))

        # Compute error
        error = abs(g_x - x_current)

        # Store iteration data
        iteraciones.append(c)
        x_list.append(x_current)
        g_x_list.append(g_x)
        f_x_list.append(f_x)
        error_list.append(error)

        # Check if the function value is close to zero
        if abs(f_x) < Tol:
            result = {"root": g_x, "message": f"{g_x} es una aproximación de una raíz de f(x) con tolerancia {Tol} en {c} iteraciones"}
            break
        elif error < Tol:
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
        'Xi': x_list,
        'g(Xi)': g_x_list,
        'f(Xi)': f_x_list,
        'Error': error_list
    })

    # Plotting with Matplotlib (PNG)
    x_vals = np.linspace(X0 - 2, X0 + 2, 1000)
    f_vals = [eval(Fun.replace("x", str(x))) for x in x_vals]
    g_vals = [eval(GFun.replace("x", str(x))) for x in x_vals]
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, f_vals, label=f'f(x) = {Fun}', color='blue')
    plt.plot(x_vals, g_vals, label=f'g(x) = {GFun}', color='orange')
    plt.plot(x_vals, x_vals, label='y = x', color='green', linestyle='--')  # Line y = x
    plt.axhline(0, color='black', linewidth=0.5)

    # Highlight iterations
    for i, x in enumerate(x_list[:-1]):
        plt.plot([x, x], [x, g_x_list[i]], 'r--')  # Vertical line
        plt.plot([x, g_x_list[i]], [g_x_list[i], g_x_list[i]], 'r--')  # Horizontal line
    
    # Add points for f(x_i) on the f(x) curve
    f_x_iter_vals = [eval(Fun.replace("x", str(x))) for x in x_list]
    
    plt.scatter(x_list, f_x_iter_vals, color='purple', label='f(x) at Iterations', zorder=5)
    # Final approximation
    plt.plot(x_list[-1], g_x_list[-1], 'ro', label="Aproximación Final")

    plt.xlabel('x')
    plt.ylabel('f(x) / g(x)')
    plt.title('Método de Punto Fijo')
    plt.legend()
    plt.grid(True)

    # Save the plot as a PNG
    png_filename = 'Imgs/fixedpoint_method/fixed_point_plot.png'
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
    y=[eval(Fun.replace("x", str(x))) for x in x_list],
    mode='markers',
    name='f(x) at Iterations',
    marker=dict(color='purple', size=8)
    ))
    # Final approximation/root
    fig.add_trace(go.Scatter(x=[x_list[-1]], y=[g_x_list[-1]], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

    fig.update_layout(title='Método de Punto Fijo',
                      xaxis_title='x', yaxis_title='f(x) / g(x)',
                      template="plotly_white")

    html_filename = 'Imgs/fixedpoint_method/fixed_point_plot.html'
    fig.write_html(html_filename)

    # Return the result and paths to the saved files
    return {
        "result": result,
        "iterations": resultados.to_dict(orient='records'),
        "png_path": png_filename,
        "html_path": html_filename
    }

