import numpy as np
import pandas as pd

def gauss_seidel_interactive():
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
    
    print("Seleccione el tipo de error (1 para Error Absoluto, 2 para Error Relativo):")
    et = 'Error Absoluto' if input() == '1' else 'Error Relativo'
    
    x0 = np.array(x0, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    c = 0
    error = tol + 1
    E = []
    xn = []
    N = []
    
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
    
    # Verificar si alguna fila de A tiene una solución directa
    x = x0
    initial_check = False
    for i in range(n):
        if np.isclose(np.dot(A[i], x), b[i]):
            initial_check = True
            print(f"{x} es una solución directa del sistema.")
            break
    
    if not initial_check:
        # Iteraciones de Gauss-Seidel
        while error > tol and c < niter:
            x1 = T @ x0 + C
            
            # Calcular error
            if et == 'Error Absoluto':
                current_error = np.linalg.norm(x1 - x0, ord=np.inf)
            else:
                current_error = np.linalg.norm((x1 - x0) / x1, ord=np.inf)
            
            E.append(current_error)
            xn.append(x1.copy())
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
        table = pd.DataFrame({'Iteración': N, 'Aproximación (xn)': xn, 'Error': E})
        print("\nTabla de resultados de Gauss-Seidel:")
        print(table.to_string(index=False))
        
        # Mostrar radio espectral y convergencia
        print(f"\nRadio espectral de T = {Re}")
        print(converge_msg)
        print(result_msg)
    else:
        print("El sistema tiene una solución directa, no se requieren iteraciones.")

gauss_seidel_interactive()
