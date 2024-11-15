import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def sor(A, b, x0, tol, niter, w, et, png_filename="static/imgs/sor_method/sor_plot.png", html_filename="static/imgs/sor_method/sor_plot.html"):
    # Asegurar que las carpetas existen
    os.makedirs(os.path.dirname(png_filename), exist_ok=True)

    n = len(b)
    c = 0
    error = tol + 1
    E = []
    xi = []
    N = []

    # Descomposición de A
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)

    # Preparar matrices para iteración
    T = np.linalg.inv(D - w * L) @ ((1 - w) * D + w * U)
    C = w * np.linalg.inv(D - w * L) @ b

    # Calcular el radio espectral
    eigenvalues = np.linalg.eigvals(T)
    Re = max(abs(eigenvalues))
    converge_msg = "El método converge" if Re < 1 else "El método no converge"
    
    # Iteraciones de SOR
    while error > tol and c < niter:
        x1 = T @ x0 + C

        if et == 'Error Absoluto':
            current_error = np.linalg.norm(x1 - x0, ord=np.inf)
        else:
            current_error = np.linalg.norm((x1 - x0) / x1, ord=np.inf)

        E.append(current_error)
        xi.append(x1.copy())
        N.append(c + 1)

        error = current_error
        x0 = x1
        c += 1

    # Resultado final
    if error < tol:
        result_msg = f"{x1} es una aproximación de la solución con una tolerancia de {tol}\n"
    else:
        result_msg = f"Fracaso en {niter} iteraciones\n"

    # Crear la tabla de resultados
    table = pd.DataFrame({'Iteración': N, 'Aproximación (xn)': xi, 'Error': E})

    # Generar gráficos con Matplotlib (PNG)
    plt.figure(figsize=(10, 6))
    plt.plot(N, E, label='Error en cada iteración', color='blue')
    plt.xlabel('Iteraciones')
    plt.ylabel('Error')
    plt.title('Método de SOR - Convergencia del Error')
    plt.grid(True)
    plt.savefig(png_filename, format='png')  # Guardar como PNG
    plt.close()

    # Gráfico interactivo con Plotly (HTML)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=N, y=E, mode='lines+markers', name='Error'))
    fig.update_layout(
        title='SOR - Convergencia del Error',
        xaxis_title='Iteraciones',
        yaxis_title='Error',
        template='plotly_white'
    )
    fig.write_html(html_filename)

    # Si el sistema es de 2 ecuaciones, visualizar la gráfica de las ecuaciones
    if n == 2:
        _plot_system(A, b, x1)

    # Devolver el resultado, tabla y las rutas de los archivos generados
    return {
        "result": result_msg,
        "iterations": table.to_dict(orient='records'),
        "png_path": png_filename,
        "html_path": html_filename,
        "converge_msg": converge_msg,
        "Re": Re
    }

def _plot_system(A, b, solution):
    """
    Genera la gráfica de un sistema de dos ecuaciones y su solución.
    A = [[a11, a12], [a21, a22]]
    b = [b1, b2]
    solution = [x1, x2] es la solución del sistema
    """
    # Ecuaciones
    x = np.linspace(-10, 10, 400)
    y1 = (b[0] - A[0][0] * x) / A[0][1]
    y2 = (b[1] - A[1][0] * x) / A[1][1]
    
    # Graficar las líneas de las ecuaciones
    plt.figure(figsize=(6, 6))
    plt.plot(x, y1, label=r'$a_{11}x + a_{12}y = b_1$', color='blue')
    plt.plot(x, y2, label=r'$a_{21}x + a_{22}y = b_2$', color='green')
    
    # Graficar la solución
    plt.plot(solution[0], solution[1], 'ro', label="Solución")
    
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gráfica del Sistema de Ecuaciones')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

# Ejemplo de uso de la función:
A = np.array([[4, -1], [-1, 4]], dtype=float)
b = np.array([15, 10], dtype=float)
x0 = np.array([0, 0], dtype=float)
tol = 1e-6
niter = 25
w = 1.25
et = 'Error Absoluto'

# Llamada a la función
result = sor(A, b, x0, tol, niter, w, et)

# Mostrar resultados en consola
print(result["result"])
print("\nTabla de iteraciones:")
print(pd.DataFrame(result["iterations"]).to_string(index=False))
print(f"\nRadio espectral de T = {result['Re']}")
print(result["converge_msg"])
