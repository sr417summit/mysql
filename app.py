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
    layout = go.Layout(title='Number of Earthquakes by Magnitude Range', xaxis={'title': 'Magnitude Range'},
                       yaxis={'title': 'Count'})
    fig = go.Figure(data=data, layout=layout)

    # Convert the chart data to JSON string
    chart_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template with the chart data
    return render_template('mag_out.html', chart_data=chart_data)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug = True)






