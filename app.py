from flask import Flask, render_template, request, send_file, url_for
from services.cap1.bisection_method import bisection_method
from services.cap1.false_position_method import false_position_method
from services.cap1.fixedpoint_method import fixedpoint_method
from services.cap1.multiple_roots_method import multiple_roots_method
from services.cap1.newton_method import newton_method
from services.cap1.secant_method import secant_method
import os

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = 'static/imgs/bisection_method'

@app.route('/methods/bisection/', methods=['GET', 'POST'])
def bisection():
    if request.method == 'POST':
        # Get form data
        a = float(request.form['a'])
        b = float(request.form['b'])
        Tol = float(request.form['Tol'])
        Niter = int(request.form['Niter'])
        Fun = request.form['Fun']

        # Run bisection method
        result = bisection_method(a, b, Tol, Niter, Fun)
        print(result['png_path'], 'and', result['html_path'])

        # Ensure static file paths are correctly handled
        png_url = url_for('static', filename=result['png_path'].replace('static/', ''))
        html_url = url_for('static', filename=result['html_path'].replace('static/', ''))
        # Return results and paths for displaying in HTML
        return render_template(
            'bisection.html', 
            result=result['result'],
            iterations=result['iterations'],
            png_path=png_url,# Accessible path for HTML
            html_path=html_url  # Accessible path for HTML
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
        Xi = float(request.form['Xi'])
        Xs = float(request.form['Xs'])
        Tol = float(request.form['Tol'])
        Niter = int(request.form['Niter'])
        Fun = request.form['Fun']
        # Run false position method
        result = false_position_method(Xi, Xs, Tol, Niter, Fun)
        print(result['png_path'], 'and', result['html_path'])
        # Ensure static file paths are correctly handled
        png_url = url_for('static', filename=result['png_path'].replace('static/', ''))
        html_url = url_for('static', filename=result['html_path'].replace('static/', ''))
        # Return results and paths for displaying in HTML
        return render_template(
            'false_position.html', 
            result=result['result'],
            iterations=result['iterations'],
            png_path=png_url,# Accessible path for HTML
            html_path=html_url  # Accessible path for HTML
        )
    
    # GET request - show form
    return render_template('false_position.html')

@app.route('/methods/fixed_point/', methods=['GET', 'POST'])
def fixed_point():
    if request.method == 'POST':
        # Get form data
        X0 = float(request.form['X0'])
        Tol = float(request.form['Tol'])
        Niter = int(request.form['Niter'])
        Fun = request.form['Fun']
        GFun = request.form['GFun']
        # Run fixed point method
        result = fixedpoint_method(X0, Tol, Niter, Fun, GFun)
        print(result['png_path'], 'and', result['html_path'])
        # Ensure static file paths are correctly handled
        png_url = url_for('static', filename=result['png_path'].replace('static/', ''))
        html_url = url_for('static', filename=result['html_path'].replace('static/', ''))
        # Return results and paths for displaying in HTML
        return render_template(
            'fixed_point.html', 
            result=result['result'],
            iterations=result['iterations'],
            png_path=png_url,# Accessible path for HTML
            html_path=html_url  # Accessible path for HTML
        )
    # GET request - show form
    return render_template('fixed_point.html')

@app.route('/methods/multiple_roots/', methods=['GET', 'POST'])
def multiple_roots():
    if request.method == 'POST':
        # Get form data
        X0 = float(request.form['X0'])
        Tol = float(request.form['Tol'])
        Niter = int(request.form['Niter'])
        Fun = request.form['Fun']
        Derivative1 = request.form['Der1']
        Derivative2 = request.form['Der2']
        # Run multiple roots method
        result = multiple_roots_method(X0, Tol, Niter, Fun, Derivative1, Derivative2)
        print(result['png_path'], 'and', result['html_path'])
        # Ensure static file paths are correctly handled
        png_url = url_for('static', filename=result['png_path'].replace('static/', ''))
        html_url = url_for('static', filename=result['html_path'].replace('static/', ''))
        # Return results and paths for displaying in HTML
        return render_template(
            'multiple_roots.html', 
            result=result['result'],
            iterations=result['iterations'],
            png_path=png_url,# Accessible path for HTML
            html_path=html_url  # Accessible path for HTML
        )

    return render_template('multiple_roots.html')


@app.route('/methods/newton/', methods=['GET', 'POST'])
def newton():
    if request.method == "POST":
        x0 = float(request.form["X0"])
        Tol = float(request.form["Tol"])
        Niter = int(request.form["Niter"])
        Fun = request.form["Fun"]
        Der = request.form["Der"]

        # Call the Newton-Raphson method
        png_url = None
        html_url = None
        result = newton_method(
            x0, Tol, Niter, Fun, Der,
            png_filename="static/imgs/newton_method/newton_plot.png",
            html_filename="static/imgs/newton_method/newton_plot.html"
        )

        if result.get("png_path") and result.get("html_path"):
            png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
            html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
    
            return render_template("newton.html", result=result, 
                               iterations=result.get("iterations"),
                               png_path=png_url,
                               html_path=html_url
            ) 
        # Pass results to template
        return render_template("newton.html", result=result, 
                               iterations=result.get("iterations"),
        )
    return render_template("newton.html")

@app.route('/methods/secant/', methods=['GET', 'POST'])
def secant():
    if request.method == 'POST':
        # Get form data
        Xi = float(request.form['Xi'])
        Xs = float(request.form['Xs'])
        Tol = float(request.form['Tol'])
        Niter = int(request.form['Niter'])
        Fun = request.form['Fun']
        # Run false position method
        result = secant_method(Xi, Xs, Tol, Niter, Fun)
        # Ensure static file paths are correctly handled
        if result.get("png_path") and result.get("html_path"):
            png_url = url_for("static", filename=result.get("png_path").replace("static/", ""))
            html_url = url_for("static", filename=result.get("html_path").replace("static/", ""))
    
            return render_template("secant.html", result=result, 
                               iterations=result.get("iterations"),
                               png_path=png_url,
                               html_path=html_url
            ) 
        # Pass results to template
        return render_template("secant.html", result=result, 
                               iterations=result.get("iterations"),
        )

    
    # GET request - show form
    return render_template('secant.html')


if __name__ == '__main__':
    app.run(debug=True)

