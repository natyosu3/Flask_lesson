from flask import Flask, render_template, request, flash, redirect, url_for
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

import os


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["GET", "POST"])
def convert():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.getcwd() + '/static/images/' + file.filename)
        return redirect(url_for('uploaded_file', filename=file.filename))

    return render_template("convert_page.html")


@app.route('/uploaded_file/<string:filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)


if __name__ == "__main__":
    app.run(debug=True)