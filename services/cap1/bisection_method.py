import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def bisection_method(a: float, b: float, Tol: float, Niter: int, Fun: str, png_filename: str = "static/imgs/bisection_method/bisection_plot.png", html_filename: str = "static/imgs/bisection_method/bisection_plot.html"):

    # Ensure the directory exists for PNG and HTML

    # Lists to store iteration data
    iteraciones = []
    a_list = []
    b_list = []
    xm_list = []
    f_xm_list = []
    error_list = []

    # Initial evaluations
    x = a
    fa = eval(Fun)
    x = b
    fb = eval(Fun)
    
    # Check if there’s a root at the endpoints
    if fa == 0:
        return {"root": a, "message": f"{a} es raíz de f(x)", "png_path": None, "html_path": None}
    elif fb == 0:
        return {"root": b, "message": f"{b} es raíz de f(x)", "png_path": None, "html_path": None}
    elif fa * fb > 0:
        return {"message": "El intervalo inicial no contiene una raíz", "png_path": None, "html_path": None}

    # Bisection loop
    c = 0
    error = Tol + 1  # Initialize error greater than tolerance
    xm = (a + b) / 2

    # Store initial midpoint and function evaluation
    x = xm
    fxm = eval(Fun)
    
    iteraciones.append(c)
    a_list.append(a)
    b_list.append(b)
    xm_list.append(xm)
    f_xm_list.append(fxm)
    error_list.append(error)
    
    while error > Tol and fxm != 0 and c < Niter:
        # Update interval based on the sign of f(xm)
        if fa * fxm < 0:
            b = xm
        else:
            a = xm
            fa = fxm

        # Recalculate midpoint and function value at new midpoint
        xm_old = xm
        xm = (a + b) / 2
        x = xm
        fxm = eval(Fun)

        # Calculate relative error
        error = abs(xm - xm_old) / abs(xm)
        
        # Store iteration data
        c += 1
        iteraciones.append(c)
        a_list.append(a)
        b_list.append(b)
        xm_list.append(xm)
        f_xm_list.append(fxm)
        error_list.append(error)

    # Check if root was found or tolerance was met
    if fxm == 0:
        result = {"root": xm, "message": f"{xm} es raíz de f(x)"}
    elif error < Tol:
        result = {"root": xm, "message": f"{xm} es una aproximación de una raíz de f(x) con una tolerancia {Tol}"}
    else:
        result = {"message": f"Fracaso en {Niter} iteraciones"}

    # Create the table of results
    resultados = pd.DataFrame({
        'Iteración': iteraciones,
        'a': a_list,
        'b': b_list,
        'xm': xm_list,
        'f(xm)': f_xm_list,
        'E (relativo)': error_list
    })

    # Plotting with Matplotlib (PNG)
    x_vals = np.linspace(a - 100, b + 100, 1000)
    y_vals = [eval(Fun.replace("x", str(x))) for x in x_vals]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f'f(x) = {Fun}', color='blue')
    plt.axhline(0, color='black', linewidth=0.5)

    # Mark each midpoint as it refines to the root
    for i, xm in enumerate(xm_list):
        plt.plot(xm, f_xm_list[i], 'ro' if i == len(xm_list) - 1 else 'go', 
                 label="Aproximación" if i == 0 else "")
    
    # Highlight the final approximation/root
    plt.plot(xm_list[-1], f_xm_list[-1], 'ro', label="Aproximación Final")

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Bisección - Método de Aproximación de Raíces')
    plt.legend()
    plt.grid(True)
    
    # Save the plot as a PNG
    plt.savefig(png_filename, format='png')  # Save as PNG
    plt.close()

    # Plotting with Plotly (HTML for interactivity)
    fig = go.Figure()

    # Function plot
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'f(x) = {Fun}', line=dict(color='blue')))
    
    # Mark the midpoints as they refine to the root
    fig.add_trace(go.Scatter(x=xm_list, y=f_xm_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))

    # Final approximation/root
    fig.add_trace(go.Scatter(x=[xm_list[-1]], y=[f_xm_list[-1]], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

    fig.update_layout(title='Bisección - Método de Aproximación de Raíces',
                      xaxis_title='x', yaxis_title='f(x)',
                      template="plotly_white")

    # Save as HTML file
    fig.write_html(html_filename)

    # Return the result and paths to the saved files
    return {
        "result": result,
        "iterations": resultados.to_dict(orient='records'),
        "png_path": png_filename,
        "html_path": html_filename
    }

