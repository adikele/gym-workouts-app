from flask import Flask
from flask import redirect, render_template, request, session, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import copy
from os import getenv
import io
#19.4: plots and all working

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")
global x_sorted, y_sorted


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

@app.route("/type_bodyweight")
def type_bodyweight():
    list_exe = [
        "pullup - front pullup",
        "pullup - back pullup"
    ]
    list_reps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    return render_template(
        "type_bodyweight.html",
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
    

@app.route("/results_bodyweight", methods=["POST"])
def results_bodyweight():
    set_number = 1
    selected_bp = "bodyweight" #changed
    selected_exercise = request.form["select_exercise"]
    selected_day = request.form["select_day"]
    selected_reps = [None] * 5

    for x in range(0, 5):
        selected_reps[x] = request.form.get("select_reps%d" % x)

    selected_user_id = session["username"]

    sets_count_no = int(request.form["sets_count"])

    for x in range(0, sets_count_no):
        sql = "INSERT INTO records (user_id, body_part, exercise, reps, created_at, day) VALUES (:user_id, :body_part, :exercise, :reps, NOW(), :day)"
        result = db.session.execute(
            sql,
            {
                "body_part": selected_bp,
                "exercise": selected_exercise,
                "reps": selected_reps[x],
                "user_id": selected_user_id,
                "day": selected_day,
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


#for plotting pullups:
def create_figure(dates, score):  
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(dates, score, color="blue")
    axis.set_ylabel("Total number of pullups for a day")
    axis.set_title(
        f"Your pullups progress"
    )
    return fig

@app.route("/plot.png")
def plot():
    global x_sorted
    global date_list
    global y_sorted
    fig = create_figure(date_list, y_sorted)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


#extract exercise data and pass to function: create_figure
@app.route("/results_plotdata")
def results_plotdata():
    '''
    5 conditions:
    (i) row which is first row:
    initialize rep_list to blank, append to new rep_list
    (ii) row with new date:
    sum rep_list, put contents of sum_rep_list in dict, initialize rep_list to blank, append to new rep_list
    (iii) row with same date as previous row:
    append to rep_list
    (iv) row which is last row (with either of the above condition):
    do the corresponding action from (i) or (ii) AND
    sum rep_list, put contents of sum_rep_list in dict
    '''
    global x_sorted
    global date_list
    global y_sorted
    selected_user_id = session["username"]
    selected_exe = 'pullup - front pullup'
    sql = "SELECT * FROM records WHERE records.user_id = :x AND records.exercise = :y"
    result = db.session.execute(sql, {"x": selected_user_id, "y": selected_exe})
    data = result.fetchall()
    pullup_dict = {}
    rep_list = []
    date_previous = '0'
    for row in data:      
        date_current = row[8]
        if  date_previous == '0':
            rep_list = []
            rep_list.append(row[5])  # row[5] = repitions
            date_previous = date_current 
        elif date_current == date_previous:
            rep_list.append(row[5])
        elif date_current != date_previous:
            rep_list_sum = sum (rep_list)
            pullup_dict [date_previous] = rep_list_sum
            rep_list = []
            rep_list.append(row[5])   
            date_previous = date_current        
        rep_list_sum = sum (rep_list)
        pullup_dict [date_current] = rep_list_sum

    x = pullup_dict.keys() #dates
    y = pullup_dict.values()
    xy = zip (x,y)
    xyz = sorted ( xy, key=lambda pair: pair[0])
    x_sorted = [ x for x,y in xyz ] 
    y_sorted = [ y for x,y in xyz ] 
    print (x_sorted) #prints ok in datetime
    date_list = []
    for i in x_sorted:
        j = i.strftime('%m/%d/%Y')
        date_list.append(j)


    #fig = create_figure(x_sorted,y_sorted) 
    fig = create_figure(date_list,y_sorted) 
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)  
    return render_template("results_plotdata.html", result=pullup_dict.keys())


if __name__ == "__main__":
    app.debug = True
    app.run()
