import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def vandermonde_method(vectorx, vectory, png_filename: str = "static/imgs/vandermonde_method/vandermonde_plot.png", html_filename: str = "static/imgs/vandermonde_method/vandermonde_plot.html"):
    try:
        # Verificar que los vectores tienen la misma longitud
        if len(vectorx) != len(vectory):
            return {"error": "Los vectores x e y deben tener la misma longitud."}

        # Asignar los vectores de entrada
        xv = np.array(vectorx, dtype=float)
        yv = np.array(vectory, dtype=float)

        # Establecer la variable "degree"
        degree = len(xv)

        # Crear la matriz de Vandermonde
        A = np.vander(xv, N=degree, increasing=False)

        # Resolver el sistema de ecuaciones para encontrar los coeficientes del polinomio
        coeficientes = np.linalg.solve(A, yv)

        # Crear el polinomio como texto
        terms = [f"{coef:.4f}x^{degree-i-1}" if i < degree - 1 else f"{coef:.4f}" 
                 for i, coef in enumerate(coeficientes)]
        polinomio = " + ".join(terms).replace("x^0", "").replace(" 1.0000x", " x").replace("x^1 ", "x ")

        # Crear un conjunto de puntos para graficar el polinomio
        x_vals = np.linspace(min(xv), max(xv), 1000)
        y_vals = np.polyval(coeficientes, x_vals)

        # Graficar el polinomio resultante
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'r', label='Polinomio')
        plt.plot(xv, yv, 'bo', label='Puntos de entrada')  # Puntos en azul
        plt.title('Polinomio usando matriz de Vandermonde')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)

        # Save the plot as a PNG
        plt.savefig(png_filename, format='png')  # Save as PNG
        plt.close()

        # Plotting with Plotly (HTML for interactivity)
        fig = go.Figure()

        # Function plot
        fig.add_trace(go.Scatter(x=xv, y=yv, mode='markers', name=f'Datos', line=dict(color='blue')))

        # Mark the midpoints as they refine to the root
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Polinomio de Interpolación", marker=dict(color='red', size=8)))

        fig.update_layout(title='Vandermonde - Metodo de interpolacion',
                          xaxis_title='x', yaxis_title='y',
                          template="plotly_white")

        # Save as HTML file
        fig.write_html(html_filename)

        return {
            "polinomio": f"El polinomio es: {polinomio}",
            "Matriz de Vandermonde": A.tolist(),  # Convertir a lista para JSON serializable
            "Coeficientes": coeficientes.tolist(),
            "png_path": png_filename,
            "html_path": html_filename
        }
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
