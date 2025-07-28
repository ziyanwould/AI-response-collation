import os
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from analysis import analyze_data
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        data = pd.read_csv(filepath).to_csv(index=False)
        results = analyze_data(data)
        return render_template('results.html', **results)


@app.route('/analyze', methods=['POST'])
def analyze_text_data():
    data = request.form['data']
    results = analyze_data(data)
    return render_template('results.html', **results)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
