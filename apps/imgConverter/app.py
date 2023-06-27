from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
import magic
import time


DATABASE = "database.db"
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy()
db.init_app(app)

# テーブルを定義
class UserInfo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)


@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        user_info = UserInfo(
            user_name = request.form["user_name"],
            email = request.form["email"],
            password = request.form["password"]
        )
        db.session.add(user_info)
        db.session.commit()
        return "HELLO, SQL"
    else:
        return render_template("user_register.html")

# IDからDBのユーザー情報を取得して表示
@app.route("/user_<int:id>")
def user_detail(id):
    user_info = db.get_or_404(UserInfo, id)
    return render_template("user_detail.html", user_info=user_info)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user = UserInfo.query.filter_by(user_name=user_name).first()
        if user:
            return redirect(url_for("user_detail", id=user.id))
        else:
            return render_template("index.html")
    else:
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