#Srividya Ramachandra student id:1002008122
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image
import csv
import pandas as pd
from PIL import Image
import base64
import io
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from IPython.display import HTML
import mysql.connector
from flask import jsonify
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import plotly
import matplotlib.pyplot as plt
import base64
import numpy as np

app = Flask(__name__, static_folder='static', static_url_path='')
conn = mysql.connector.connect(
  user='sxr8123', 
  password='417Summit', 
  host= 'sxr8123.mysql.database.azure.com', 
  port=3306,
  database="earthquake"
)

@app.route('/',methods = ["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/mag_out', methods=['POST'])
def mag_out():
    get_mag1 = int(request.form["mag1"])
    get_mag2 = int(request.form["mag2"])
    get_nbars = int(request.form["num"])
    sql = """SELECT CONCAT_WS('-', FLOOR(S/{}) * {}, FLOOR(S/{}) * {} + {}) AS mag_range, COUNT(*) 
             FROM earthquake.datas 
             WHERE R BETWEEN %s AND %s 
             GROUP BY mag_range 
             ORDER BY mag_range 
             LIMIT {}""".format((get_mag2-get_mag1+1)//get_nbars, get_mag1, (get_mag2-get_mag1+1)//get_nbars, get_mag1, (get_mag2-get_mag1+1)//get_nbars-1, get_nbars)
    tuple1 = (get_mag1, get_mag2)
    mycursor = conn.cursor()
    mycursor.execute(sql, tuple1)
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=['Magnitude Range', 'Count'])
    
    # Create a bar chart using Plotly
    data = [go.Bar(x=df['Magnitude Range'], y=df['Count'])]
    layout = go.Layout(title='Bar Chart', xaxis={'title': 'Magnitude Range'},
                       yaxis={'title': 'Count'})
    fig = go.Figure(data=data, layout=layout)

    # Convert the chart data to JSON string
    chart_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template with the chart data
    return render_template('mag_out.html', chart_data=chart_data)

@app.route('/get_pop',methods = ["GET","POST"])
def get_pop():
    return render_template('get_pop.html')

@app.route('/pie', methods=['POST'])
def pie():
    get_mag1 = int(request.form["pop1"])
    get_mag2 = int(request.form["pop2"])
    get_nbars = int(request.form["num"])
    sql = """SELECT CONCAT_WS('-', FLOOR(S/{}) * {}, FLOOR(S/{}) * {} + {}) AS mag_range, COUNT(*) 
             FROM earthquake.datas 
             WHERE R BETWEEN %s AND %s 
             GROUP BY mag_range 
             ORDER BY mag_range 
             LIMIT {}""".format((get_mag2-get_mag1+1)//get_nbars, get_mag1, (get_mag2-get_mag1+1)//get_nbars, get_mag1, (get_mag2-get_mag1+1)//get_nbars-1, get_nbars)
    tuple1 = (get_mag1, get_mag2)
    mycursor = conn.cursor()
    mycursor.execute(sql, tuple1)
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=['Magnitude Range', 'Count'])
    
    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=df['Magnitude Range'], values=df['Count'], 
                                 hole=0.4, 
                                 sort=False, 
                                 scalegroup='one')])
    
    # Set the number of slices for the pie chart
    fig.update_traces(hole=0.4, sort=False, scalegroup='one', 
                      pull=[0.1]*get_nbars) # change [0.1]*get_nbars to desired proportions
    
    layout = go.Layout(title='Pie Chart')
    fig.update_layout(layout)

    # Convert the chart data to JSON string
    chart_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template with the chart data
    return render_template('pop.html', chart_data=chart_data)

@app.route('/top_pop',methods = ["GET","POST"])
def top_pop():
    return render_template('top_pop.html')

@app.route('/disp_pop', methods=['POST'])
def disp_pop():
    get_r1 = int(request.form["pop1"])
    get_r2 = int(request.form["pop2"])
    mycursor = conn.cursor()
    mycursor.execute("SELECT S, T FROM earthquake.datas WHERE R BETWEEN %s AND %s", (get_r1, get_r2))
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=['S', 'T'])
    
    # Create a scatter chart using Plotly
    high_s = df['S'].quantile(0.5)
    df['color'] = np.where(df['S'] > high_s, 'red', 'green')
    fig = go.Figure(data=go.Scatter(x=df['S'], y=df['T'], mode='markers', marker=dict(color=df['color'])))
    fig.update_layout(title='Scatter Chart of S vs T', xaxis_title='S', yaxis_title='T')

    # Convert the chart data to JSON string
    chart_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template with the chart data
    return render_template('disp_pop.html', chart_data=chart_data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)






