#pass exercise data to create figure
@app.route("/results_plotdata")
def results_plotdata():
    '''
    3 conditions:
    (i)row with new date:
    sum rep_list, put contents of sum_rep_list in dict, initialize rep_list to blank, append to new rep_list
    (ii) row with same date as previous row:
    append to rep_list
    (iii) row which is last row (with either of the above condition):
    do the corresponding action from (i) or (ii) AND
    sum rep_list, put contents of sum_rep_list in dict
    '''
    global y
    global date_list
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
        if  date_current != date_previous:  # row with new date
            rep_list_sum = sum (rep_list)
            print (rep_list)
            pullup_dict [row[8]] = rep_list_sum
            rep_list = []
            rep_list.append(row[5])   # row[5] = repitions
            date_previous = date_current        
        else: # row with same date as previous row:
            rep_list.append(row[5])
        rep_list_sum = sum (rep_list)
        pullup_dict [row[8]] = rep_list_sum

    x = pullup_dict.keys() #dates
    y = pullup_dict.values()
    pullup_dict_list = []
    for i in y:
        pullup_dict_list.append(i)

    date_list = []
    for i in x:
        j = i.strftime('%m/%d/%Y')
        print (j) 
        date_list.append(j)

    print (date_list) 
    print (y)
    print (pullup_dict_list)
    #fig = create_figure(date_list,y) 
    fig = create_figure(date_list, pullup_dict_list)  
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)  
    return render_template("results_plotdata.html", result=pullup_dict.keys())

