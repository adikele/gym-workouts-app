
# 15.4.2021
# plotting dates and pullups:
# get plot data from fn getplotdata():
# Little bit wondering how did I get the "global" x,y values in my plot data in covid

def create_figure(dates, score):  #TODO -- replace with dates..
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(dates, score, color="blue")
    axis.set_ylabel("Persons infected in last 14 days (source: EU Open Data)")
    axis.set_title(
        f"Cumulative number (14 days) of COVID-19 cases per 100000 persons \n Data updated on:"
    )
    return fig

@app.route("/plot.png")
def plot():
    global x
    global y
    fig = create_figure(x, y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

#modifying bolere from app.py
#pass data to create figure
@app.route("/getplotdata")
def getplotdata():
    selected_user_id = session["username"]
    selected_exe = 'pullup - front pullup'
    sql = "SELECT * FROM records WHERE records.user_id = :x AND WHERE records.exercise = :y"
    result = db.session.execute(sql, {"x": selected_user_id}, {"y": selected_exe})
    data = result.fetchall()

    #if row[2] == 'pullup - front pullup':  #could get this condition from sql query
    print (data)
    '''
    2 conditions:
    row with new date -- put contents of rep_list in dict, initialize rep_list to blank, append to new rep_list
    row with same date as previous row -- append to rep_list
    dict (date: rep_list, ..)
    '''
    pullup_dict = {}
    rep_list = []
    date_previous = '0'
    for row in data:      
        date_current = row[8]
        if  date_current != date_previous:  # row with new date
            rep_list_sum = sum (rep_list)
            pullup_dict [row[8]] = rep_list_sum
            rep_list = []
            rep_list.append(row[5])   # row[5] = repitions
            date_previous = date_current        
        else: # row with same date as previous row:
            rep_list.append(row[5])

    x = pullup_dict.keys() #dates
    y = pullup_dict.values()
    fig = create_figure(x,y) 
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)  
    return render_template("results_plotdata.html", result=pullup_dict.keys())

    
#    return render_template("outofdb_new.html", data=data)

'''
13: bodyweight : pullup - front pullup : None : None : 12 : 2021-04-09 22:40:54.623323 :abc :2021-04-09

bolari
@app.route("/countries_result", methods=["POST"])
def countries_result():
    global x
    global y
    country_sel = request.form["country_name"]

    df = pd.read_csv(DATA_FILE)

    list_countries, list_cases = fetch_home_continent_data(df, country_sel)

    dict_continent = dict(zip(list_countries, list_cases))

    list_countries_random = random_countries(list_countries, country_sel)

    dict_fivecountries = fetch_five_countries_data(
        dict_continent, country_sel, list_countries_random
    )

    x = dict_fivecountries.keys()
    y = dict_fivecountries.values()

    fig = create_figure(x, y)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return render_template("countries_result.jinja2", result=dict_fivecountries.keys())








bolera
@app.route("/plot.png")
def plot():
    global x
    global y
    fig = create_figure(x, y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


bolero
# plotting countries and cases:
def create_figure(countries, cases):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(countries, cases, color="blue")
    axis.set_ylabel("Persons infected in last 14 days (source: EU Open Data)")
    axis.set_title(
        f"Cumulative number (14 days) of COVID-19 cases per 100000 persons \n Data updated on: {DATA_DATE}  Next update: {NEXT_UPDATE_DATE}"
    )
    return fig


bolere 
from app.py
@app.route("/outofdb_new")
def outofdb_new():
    selected_user_id = session["username"]
    sql = "SELECT * FROM records WHERE records.user_id = :x"
    result = db.session.execute(sql, {"x": selected_user_id})
    data = result.fetchall()
    return render_template("outofdb_new.html", data=data)

from db:

CREATE TABLE records (id SERIAL PRIMARY KEY, body_part VARCHAR,  exercise VARCHAR, set_number INTEGER, weight INTEGER, reps INTEGER);

'''