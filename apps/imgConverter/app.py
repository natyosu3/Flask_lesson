from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
import subprocess
import threading

app = Flask(__name__)
app.config['convert_finished'] = False  # フラグをアプリケーションの設定に格納します

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert/", methods=["GET", "POST"])
def convert():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path, 'static/images', filename))

        th = threading.Thread(target=convert_pdf, args=(filename, ))
        th.start()

        return redirect(url_for('uploaded_file', filename=filename))

    return render_template("convert_page.html")

@app.route('/uploaded_file/<string:filename>')
def uploaded_file(filename):
    # アプリケーションの設定からフラグの値をチェックしてリダイレクトを行う
    if app.config['convert_finished']:
        return redirect(url_for('finished', filename=filename))

    return render_template('uploaded_file.html', filename=filename)

@app.route('/finished/<string:filename>')
def finished(filename):
    return render_template('finish.html')

def convert_pdf(filename):
    result = subprocess.Popen(f"ffmpeg -i {os.path.join(os.getcwd(), 'apps', 'imgConverter', 'static', 'images', filename)} {os.path.join(os.getcwd(), 'apps', 'imgConverter', 'static', 'images', filename + '.avi')}", stdout=subprocess.DEVNULL)
    result.wait()

    # アプリケーションの設定のフラグを設定する
    app.config['convert_finished'] = True

if __name__ == "__main__":
    app.run(debug=True)
