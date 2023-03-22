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
    sql = """ select net, count(net),max(mag) from earthquake.upload where mag between %s and %s group by net order by net; """
    tuple1 = (get_mag1,get_mag2)
    mycursor = conn.cursor()
    mycursor.execute(sql, tuple1)
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=['net', 'count', 'max_mag'])
    
    # Create a bar chart using Plotly
    data = [go.Bar(x=df['net'], y=df['count'])]
    layout = go.Layout(title='Number of Earth Quakes by State in the Given Range', xaxis={'title': 'State'},
    yaxis={'title': 'Number of Occurences'})
    fig = go.Figure(data=data, layout=layout)

    # Convert the chart data to JSON string
    chart_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template with the chart data
    return render_template('mag_out.html', chart_data=chart_data)

@app.route('/get_pop',methods = ["GET","POST"])
def get_pop():
    return render_template('get_pop.html')

@app.route('/population', methods=['POST'])
def population():
    get_pop1 = int(request.form["pop1"])
    get_pop2 = int(request.form["pop2"])

    sql = """ SELECT State, SUM(Population) FROM earthquake.assign3 WHERE Population BETWEEN %s AND %s GROUP BY State ORDER BY Sum(population) DESC;"""
    tuple1 = (get_pop1,get_pop2)
    mycursor = conn.cursor()
    mycursor.execute(sql, tuple1)
    myresult = mycursor.fetchall()
    print(myresult)

    df = pd.DataFrame(myresult, columns=['State', 'Population'])
    

    # Create a bar chart using Plotly
    trace = go.Bar(x=df['State'], y=df['Population'])
    layout = go.Layout(title='Population by State')
    fig = go.Figure(data=[trace], layout=layout)

    # Convert the Plotly figure to a JSON string and insert it into the template
    #chart_json = fig.to_json()
    chart_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Convert the DataFrame to an HTML table and insert it into the template
    table_html = df.to_html(index=False)

    # Render the template with the chart and table
    return render_template('pop.html', chart_data=chart_data, table_html=table_html)

@app.route('/top_pop',methods = ["GET","POST"])
def top_pop():
    return render_template('top_pop.html')

@app.route('/disp_pop', methods=['GET','POST'])
def disp_pop():
    pop1 = int(request.form["pop1"])
    pop2 = int(request.form["pop2"])
    #num = int(request.form["num"])

    sql = """ SELECT State, Population
              FROM (
                  SELECT State, Population
                  FROM earthquake.test2
                  WHERE Population BETWEEN %s AND %s
                  ORDER BY Population DESC
                  LIMIT 3
              ) top_states
              UNION
                  SELECT State, Population
                  FROM (
                      SELECT State, Population
                      FROM earthquake.test2
                      WHERE Population BETWEEN %s AND %s
                      ORDER BY Population ASC
                      LIMIT 3
                  ) bottom_states;"""
    data = (pop1, pop2,pop1,pop2)
    mycursor = conn.cursor()
    mycursor.execute(sql, data)
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=['State', 'Population'])

    # Create top chart
    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(x=df[df['Population'] > df['Population'].mean()].State,
                             y=df[df['Population'] > df['Population'].mean()].Population,
                             name='Top 3 States',
                             marker=dict(color='red')))
    fig_top.update_layout(title='Top 3 States with Population above Mean', xaxis_title='State', yaxis_title='Population')

    # Create bottom chart
    fig_bottom = go.Figure()
    fig_bottom.add_trace(go.Bar(x=df[df['Population'] < df['Population'].mean()].State,
                                y=df[df['Population'] < df['Population'].mean()].Population,
                                name='Bottom 3 States',
                                marker=dict(color='blue')))
    fig_bottom.update_layout(title='Bottom 3 States with Population below Mean', xaxis_title='State', yaxis_title='Population')

    # Convert figures to JSON format
    fig_top_json = json.dumps(fig_top, cls=plotly.utils.PlotlyJSONEncoder)
    fig_bottom_json = json.dumps(fig_bottom, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('disp_pop.html', plot_top=fig_top_json, plot_bottom=fig_bottom_json)



    

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=5000, debug = True)






