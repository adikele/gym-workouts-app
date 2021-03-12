#4.3.2021
#First cloud upload:

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
    list_exe = ["shoulders - overhead bar", "shoulders - lateral raises", "shoulders - overhead dumbbells"]
    list_weights = [n for n in range(1, 30)]   
    list_reps = [0, 1, 2, 3, 4, 5, 6, 7]
    return render_template(
        "index_lentis.html",
        form_weights=list_weights,
        form_exercise=list_exe,
        form_repititions=list_reps,
    )

'''
ORIGINAL
@app.route("/training_results", methods=["POST"])
def training_results():
    set_number = 1
    selected_bp = "shoulders"
    selected_exercise = request.form["select_exercise"]
    selected_weight = request.form["select_weight"]    
    selected_reps = request.form["select_reps"]
    selected_user_id = session["username"] 
    sql = "INSERT INTO records (user_id, body_part, exercise, weight, reps, created_at) VALUES (:user_id, :body_part, :exercise, :weight, :reps, NOW())"
    result = db.session.execute(
        sql,
        {"body_part": selected_bp, "exercise": selected_exercise, "weight": selected_weight, "reps": selected_reps, "user_id": selected_user_id},
    )
    db.session.commit()
    return redirect("/")
'''

@app.route("/training_results", methods=["POST"])
def training_results():
    set_number = 1
    selected_bp = "shoulders"
    selected_exercise = request.form["select_exercise"]

    selected_weight  = [None] * 5
    selected_reps = [None] * 5
    
    for x in range(0, 5):
        selected_weight[x] = request.form.get("select_weight%d" % x)

    for x in range(0, 5):
        selected_reps[x] = request.form.get("select_reps%d" % x)

    #selected_weight = request.form["select_weight"]    
    #selected_reps = request.form["select_reps"]
    selected_user_id = session["username"] 
    
    sets_count_no = int (request.form["sets_count"]) 

    for x in range(0, sets_count_no):
        sql = "INSERT INTO records (user_id, body_part, exercise, weight, reps, created_at) VALUES (:user_id, :body_part, :exercise, :weight, :reps, NOW())"
        result = db.session.execute(
            sql,
            {"body_part": selected_bp, "exercise": selected_exercise, "weight": selected_weight[x], "reps": selected_reps[x], "user_id": selected_user_id},
        )
        db.session.commit()
    return redirect("/")

@app.route("/outofdb_new")
def outofdb_new():
    selected_user_id = session["username"] 
    sql = "SELECT * FROM records WHERE records.user_id = :x" 
    result = db.session.execute(sql, {"x": selected_user_id}, )   
    data = result.fetchall()
    return render_template("outofdb_new.html", data=data)


@app.route("/signup",methods=["POST"])
def signup():
    selected_username = request.form["signup_username"]
    selected_password = request.form["signup_password"]
    hash_value = generate_password_hash(selected_password) #new
    sql = "INSERT INTO users (username, password ) VALUES (:username, :password)"
    result = db.session.execute(
        sql,
        {"username": selected_username, "password": hash_value}, #modified
    )
    db.session.commit()
    return render_template("signup_done.html")
    

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None: #what is this 'user' which is returned?, it is tested twice
        return redirect("/invalid_login")
    else:
        hash_value_from_db = user[0] #modified
        if check_password_hash(hash_value_from_db, password): #new
        #if password_from_db == password:
            session["username"] = username
            return redirect("/correct_login")
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


@app.route("/correct_login")
def correct_login():
    return render_template("correct_login.html")

@app.route("/ref-form")
def ref_form():
    return render_template("ref-form.html")


#ref
@app.route("/ref_form2")
def ref_form2():
    #names = [5]
    #names = [['a', 'b'],['c', 'd']]  
    return render_template("ref_form2.html")

#Note: if this route is gathering form data, it has to be post!!
@app.route("/ref_form2_results", methods=["POST"])
def ref_form2_results():
    #paylename = list
    paylename  = [None] * 3
    for x in range(0, 3):
        paylename [x] = request.form.get("fname%d" % x)
    n = len(paylename)
    '''
    sql = "INSERT INTO records (user_id, body_part, exercise, weight, reps, created_at) VALUES (:user_id, :body_part, :exercise, :weight, :reps, NOW())"
    result = db.session.execute(
        sql,
        {"body_part": selected_bp, "exercise": selected_exercise, "weight": selected_weight, "reps": selected_reps, "user_id": selected_user_id},
    )
    db.session.commit()
    '''
    selected_user_id = session["username"] 
    for x in range (0,3):
        sql = "INSERT INTO records (user_id, weight) VALUES (:user_id, :weight)"
        result = db.session.execute(
            sql,
            {"weight": paylename [x], "user_id": selected_user_id},
        )
        db.session.commit()
    return render_template("ref_form2_results.html", paylename=paylename)
    


if __name__ == "__main__":
    app.debug = True
    app.run()

