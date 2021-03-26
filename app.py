from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index_lentis")
def index_lentis():
    list_exe = [
        "shoulders - overhead bar",
        "shoulders - lateral raises",
        "shoulders - overhead dumbbells",
    ]
    list_weights = [n for n in range(1, 30)]
    list_reps = [0, 1, 2, 3, 4, 5, 6, 7]
    return render_template(
        "index_lentis.html",
        form_weights=list_weights,
        form_exercise=list_exe,
        form_repititions=list_reps,
    )

#adding for back
@app.route("/type_back")
def type_back():
    list_exe = [
        "back - front row",
        "back - singlehanded dumbbell pull"
    ]
    list_weights = [n for n in range(1, 30)]
    list_reps = [0, 1, 2, 3, 4, 5, 6, 7]
    return render_template(
        "type_back.html",
        form_weights=list_weights,
        form_exercise=list_exe,
        form_repititions=list_reps,
    )

@app.route("/training_results", methods=["POST"])
def training_results():
    set_number = 1
    selected_bp = "shoulders"
    selected_exercise = request.form["select_exercise"]
    selected_weight = [None] * 5
    selected_reps = [None] * 5

    for x in range(0, 5):
        selected_weight[x] = request.form.get("select_weight%d" % x)

    for x in range(0, 5):
        selected_reps[x] = request.form.get("select_reps%d" % x)

    selected_user_id = session["username"]

    sets_count_no = int(request.form["sets_count"])

    for x in range(0, sets_count_no):
        sql = "INSERT INTO records (user_id, body_part, exercise, weight, reps, created_at) VALUES (:user_id, :body_part, :exercise, :weight, :reps, NOW())"
        result = db.session.execute(
            sql,
            {
                "body_part": selected_bp,
                "exercise": selected_exercise,
                "weight": selected_weight[x],
                "reps": selected_reps[x],
                "user_id": selected_user_id,
            },
        )
        db.session.commit()
    return redirect("/")

#adding for back
@app.route("/results_back", methods=["POST"])
def results_back():
    set_number = 1
    selected_bp = "back" #changed
    selected_exercise = request.form["select_exercise"]
    selected_weight = [None] * 5
    selected_reps = [None] * 5

    for x in range(0, 5):
        selected_weight[x] = request.form.get("select_weight%d" % x)

    for x in range(0, 5):
        selected_reps[x] = request.form.get("select_reps%d" % x)

    selected_user_id = session["username"]

    sets_count_no = int(request.form["sets_count"])

    for x in range(0, sets_count_no):
        sql = "INSERT INTO records (user_id, body_part, exercise, weight, reps, created_at) VALUES (:user_id, :body_part, :exercise, :weight, :reps, NOW())"
        result = db.session.execute(
            sql,
            {
                "body_part": selected_bp,
                "exercise": selected_exercise,
                "weight": selected_weight[x],
                "reps": selected_reps[x],
                "user_id": selected_user_id,
            },
        )
        db.session.commit()
    return redirect("/")
    
    

@app.route("/outofdb_new")
def outofdb_new():
    selected_user_id = session["username"]
    sql = "SELECT * FROM records WHERE records.user_id = :x"
    result = db.session.execute(sql, {"x": selected_user_id})
    data = result.fetchall()
    return render_template("outofdb_new.html", data=data)


@app.route("/signup", methods=["POST"])
def signup():
    selected_username = request.form["signup_username"]
    selected_password = request.form["signup_password"]
    hash_value = generate_password_hash(selected_password)
    sql = "INSERT INTO users (username, password ) VALUES (:username, :password)"
    result = db.session.execute(
        sql, {"username": selected_username, "password": hash_value}
    )
    db.session.commit()
    return render_template("signup_done.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user == None:
        return redirect("/invalid_login")
    else:
        hash_value_from_db = user[0]
        if check_password_hash(hash_value_from_db, password):
            session["username"] = username
            return redirect("/exercise_categories")
        else:
            return redirect("/invalid_pw")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/invalid_login")
def invalid_login():
    return render_template("invalid_login.html")


@app.route("/invalid_pw")
def invalid_pw():
    return render_template("invalid_pw.html")


@app.route("/exercise_categories")
def exercise_categories():
    return render_template("exercise_categories.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
