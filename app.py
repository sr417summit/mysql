#Srividya Ramachandra student id:1002008122
from flask import Flask, render_template
from flask_caching import Cache
import mysql.connector
import pandas as pd
import time
from flask import render_template
from flask import request
from flask import url_for
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

conn = mysql.connector.connect(
  user='sxr8123', 
  password='417Summit', 
  host= 'sxr8123.mysql.database.azure.com', 
  port=3306,
  database="earthquake"
)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        state = request.form["State"]
        r1 = int(request.form["Rank1"])
        #r2 = int(request.form["Rank2"])
        s1_time = time.perf_counter()
        #sql = """SELECT * FROM earthquake.assign3 WHERE State = %s and Rank > %s;"""
        sql = """SELECT * FROM earthquake.assign3 WHERE State = %s;"""
        #params = (state,r1,r2)
        #params = (state,r1)
        mycursor = conn.cursor()
        mycursor.execute(sql, (state,))
        myresult = mycursor.fetchall()
        df_2 = pd.DataFrame(myresult)
        e1_time = time.perf_counter()
        time_el = (e1_time - s1_time)
        return render_template('state.html', table2=df_2.to_html(),titles = ['City',	'State',	'Rank',	'Population',	'lat',	'lon'], time_el=time_el)
    else:
        s_time = time.perf_counter()
        sql = "SELECT * FROM earthquake.assign3;"
        mycursor = conn.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        df_1 = pd.DataFrame(myresult)
        e_time = time.perf_counter()
        time_el_1 = (e_time - s_time)
        return render_template('state.html', table1=df_1.to_html(), time_el_1=time_el_1)
""""
@app.route('/output', methods=["GET", "POST"])
def cache_out():
    if request.method == "POST":
        state = request.form["net"]
        s1_time = time.perf_counter()
        data = cache.get(state)
        if data is None:
            sql = "SELECT * FROM earthquake.assign3 WHERE net = %s;"
            mycursor = conn.cursor()
            mycursor.execute(sql, (state,))
            myresult = mycursor.fetchall()
            data = pd.DataFrame(myresult)
            cache.set(state, data)
            cache.set(state, data)
    
        e1_time = time.perf_counter()
        time_el = (e1_time - s1_time)
        message = "This is from the cache"
        return render_template('cache.html', table1=data.to_html().strip(), time_el=time_el,message=message)
    else:
        s_time = time.perf_counter()
        #state = request.form["net"]
        sql = "SELECT * FROM earthquake.assign3 WHERE net = 'ak';"
        mycursor = conn.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        df_1 = pd.DataFrame(myresult)
        e_time = time.perf_counter()
        time_el_1 = (e_time - s_time)
        message = "This is from the database"
        return render_template('cache.html', table1=df_1.to_html(), time_el_1=time_el_1,message=message)
   
@app.route('/output2', methods=["GET", "POST"])
def cache_data():
    time_list = []
    data_list = []
    if request.method == "POST":
        state = request.form["net"]
        mag = float(request.form["mag"])
        count = int(request.form["count"])
        params = (state,mag)
        for c in range(0,count):
            s1_time = time.perf_counter()
            data = cache.get(state)
            if data is None:
                sql = "SELECT * FROM earthquake.assign3 WHERE State = %s and Rank > %s;"
                mycursor = conn.cursor()
                mycursor.execute(sql, params)
                myresult = mycursor.fetchall()
                data = pd.DataFrame(myresult)
                cache.set(state, data)
            e1_time = time.perf_counter()
            time_el = (e1_time - s1_time)
            time_list.append(time_el)
            data_list.append(data)
            data_df = pd.DataFrame(data)
            #data_df['Time']=time_list
            #data_df['Data'] = data_list
            total_time = sum(time_list)
        
        return render_template('cache1.html', table1=data_df.to_html().strip(),total_time=total_time)
    else:
        
        s_time = time.perf_counter()
        #state = request.form["net"]
        sql = "SELECT * FROM earthquake.assign3 WHERE net = 'ak';"
        mycursor = conn.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        df_1 = pd.DataFrame(myresult)
        e_time = time.perf_counter()
        time_el_1 = (e_time - s_time)
        time_list.append(time_el_1)
        total_time = sum(time_list)
        message = "This is is from the Database"
        return render_template('cache1.html', table1=df_1.to_html(),total_time=total_time)
"""
@app.route('/output3', methods=["GET", "POST"])
def cache_3():
    time_list = []
    data_list = []
    if request.method == "POST":
        state = request.form["State"]
        r1 = int(request.form["Rank"])
        count = int(request.form["count"])
        #params = (state,r1)
        for c in range(0,count):
            s1_time = time.perf_counter()
            data = cache.get(state)
            if data is None:
                #sql = "SELECT * FROM earthquake.assign3 WHERE State = %s and Rank > %s;"
                sql = "SELECT * FROM earthquake.assign3 WHERE State = %s;"
                mycursor = conn.cursor()
                mycursor.execute(sql, (state,))
               
                myresult = mycursor.fetchall()
                data = pd.DataFrame(myresult)
                cache.set(state, data)
                
            e1_time = time.perf_counter()
            time_el = (e1_time - s1_time)
            time_list.append(time_el)
            data_list.append(data)
        
        data_df = pd.concat([pd.Series(time_list), pd.Series(data_list)], axis=1)
        data_df.columns = ['Time', 'Data']
        data_df['Data'] = data_df['Data'].apply(lambda x: ', '.join(map(str, x.values)))
        data_df = pd.melt(data_df, id_vars=['Time'], value_vars=['Data'])
        total_time = sum(time_list)
        return render_template('cache2.html', table1=data_df.to_html(index=False), total_time=total_time)
    else:
        
        s_time = time.perf_counter()
        #state = request.form["net"]
        sql = "SELECT * FROM earthquake.assign3 WHERE State = 'California';"
        mycursor = conn.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        df_1 = pd.DataFrame(myresult)
        e_time = time.perf_counter()
        time_el_1 = (e_time - s_time)
        time_list.append(time_el_1)
        total_time = sum(time_list)
        message = "This is is from the Database"
        return render_template('cache2.html', table1=df_1.to_html(),total_time=total_time)
if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8000, debug = True)






