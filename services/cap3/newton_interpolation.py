import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def newton_interpolation_method(x, y, png_filename: str = "static/imgs/newton_int_method/newton_int_plot.png", html_filename: str = "static/imgs/newton_int_method/newton_int_plot.html"):
    
    if len(x) != len(y):
        return {"error": "Los vectores x e y deben tener la misma longitud."}
        
    # Convertir x e y a arrays numéricos
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    
    # Número de puntos
    n = len(x)
    
    # Crear la tabla de diferencias divididas
    Tabla = np.zeros((n, n + 1))
    Tabla[:, 0] = x
    Tabla[:, 1] = y

    for j in range(2, n + 1):
        for i in range(j - 1, n):
            Tabla[i, j] = (Tabla[i, j - 1] - Tabla[i - 1, j - 1]) / (Tabla[i, 0] - Tabla[i - j + 1, 0])
    
    # Extraer los coeficientes
    coef = np.diag(Tabla, k=1)
    
    # Construir el polinomio de interpolación
    pol = [coef[0]]
    acum = [1]
    pol_text = f"{coef[0]:.4f}"  # Empezamos con el primer coeficiente en formato de texto
    
    for i in range(1, n):
        pol = np.append([0], pol)
        acum = np.convolve(acum, [1, -x[i - 1]])
        pol = pol + coef[i] * acum
        
        # Concatenar el término correspondiente en el polinomio como texto
        term = f"({coef[i]:.4f})"
        for j in range(len(acum) - 1):
            term += f"(x - {x[i - 1]:.4f})"
        pol_text += " + " + term
    
    # Mostrar la tabla de diferencias divididas
    print("Tabla de diferencias divididas de Newton:")
    print(Tabla)
    
    # Mostrar el polinomio de interpolación
    print("Polinomio de interpolación:")
    print(pol_text)

    # Generar valores de x para graficar
    xpol = np.linspace(min(x), max(x), 1000)
    p = np.zeros_like(xpol)

    # Evaluar el polinomio para cada punto
    for i in range(len(pol)):
        p += pol[i] * xpol**(len(pol) - i - 1)

    # Graficar
    plt.figure()
    plt.plot(x, y, 'r*', label='Datos')
    plt.plot(xpol, p, 'b', label='Polinomio de Interpolación')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interpolación de Newton con Diferencias Divididas')
    plt.grid(True)
    
    # Save the plot as a PNG
    plt.savefig(png_filename, format='png')  # Save as PNG
    plt.close()

    # Plotting with Plotly (HTML for interactivity)
    fig = go.Figure()

    # Function plot
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=f'Datos', line=dict(color='blue')))

    # Mark the midpoints as they refine to the root
    fig.add_trace(go.Scatter(x=xpol, y=p, mode='lines', name="Polinomio de Interpolación", marker=dict(color='red', size=8)))

    fig.update_layout(title='Newton - Metodo de interpolacion',
                      xaxis_title='x', yaxis_title='y',
                      template="plotly_white")

    # Save as HTML file
    fig.write_html(html_filename)

    return {
        "polinomio": f"El polinomio es: {pol_text}",
        "png_path": png_filename,
        "html_path": html_filename
    }
