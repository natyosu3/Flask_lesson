from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
import magic
import time

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        file = request.files['file']
        file_data = file.stream.read()

        file_type = magic.from_buffer(file_data, mime=True)
        file.stream.seek(0)  # ファイルの読み取り位置を先頭に戻す

        if file_type == "image/png":
            file.save(os.path.join(app.root_path, 'static/images', secure_filename(file.filename)))
            return redirect(url_for('wait_page', filename=file.filename))
        else:
            return "DAMN"
        
    if request.method == "GET":
        return render_template("convert_page.html")


@app.route('/wait/<filename>')
def wait_page(filename):
    # 変換処理の実行（非同期など）
    time.sleep(3)

    # 変換終了ページにリダイレクト
    return redirect(url_for('finish_page', filename=filename))


@app.route('/finish/<filename>')
def finish_page(filename):
    return render_template('finish.html', filename=filename)


@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
