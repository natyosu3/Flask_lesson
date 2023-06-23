from flask import Flask, url_for, render_template, redirect, request, abort

app = Flask(__name__)

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        print(username, email, description)

        # contactエンドポイントへリダイレクトする
        return render_template("contact_complete.html")
    
    if request.method == "GET":
        return "ERRORだよ"
    



if __name__ == "__main__":
    app.run(debug=True)