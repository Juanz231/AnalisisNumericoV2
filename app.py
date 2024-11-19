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
            return render_template("bisection.html", result={"message": "Ingrese todos los valores y bien parcerito"})
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
            return render_template("false_position.html", result={"message": "Ingrese todos los valores y bien parcerito"})

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
            return render_template("fixed_point.html", result={"message": "Ingrese todos los valores y bien parcerito"})
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
            return render_template("multiple_roots.html", result={"message": "Ingrese todos los valores y bien parcerito"})

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
            return render_template("newton.html", result={"message": "Ingrese todos los valores y bien parcerito"})

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
            return render_template("secant.html", result={"message": "Ingrese todos los valores y bien parcerito"})

        return render_template("secant.html", result=result, 
                               iterations=result.get("iterations"),
        )
    # GET request - show form
    return render_template('secant.html')

@app.route('/derivative/', methods=['GET', 'POST'])
def derivative():
    if request.method == 'POST':
        try:
            x = symbols('x')  # Define the variable
            user_function = request.form['function']
            parsed_function = sympify(user_function)  # Parse the input into a sympy expression
            derivative = diff(parsed_function, x)  # Compute the derivative
            return f"The derivative of {user_function} is: {derivative}"
        except Exception as e:
            return f"Error: {e}"
    return render_template('derivative.html')

@app.route('/methods/gauss_seidel/', methods=['GET', 'POST'])
def gauss_seidel():
    if request.method == 'POST':
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
        convergence_message = "The method converges." if abs(Re) < 1 else "The method does not converge."

        # Generar las URL de los gráficos
        if result.get("png_path") and result.get("html_path"):
            png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
            html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            return render_template("gauss_seidel.html", result=result["result"], 
                                   iterations=result.get("iterations"),
                                   png_path=png_url,
                                   html_path=html_url,
                                   Re=Re,
                                   convergence_message=convergence_message  # Añadir el mensaje de convergencia
            ) 
        # Si no se generan gráficos, solo pasar resultados
        return render_template("gauss_seidel.html", result=result["result"], 
                               iterations=result.get("iterations"),
                               Re=Re,
                               convergence_message=convergence_message,  # Añadir el mensaje de convergencia
        )

    return render_template('gauss_seidel.html')


@app.route('/methods/jacobi/', methods=['GET', 'POST'])
def jacobi():
    if request.method == 'POST':
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

        # Generar las URL de los gráficos
        if result.get("png_path") and result.get("html_path"):
            png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
            html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            return render_template("jacobi.html", result=result["result"], 
                                   iterations=result.get("iterations"),
                                   png_path=png_url,
                                   html_path=html_url,
                                   Re=Re,
                                   convergence_message=convergence_message
            ) 

        # Si no se generan gráficos, solo pasar resultados
        return render_template("jacobi.html", result=result["result"], 
                               iterations=result.get("iterations"),
                               Re=Re,
                               convergence_message=convergence_message
        )

    return render_template('jacobi.html')


@app.route('/methods/sor/', methods=['GET', 'POST'])
def sor():
    if request.method == 'POST':
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
        
        Re = result.get("Re") 
        # Generar las URL de los gráficos
        if result.get("png_path") and result.get("html_path"):
            png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
            html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))

            return render_template("sor.html", result=result["result"], 
                                   iterations=result.get("iterations"),
                                   png_path=png_url,
                                   html_path=html_url,
                                   converge_msg=result.get("converge_msg"),
                                   Re=result.get("Re")
            ) 
        # Si no se generan gráficos, solo pasar resultados
        return render_template("sor.html", result=result["result"], 
                               iterations=result.get("iterations"),
                               converge_msg=result.get("converge_msg"),
                               Re=Re,
        )

    return render_template('sor.html')


if __name__ == '__main__':
    app.run(debug=True)
