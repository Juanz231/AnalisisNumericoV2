import numpy as np
import pandas as pd

def sor():
    # Solicitar los datos del usuario
    print("Ingrese el vector inicial x0 (por ejemplo, 0 0 para [0, 0]):")
    x0 = list(map(float, input().split()))

    print("Ingrese la matriz A (por ejemplo, 4 -1; -2 4 para [[4, -1], [-2, 4]]):")
    A = []
    for i in range(len(x0)):
        row = list(map(float, input(f"Fila {i+1}: ").split()))
        A.append(row)

    print("Ingrese el vector independiente b (por ejemplo, 3 1 para [3, 1]):")
    b = list(map(float, input().split()))

    print("Ingrese la tolerancia:")
    tol = float(input())

    print("Ingrese el número máximo de iteraciones:")
    niter = int(input())

    print("Ingrese el valor de omega (w) entre 0 y 2:")
    w = float(input())

    print("Seleccione el tipo de error (1 para Error Absoluto, 2 para Error Relativo):")
    et = 'Error Absoluto' if input() == '1' else 'Error Relativo'

    x0 = np.array(x0, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
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

    # Mostrar tabla de iteraciones
    table = pd.DataFrame({'Iteración': N, 'Aproximación (xn)': xi, 'Error': E})
    print("\nTabla de resultados de SOR:")
    print(table.to_string(index=False))

    # Mostrar radio espectral y convergencia
    print(f"\nRadio espectral de T = {Re}")
    print(converge_msg)
    print(result_msg)

    # Guardar los resultados en un archivo CSV
    table_file_path = 'tabla_sor.csv'
    table.to_csv(table_file_path, index=False)
    print(f"Los resultados han sido guardados en {table_file_path}")

sor()
