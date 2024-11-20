import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import plotly.graph_objects as go
from sympy import symbols, expand

def spline_cubic(vectorx, vectory, png_filename: str = "static/imgs/spline_cubic_method/spline_cubic_plot.png", html_filename: str = "static/imgs/spline_cubic_method/spline_cubic_plot.html"):
    if len(vectorx) != len(vectory):
        return {"error": "Los vectores x e y deben tener la misma longitud."}
    #Verificar que no hayan mas de 8 datos
    if len(vectorx)>8:
        return {"error": "El numero maximo de datos es 8"}
    if len(np.unique(vectorx)) != len(vectorx):
                return {"error": "El vector X no puede contener valores duplicados."}
    
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

    # Crear el spline cúbico usando Scipy (tipo de frontera natural)
    cs = CubicSpline(x, y, bc_type="natural")

    # Obtener los coeficientes del spline por tramos
    tramos_ajustados = ajustar_polinomios(cs, x)

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
        "polinomio": tramos_ajustados,
        "png_path": png_filename,
        "html_path": html_filename
    }
    
def ajustar_polinomios(cs, x):
    # Variables simbólicas para la expansión
    x_sym = symbols('x')
    tramos = []

    for i in range(len(x) - 1):
        # Coeficientes del tramo i
        c3, c2, c1, c0 = cs.c[:, i]
        xi = x[i]
        
        # Polinomio desplazado
        polinomio_desplazado = c3 * (x_sym - xi)**3 + c2 * (x_sym - xi)**2 + c1 * (x_sym - xi) + c0
        
        # Expandir para obtenerlo en términos de x
        polinomio_expandido = expand(polinomio_desplazado)
        tramos.append(str(polinomio_expandido))
    
    return tramos