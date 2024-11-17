import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re


def false_position_method(Xi: float, Xs: float, Tol: float, Niter: int, Fun: str, error_type: str = "absolute", png_filename: str = "static/imgs/false_position_method/false_position_plot.png", html_filename: str = "static/imgs/false_position_method/false_position_plot.html"):
    # Lists to store iteration data
    iteraciones = []
    xi_list = []
    xs_list = []
    xm_list = []
    f_xm_list = []
    error_list = []
    try: 
        # Initial evaluation of f(Xi) and f(Xs)
        x = Xi
        f_xi = eval(Fun)
        x = Xs
        f_xs = eval(Fun)
        
        # Check if initial values are roots
        if f_xi == 0:
            return {"root": Xi, "message": f"{Xi} es raíz de f(x)"}
        elif f_xs == 0:
            return {"root": Xs, "message": f"{Xs} es raíz de f(x)"}
        elif f_xi * f_xs > 0:
            return {"message": "El intervalo inicial no encierra una raíz (f(Xi) * f(Xs) > 0)"}
        
        # Initial midpoint
        Xm = Xi - (f_xi * (Xs - Xi)) / (f_xs - f_xi)
        x = Xm
        f_xm = eval(Fun)
        error = 1
        # Store initial data for the first iteration
        iteraciones.append(0)
        xi_list.append(Xi)
        xs_list.append(Xs)
        xm_list.append(Xm)
        f_xm_list.append(f_xm)
        error_list.append("N/A")  # No error on first iteration
        
        for c in range(1, Niter + 1):
            # Update interval based on f(Xi) and f(Xm) signs
            if f_xi * f_xm < 0:
                Xs = Xm
                f_xs = f_xm
            else:
                Xi = Xm
                f_xi = f_xm

            # Calculate new Xm
            Xm_new = Xi - (f_xi * (Xs - Xi)) / (f_xs - f_xi)

            # Calculate error
            if error_type == "absolute":
                error = abs(Xm_new - Xm)
            else:
                error = abs(Xm_new - Xm) / abs(Xm_new)

            # Update for next iteration
            Xm = Xm_new
            x = Xm
            f_xm = eval(Fun)

            # Store current iteration data
            iteraciones.append(c)
            xi_list.append(Xi)
            xs_list.append(Xs)
            xm_list.append(Xm)
            f_xm_list.append(f_xm)
            error_list.append(error)

            # Check stopping criteria
            if error < Tol:
                result = {"root": Xm, "message": f"{Xm} es una aproximación de una raíz de f(x) con tolerancia {Tol} en {c} iteraciones"}
                break
            else:
                result = {"message": f"Fracaso en {Niter} iteraciones"}


        # Store results in a DataFrame for output
        resultados = pd.DataFrame({
            'Iteración': iteraciones,
            'Xi': xi_list,
            'Xs': xs_list,
            'xm': xm_list,
            'f(Xm)': f_xm_list,
            'E (relativo)': error_list
        })
        print(resultados)
        # Plotting with Matplotlib (PNG)
        x_vals = np.linspace(Xi - 10, Xs + 10, 1000)

        y_vals = []
        for x in x_vals:
            safe_fun = re.sub(r'\bx\b', f'({x})', Fun)  # Replace standalone 'x'
            y_vals.append(eval(safe_fun, {"np": np}))  # Evaluate the expression    
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label=f'f(x) = {Fun}', color='blue')
        plt.axhline(0, color='black', linewidth=0.5)

        # Mark each midpoint as it refines to the root
        for i, xm in enumerate(xm_list):
            plt.plot(xm, f_xm_list[i], 'ro' if i == len(xm_list) - 1 else 'go', 
                    label="Aproximación" if i == 0 else "")
        
        # Highlight the final approximation/root
        plt.plot(xm_list[-1], f_xm_list[-1], 'ro', label="Aproximación Final")

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Regla falsa - Método de Aproximación de Raíces')
        plt.legend()
        plt.grid(True)
        
        # Save the plot as a PNG
        plt.savefig(png_filename, format='png')  # Save as PNG
        plt.close()

        # Plotting with Plotly (HTML for interactivity)
        fig = go.Figure()

        # Function plot
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'f(x) = {Fun}', line=dict(color='blue')))
        
        # Mark the midpoints as they refine to the root
        fig.add_trace(go.Scatter(x=xm_list, y=f_xm_list, mode='markers+lines', name="Aproximaciones", marker=dict(color='red', size=8)))

        # Final approximation/root
        fig.add_trace(go.Scatter(x=[xm_list[-1]], y=[f_xm_list[-1]], mode='markers', name="Aproximación Final", marker=dict(color='green', size=10)))

        fig.update_layout(title='Bisección - Método de Aproximación de Raíces',
                        xaxis_title='x', yaxis_title='f(x)',
                        template="plotly_white")

        # Save as HTML file
        fig.write_html(html_filename)
        print(resultados)
        # Return the result and paths to the saved files
    except Exception as e:
        return {"message": str(e)}
    else:
        return {
            "result": result,
            "iterations": resultados.to_dict(orient='records'),
            "png_path": png_filename,
            "html_path": html_filename
        }
