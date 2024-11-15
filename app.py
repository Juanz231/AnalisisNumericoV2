from flask import Flask, render_template, request, send_file, url_for
from services.cap1.bisection_method import bisection_method
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

if __name__ == '__main__':
    app.run(debug=True)

