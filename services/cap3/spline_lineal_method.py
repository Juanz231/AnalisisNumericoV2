import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def spline_lineal(vectorx, vectory, png_filename: str = "static/imgs/spline_lineal_method/spline_lineal_plot.png", html_filename: str = "static/imgs/spline_lineal_method/spline_lineal_plot.html"):
    x = np.array(vectorx, dtype=float)
    y = np.array(vectory, dtype=float)
    n = len(x)
    
    # Verificar que hay suficientes puntos
    if n < 2:
        return {
            "message": "Se necesitan al menos 2 puntos para calcular un spline lineal.",
            "successful": False,
            "segments": [],
            "equations": [],
        }
    
    segments = []
    equations = []

    # Calcular los tramos
    for i in range(n - 1):
        # Pendiente
        m = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
        # Ecuación del tramo
        tramo = f"{m:.4f}*(x - {x[i]:.4f}) + {y[i]:.4f}"
        segments.append(tramo)
        equations.append(f"Tramo {i + 1}: {tramo}")
    
    # Crear el gráfico
    x_vals = []
    y_vals = []
    for i in range(n - 1):
        x_segment = np.linspace(x[i], x[i + 1], 100)
        y_segment = eval(segments[i].replace("x", "x_segment"))
        x_vals.extend(x_segment)
        y_vals.extend(y_segment)

    plt.figure()
    plt.plot(x_vals, y_vals, 'r', label="Spline Lineal")
    plt.plot(x, y, 'bo', label="Puntos de entrada")
    plt.title("Spline Lineal")
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
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Spline Lineal", marker=dict(color='red', size=8)))


    fig.update_layout(title='Spline lineal - Metodo de interpolacion',
                      xaxis_title='x', yaxis_title='y',
                      template="plotly_white")

    # Save as HTML file
    fig.write_html(html_filename)
    
    return {
        "message": "Spline lineal calculado con éxito.",
        "successful": True,
        "segments": segments,
        "equations": equations,
    }

