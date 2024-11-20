import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import plotly.graph_objects as go

def spline_cubic(vectorx, vectory, png_filename: str = "static/imgs/spline_cubic_method/spline_cubic_plot.png", html_filename: str = "static/imgs/spline_cubic_method/spline_cubic_plot.html"):
    if len(vectorx) != len(vectory):
        return {"error": "Los vectores x e y deben tener la misma longitud."}
    x = np.array(vectorx, dtype=float)
    y = np.array(vectory, dtype=float)

    # Verificar que hay suficientes puntos
    if len(x) < 3:
        return {
            "error": "Se necesitan al menos 3 puntos para calcular un spline cúbico."
        }

    # Ordenar los puntos por los valores de x
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]

    # Crear el spline cúbico usando Scipy
    cs = CubicSpline(x, y, bc_type="natural")

    # Obtener los coeficientes del spline por tramos
    coefs = cs.c.T  # Cada fila contiene los coeficientes de un tramo
    tramos = []
    for i in range(len(coefs)):
        tramo = (
            f"{coefs[i, 3]:.4f}*(x - {x[i]:.4f})^3 + {coefs[i, 2]:.4f}*(x - {x[i]:.4f})^2 "
            f"+ {coefs[i, 1]:.4f}*(x - {x[i]:.4f}) + {coefs[i, 0]:.4f}"
        )
        tramos.append(tramo)

    # Crear el gráfico del spline
    x_vals = np.linspace(min(x), max(x), 1000)
    y_vals = cs(x_vals)

    plt.figure()
    plt.plot(x_vals, y_vals, "r", label="Spline Cúbico")
    plt.plot(x, y, "bo", label="Puntos de entrada")
    plt.title("Spline Cúbico Natural")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    
    # Save the plot as a PNG
    plt.savefig(png_filename, format='png')  # Save as PNG
    plt.close()

    # Plotting with Plotly (HTML for interactivity)
    fig = go.Figure()

    # Function plot
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Puntos de entrada', line=dict(color='blue')))
    
    # Mark the midpoints as they refine to the root
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Spline Cúbico", marker=dict(color='red', size=8)))


    fig.update_layout(title='Spline Cúbico - Metodo de interpolacion',
                      xaxis_title='x', yaxis_title='y',
                      template="plotly_white")

    # Save as HTML file
    fig.write_html(html_filename)

    return {
        "polinomio": tramos,
        "png_path": png_filename,
        "html_path": html_filename
    }