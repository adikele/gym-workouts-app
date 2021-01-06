# 5.1.2021
# this works.. program saves resuslt in database "records" and displays them!
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def index():
    list_weights = [n for n in range(1, 30)]
    list_parts = ["shoulders - overhead push", "back - barbell rows"]
    list_reps = [0, 1, 2, 3, 4, 5, 6, 7]
    return render_template(
        "index.html",
        form_weights=list_weights,
        form_bodyparts=list_parts,
        form_repititions=list_reps,
    )


@app.route("/training_results", methods=["POST"])
def training_results():
    selected_weight = request.form["select_weight"]
    selected_bp = request.form["select_bodypart"]
    selected_reps = request.form["select_reps"]
    sql = "INSERT INTO records (body_part,  weight, reps) VALUES (:body_part, :weight, :reps)"
    result = db.session.execute(
        sql,
        {"body_part": selected_bp, "weight": selected_weight, "reps": selected_reps},
    )
    db.session.commit()
    return redirect("/")


@app.route("/outofdb_new")
def outofdb_new():
    sql = "SELECT * FROM records"
    result = db.session.execute(sql)
    data = result.fetchall()
    return render_template("outofdb_new.html", data=data)


if __name__ == "__main__":
    app.debug = True
    app.run()
