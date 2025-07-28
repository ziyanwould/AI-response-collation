import os
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from analysis import analyze_data
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def process_data(data):
    try:
        results = analyze_data(data)
        # Convert dict_keys to lists for JSON serialization
        results['optimization_category_counts_labels'] = list(results['optimization_category_counts'].keys())
        results['optimization_category_counts_values'] = list(results['optimization_category_counts'].values())
        results['sentiment_counts_labels'] = list(results['sentiment_counts'].keys())
        results['sentiment_counts_values'] = list(results['sentiment_counts'].values())
        results['category_counts_labels'] = list(results['category_counts'].keys())
        results['category_counts_values'] = list(results['category_counts'].values())
        return render_template('index.html', results=results)
    except pd.errors.EmptyDataError:
        return "错误：上传的CSV文件为空或无效。"
    except Exception as e:
        return f"发生错误：{e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                data = pd.read_csv(filepath).to_csv(index=False)
                return process_data(data)
        elif 'data' in request.form:
            data = request.form['data']
            if not data:
                return "错误：粘贴的数据为空。"
            return process_data(data)
    return render_template('index.html', results=None)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
