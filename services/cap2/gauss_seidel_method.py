import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def gauss_seidel(A, b, x0, tol, niter, et, png_filename="static/imgs/gauss_seidel_method/gauss_seidel_plot.png", html_filename="static/imgs/gauss_seidel_method/gauss_seidel_plot.html"):
    # Asegurar que las carpetas existen
    os.makedirs(os.path.dirname(png_filename), exist_ok=True)
    
    n = len(b)
    c = 0
    error = tol + 1
    iteraciones = []
    aproximaciones = []
    errores = []
    
    # Descomposición de A
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    
    # Preparar matrices para iteración
    T = np.linalg.inv(D - L) @ U
    C = np.linalg.inv(D - L) @ b
    
    # Calcular el radio espectral
    Re = max(abs(np.linalg.eigvals(T)))
    converge_msg = "El método converge" if Re < 1 else "El método no converge"
    
    # Iteraciones de Gauss-Seidel
    while error > tol and c < niter:
        x1 = T @ x0 + C
        
        # Calcular error
        if et == 'Error Absoluto':
            current_error = np.linalg.norm(x1 - x0, ord=np.inf)
        else:
            current_error = np.linalg.norm((x1 - x0) / x1, ord=np.inf)
        
        # Guardar datos de la iteración
        iteraciones.append(c)
        aproximaciones.append(x1.copy())
        errores.append(current_error)
        
        error = current_error
        x0 = x1
        c += 1
    
    # Verificar resultado final
    if error < tol:
        result_msg = f"{x1} es una aproximación de la solución con una tolerancia de {tol}\n"
    else:
        result_msg = f"Fracaso en {niter} iteraciones\n"
    
    # Crear tabla de resultados
    resultados = pd.DataFrame({
        "Iteración": iteraciones,
        "Aproximación (xn)": aproximaciones,
        "Error": errores
    })
    
    # Gráfico PNG con Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(iteraciones, errores, label='Error en cada iteración', color='blue')
    plt.xlabel('Iteraciones')
    plt.ylabel('Error')
    plt.title('Método de Gauss-Seidel - Convergencia del Error')
    plt.grid(True)
    plt.savefig(png_filename, format='png')  # Guardar como PNG
    plt.close()

    # Gráfico interactivo con Plotly (HTML)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=iteraciones, y=errores, mode='lines+markers', name='Error'))
    fig.update_layout(
        title='Gauss-Seidel - Convergencia del Error',
        xaxis_title='Iteraciones',
        yaxis_title='Error',
        template='plotly_white'
    )
    fig.write_html(html_filename)

    # Si el sistema es de 2 ecuaciones, generar la gráfica de las ecuaciones
    if n == 2:
        _plot_system(A, b, x1)
    
    # Devolver el resultado, tabla y las rutas de los archivos generados
    return {
        "result": result_msg,
        "iterations": resultados.to_dict(orient='records'),
        "png_path": png_filename,
        "html_path": html_filename,
        "converge_msg": converge_msg,
        "Re": Re
    }

def _plot_system(A, b, solution):
    # Gráfica para sistemas de dos ecuaciones
    x = np.linspace(-10, 10, 400)
    y1 = (b[0] - A[0][0] * x) / A[0][1]
    y2 = (b[1] - A[1][0] * x) / A[1][1]
    
    plt.figure(figsize=(6, 6))
    plt.plot(x, y1, label=r'$a_{11}x + a_{12}y = b_1$', color='blue')
    plt.plot(x, y2, label=r'$a_{21}x + a_{22}y = b_2$', color='green')
    plt.plot(solution[0], solution[1], 'ro', label="Solución")
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Sistema de Ecuaciones - Gauss-Seidel')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

# Ejemplo de uso:
A = np.array([[4, -1], [-1, 4]], dtype=float)
b = np.array([15, 10], dtype=float)
x0 = np.array([0, 0], dtype=float)
tol = 1e-6
niter = 25
et = 'Error Absoluto'

result = gauss_seidel(A, b, x0, tol, niter, et)

# Mostrar resultados
print(result["result"])
print(pd.DataFrame(result["iterations"]))
print(f"Radio espectral: {result['Re']}")
print(result["converge_msg"])
