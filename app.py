from flask import Flask, render_template, request, send_file, url_for
from services.cap1.bisection_method import bisection_method
from services.cap1.false_position_method import false_position_method
from services.cap1.fixedpoint_method import fixedpoint_method
from services.cap1.multiple_roots_method import multiple_roots_method
from services.cap1.newton_method import newton_method
from services.cap1.secant_method import secant_method
from services.cap2.gauss_seidel_method import gauss_seidel_method
from services.cap2.jacobi_method import jacobi_method
from services.cap2.sor_method import sor_method
from services.cap3.lagrange_method import lagrange_method
from services.cap3.newton_interpolation import newton_interpolation_method
from services.cap3.spline_cubic_method import spline_cubic
from services.cap3.spline_lineal_method import spline_lineal
from services.cap3.vandermonde_method import vandermonde_method
import numpy as np
import os
from sympy import symbols, diff, sympify

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = 'static/imgs/bisection_method'

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/methods/bisection/', methods=['GET', 'POST'])
def bisection():
    if request.method == 'POST':
        # Get form data
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            Tol = float(request.form['Tol'])
            Niter = int(request.form['Niter'])
            Fun = request.form['Fun']
            error_type = request.form.get("error_type", "relative")  # Default to relative
            # Run bisection method
            result = bisection_method(a, b, Tol, Niter, Fun, error_type)
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
        
                return render_template("bisection.html", result=result["result"], 
                                iterations=result.get("iterations"),
                                png_path=png_url,
                                html_path=html_url
                )
        except Exception as e:
            return render_template("bisection.html", input_error=True)
        # Pass results to template
        return render_template("bisection.html", result=result, 
                               iterations=result.get("iterations"),
        )
    
    # GET request - show form
    return render_template('bisection.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/methods/false_position/', methods=['GET', 'POST'])
def false_position():
    if request.method == 'POST':
        # Get form data
        try:
            Xi = float(request.form['Xi'])
            Xs = float(request.form['Xs'])
            Tol = float(request.form['Tol'])
            Niter = int(request.form['Niter'])
            Fun = request.form['Fun']
            error_type = request.form.get("error_type", "relative")
            # Run false position method
            result = false_position_method(Xi, Xs, Tol, Niter, Fun, error_type)
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
        
                return render_template("false_position.html", result=result["result"], 
                                iterations=result.get("iterations"),
                                png_path=png_url,
                                html_path=html_url
                )
        except Exception as e:
            return render_template("false_position.html", input_error=True)

        # Pass results to template
        return render_template("false_position.html", result=result, 
                               iterations=result.get("iterations"),
        )
    
    # GET request - show form
    return render_template('false_position.html')

@app.route('/methods/fixed_point/', methods=['GET', 'POST'])
def fixed_point():
    if request.method == 'POST':
        # Get form data
        try:
            X0 = float(request.form['X0'])
            Tol = float(request.form['Tol'])
            Niter = int(request.form['Niter'])
            Fun = request.form['Fun']
            GFun = request.form['GFun']
            error_type = request.form.get("error_type", "relative")
            # Run fixed point method
            result = fixedpoint_method(X0, Tol, Niter, Fun, GFun, error_type)
            
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
        
                return render_template("fixed_point.html", result=result['result'], 
                                iterations=result.get("iterations"),
                                png_path=png_url,
                                html_path=html_url
                ) 
            # Pass results to template
        except Exception as e:
            return render_template("fixed_point.html", input_error=True)
        else:
            return render_template("fixed_point.html", result=result, 
                                   iterations=result.get("iterations"),
            )
    # GET request - show form
    return render_template('fixed_point.html')

@app.route('/methods/multiple_roots/', methods=['GET', 'POST'])
def multiple_roots():
    if request.method == 'POST':
        # Get form data
        try:
            X0 = float(request.form['X0'])
            Tol = float(request.form['Tol'])
            Niter = int(request.form['Niter'])
            Fun = request.form['Fun']
            Derivative1 = request.form['Der1']
            Derivative2 = request.form['Der2']
            error_type = request.form.get("error_type", "relative")
            # Run multiple roots method
            result = multiple_roots_method(X0, Tol, Niter, Fun, Derivative1, Derivative2, error_type)

            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
        
                return render_template("multiple_roots.html", result=result["result"], 
                                iterations=result.get("iterations"),
                                png_path=png_url,
                                html_path=html_url
                ) 
        except Exception as e:
            return render_template("multiple_roots.html", input_error=True)

        return render_template("multiple_roots.html", result=result, 
                               iterations=result.get("iterations"),
        )

    return render_template('multiple_roots.html')

@app.route('/methods/newton/', methods=['GET', 'POST'])
def newton():
    if request.method == "POST":
        try:
            x0 = float(request.form["X0"])
            Tol = float(request.form["Tol"])
            Niter = int(request.form["Niter"])
            Fun = request.form["Fun"]
            Der = request.form["Der"]
            error_type = request.form.get("error_type", "relative")

            # Call the Newton-Raphson method
            png_url = None
            html_url = None
            result = newton_method(x0, Tol, Niter, Fun, Der, error_type)
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
        
                return render_template("newton.html", result=result["result"], 
                                iterations=result.get("iterations"),
                                png_path=png_url,
                                html_path=html_url
                ) 
        except Exception as e:
            return render_template("newton.html", input_error=True)

            # Pass results to template
        return render_template("newton.html", result=result, 
                                iterations=result.get("iterations"),
        )
    return render_template("newton.html")

@app.route('/methods/secant/', methods=['GET', 'POST'])
def secant():
    if request.method == 'POST':
        try:
            # Get form data
            Xi = float(request.form['Xi'])
            Xs = float(request.form['Xs'])
            Tol = float(request.form['Tol'])
            Niter = int(request.form['Niter'])
            Fun = request.form['Fun']
            error_type = request.form.get("error_type", "relative")
            # Run false position method
            result = secant_method(Xi, Xs, Tol, Niter, Fun, error_type)
            # Ensure static file paths are correctly handled
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
        
                return render_template("secant.html", result=result["result"],
                                iterations=result.get("iterations"),
                                png_path=png_url,
                                html_path=html_url
                ) 
            # Pass results to template
        except Exception as e:
            return render_template("secant.html", input_error=True)

        return render_template("secant.html", result=result, 
                               iterations=result.get("iterations"),
        )
    # GET request - show form
    return render_template('secant.html')

@app.route('/cap1', methods=['GET'])
def cap1():
    return render_template('cap1.html')

@app.route('/cap2', methods=['GET'])
def cap2():
    return render_template('cap2.html')

@app.route('/cap3', methods=['GET'])
def cap3():
    return render_template('cap3.html')

@app.route('/derivative/', methods=['GET', 'POST'])
def derivative():
    result = None
    if request.method == 'POST':
        function_input = request.form.get('function')
        variable_input = request.form.get('variable', 'x')
        
        try:
            variable = symbols(variable_input)
            function = sympify(function_input)
            derivative = diff(function, variable)
            
            result = {
                'original_function': function_input,
                'variable': variable_input,
                'derivative': str(derivative)
            }
        except Exception as e:
            result = {'error': f'Error procesando la función: {e}'}
    
    return render_template('derivative.html', result=result)


@app.route('/methods/gauss_seidel/', methods=['GET', 'POST'])
def gauss_seidel():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            A = np.array([[float(num) for num in row.split(',')] for row in request.form['matrixA'].split(';')])
            b = np.array([float(num) for num in request.form['vectorB'].split(',')])
            x0 = np.array([float(num) for num in request.form['x0'].split(',')])
            tol = float(request.form['tol'])
            niter = int(request.form['niter'])
            et = request.form['error_type']

            # Llamar al método de Gauss-Seidel
            result = gauss_seidel_method(A, b, x0, tol, niter, et)

            # Determinar si el método converge o no, basado en el radio espectral
            Re = result.get("Re")
            convergence_message = "El método converge." if abs(Re) < 1 else "El método no converge."

            # Generar las URL de los gráficos principales (error de convergencia)
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Generar las URL de los gráficos para el sistema de ecuaciones (solo para 2x2)
            system_plot_html_url = None
            system_plot_png_url = None
            if result.get("system_plot_html") and result.get("system_plot_png"):
                system_plot_html_url = url_for("static", filename=result["system_plot_html"].replace("static/", ""))
                system_plot_png_url = url_for("static", filename=result["system_plot_png"].replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "gauss_seidel.html", 
                result=result["result"], 
                iterations=result.get("iterations"),
                png_path=png_url,
                html_path=html_url,
                system_plot_html=system_plot_html_url,
                system_plot_png=system_plot_png_url,
                Re=Re,
                convergence_message=convergence_message
            )
        except Exception as e:
            return render_template("gauss_seidel.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('gauss_seidel.html')


@app.route('/methods/jacobi/', methods=['GET', 'POST'])
def jacobi():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            A = np.array([[float(num) for num in row.split(',')] for row in request.form['matrixA'].split(';')])
            b = np.array([float(num) for num in request.form['vectorB'].split(',')])
            x0 = np.array([float(num) for num in request.form['x0'].split(',')])
            tol = float(request.form['tol'])
            niter = int(request.form['niter'])
            et = request.form['error_type']

            # Llamar al método de Jacobi
            result = jacobi_method(A, b, x0, tol, niter, et)

            # Obtener el radio espectral y la convergencia
            Re = result.get("Re")  # Asumiendo que el método jacobi_method devuelve el radio espectral
            convergence_message = "El método converge." if abs(Re) < 1 else "El método no converge."

            # Generar las URL de los gráficos principales (error de convergencia)
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Generar las URL de los gráficos para el sistema de ecuaciones (solo para 2x2)
            system_plot_html_url = None
            system_plot_png_url = None
            if result.get("system_plot_html") and result.get("system_plot_png"):
                system_plot_html_url = url_for("static", filename=result["system_plot_html"].replace("static/", ""))
                system_plot_png_url = url_for("static", filename=result["system_plot_png"].replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "jacobi.html", 
                result=result["result"], 
                iterations=result.get("iterations"),
                png_path=png_url,
                html_path=html_url,
                system_plot_html=system_plot_html_url,
                system_plot_png=system_plot_png_url,
                Re=Re,
                convergence_message=convergence_message
            )
        except Exception as e:
            return render_template("jacobi.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('jacobi.html')

@app.route('/methods/sor/', methods=['GET', 'POST'])
def sor():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            A = np.array([[float(num) for num in row.split(',')] for row in request.form['matrixA'].split(';')])
            b = np.array([float(num) for num in request.form['vectorB'].split(',')])
            x0 = np.array([float(num) for num in request.form['x0'].split(',')])
            tol = float(request.form['tol'])
            niter = int(request.form['niter'])
            et = request.form['error_type']  # Tipo de error
            w = float(request.form['w'])  # Valor de omega para SOR

            # Llamar al método de SOR
            result = sor_method(A, b, x0, tol, niter, w, et)

            # Obtener el radio espectral y la convergencia
            Re = result.get("Re")  # Asumiendo que el método sor_method devuelve el radio espectral
            convergence_message = "El método converge." if abs(Re) < 1 else "El método no converge."

            # Generar las URL de los gráficos
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Generar las URL de los gráficos para el sistema de ecuaciones (solo para 2x2)
            system_plot_html_url = None
            system_plot_png_url = None
            if result.get("system_plot_html") and result.get("system_plot_png"):
                system_plot_html_url = url_for("static", filename=result["system_plot_html"].replace("static/", ""))
                system_plot_png_url = url_for("static", filename=result["system_plot_png"].replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "sor.html", 
                result=result["result"], 
                iterations=result.get("iterations"),
                png_path=png_url,
                html_path=html_url,
                system_plot_html=system_plot_html_url,
                system_plot_png=system_plot_png_url,
                Re=Re,
                convergence_message=convergence_message
            )
        except Exception as e:
            return render_template("sor.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('sor.html')

@app.route('/methods/vandermonde/', methods=['GET', 'POST'])
def vandermonde():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            if request.form['vectorX'] and request.form['vectorY']:
                x = np.array([float(num) for num in request.form['vectorX'].split(',')])
                y = np.array([float(num) for num in request.form['vectorY'].split(',')])
            else:
                return render_template("vandermonde.html", input_error=True, e="Los vectores X e Y no pueden estar vacíos.")

            # Llamar al método de Vandermonde
            result = vandermonde_method(x, y)
            if result.get("error"):
                return render_template("vandermonde.html", input_error=True, e=result["error"])
            # Obtenemos 
            polinomio = result.get("polinomio") 
            # Generar las URL de los gráficos principales (error de convergencia)
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "vandermonde.html",
                result=result,
                png_path=png_url,
                html_path=html_url,
                polinomio=polinomio
            )
        except Exception as e:
            return render_template("vandermonde.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('vandermonde.html')

@app.route('/methods/newton_int/', methods=['GET', 'POST'])
def newton_int():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            if request.form['vectorX'] and request.form['vectorY']:
                x = np.array([float(num) for num in request.form['vectorX'].split(',')])
                y = np.array([float(num) for num in request.form['vectorY'].split(',')])
            else:
                return render_template("newton_int.html", input_error=True, e="Los vectores X e Y no pueden estar vacíos.")

            # Llamar al método de Vandermonde
            result = newton_interpolation_method(x, y)
            if result.get("error"):
                return render_template("newton_int.html", input_error=True, e=result["error"])
            # Obtenemos 
            polinomio = result.get("polinomio") 
            # Generar las URL de los gráficos principales (error de convergencia)
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "newton_int.html",
                result=result,
                png_path=png_url,
                html_path=html_url,
                polinomio=polinomio
            )
        except Exception as e:
            return render_template("newton_int.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('newton_int.html')

@app.route('/methods/lagrange/', methods=['GET', 'POST'])
def lagrange():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            if request.form['vectorX'] and request.form['vectorY']:
                x = np.array([float(num) for num in request.form['vectorX'].split(',')])
                y = np.array([float(num) for num in request.form['vectorY'].split(',')])
            else:
                return render_template("lagrange.html", input_error=True, e="Los vectores X e Y no pueden estar vacíos.")
            
            # Llamar al método de Vandermonde
            result = lagrange_method(x, y)
            if result.get("error"):
                return render_template("lagrange.html", input_error=True, e=result["error"])
            # Obtenemos 
            polinomio = result.get("polinomio") 
            # Generar las URL de los gráficos principales (error de convergencia)
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "lagrange.html",
                result=result,
                png_path=png_url,
                html_path=html_url,
                polinomio=polinomio
            )
        except Exception as e:
            return render_template("lagrange.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('lagrange.html')

@app.route('/methods/spline/', methods=['GET', 'POST'])
def spline():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            if request.form['vectorX'] and request.form['vectorY']:
                x = np.array([float(num) for num in request.form['vectorX'].split(',')])
                y = np.array([float(num) for num in request.form['vectorY'].split(',')])
            else:
                return render_template("spline.html", input_error=True, e="Los vectores X e Y no pueden estar vacíos.")
            
            if request.form.get("spline_type")== "Lineal":
                result = spline_lineal(x, y)
            else:
                result = spline_cubic(x, y)
            if result.get("error"):
                return render_template("spline.html", input_error=True, e=result["error"])
            # Obtenemos 
            polinomio = result.get("polinomio") 
            # Generar las URL de los gráficos principales
            png_url = None
            html_url = None
            if result.get("png_path") and result.get("html_path"):
                png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
                html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            # Renderizar la plantilla con todos los datos
            return render_template(
                "spline.html",
                result=result,
                png_path=png_url,
                html_path=html_url,
                polinomio=polinomio
            )
        except Exception as e:
            return render_template("spline.html", input_error=True)
    # En caso de método GET, solo renderizar la página inicial
    return render_template('spline.html')


if __name__ == '__main__':
    app.run(debug=True)
