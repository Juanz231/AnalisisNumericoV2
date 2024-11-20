import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def lagrange_method(vectorx, vectory,png_filename: str = "static/imgs/lagrange_method/lagrange_plot.png", html_filename: str = "static/imgs/lagrange_method/lagrange_plot.html"):
    if len(vectorx) != len(vectory):
        return {"error": "Los vectores x e y deben tener la misma longitud."}
    #Verificar que no hayan mas de 8 datos
    if len(vectorx)>8:
        return {"error": "El numero maximo de datos es 8"}
    if len(np.unique(vectorx)) != len(vectorx):
        return {"error": "El vector X no puede contener valores duplicados."}
    xv = np.array(vectorx, dtype=float)
    yv = np.array(vectory, dtype=float)
    n = len(xv)
    
    # Crear la tabla para almacenar los términos del polinomio
    Tabla = np.zeros((n, n))
    
    for i in range(n):
        Li = [1]
        den = 1
        for j in range(n):
            if j != i:
                # Construir el término (x - xv[j])
                paux = [1, -xv[j]]
                # Multiplicar polinomios
                Li = np.convolve(Li, paux)
                # Calcular el denominador
                den *= (xv[i] - xv[j])
        
        # Agregar el término correspondiente a la tabla
        Tabla[i, :] = yv[i] * np.array(Li) / den
    
    # Sumar los términos para obtener el polinomio final
    pol = np.sum(Tabla, axis=0)
    
    pol_r = pol[::-1]
    n_pol = len(pol)
    polynomial_terms = []
    for i in range(n_pol):
        if i == 0:
            if pol_r [i] < 0:
                polynomial_terms.append(f"-{abs(pol_r [i])}")
            else:
                polynomial_terms.append(f"+{abs(pol_r [i])}")
        else:
            polynomial_terms.append(f"+{pol_r [i]}*x^{i} ")

    # Revertir los términos para que el polinomio esté en orden canónico
    polynomial_terms.reverse()
    pol_text = "".join(polynomial_terms).replace("+-", "-")

    # Mostrar el polinomio
    #print("Polinomio de Lagrange (coeficientes):")
    #print(pol)
    
    # Crear un conjunto de puntos para graficar el polinomio
    x_vals = np.linspace(min(xv), max(xv), 1000)
    y_vals = np.polyval(pol, x_vals)
    
    # Graficar el polinomio resultante
    plt.figure()
    plt.plot(x_vals, y_vals, 'r', label='Polinomio de Lagrange')
    plt.plot(xv, yv, 'bo', label='Puntos de entrada')  # Puntos en azul
    plt.title('Polinomio de Lagrange')
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
    fig.add_trace(go.Scatter(x=xv, y=yv, mode='markers', name='Puntos de entrada', line=dict(color='blue')))
    
    # Mark the midpoints as they refine to the root
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Polinomio de Lagrange", marker=dict(color='red', size=8)))


    fig.update_layout(title='Lagrange - Metodo de interpolacion',
                      xaxis_title='x', yaxis_title='y',
                      template="plotly_white")

    # Save as HTML file
    fig.write_html(html_filename)
    
    return {
        "polinomio": f"El polinomio es: {pol_text}",
        "png_path": png_filename,
        "html_path": html_filename
    }
