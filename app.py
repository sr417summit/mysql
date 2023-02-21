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

app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')

import mysql.connector
# Establish the connection
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

@app.route('/state',methods = ["POST"])
def state():
    get_time1 = request.form["time1"]
    get_time2 = request.form["time2"]
    sql = """ select * from earthquake.upload where mag in (select  max(mag) from earthquake.upload where time between %s and %s) """
    tuple1 = (get_time1,get_time2)
    mycursor = conn.cursor()
    mycursor.execute(sql, tuple1)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('state.html')
    return render_template('state.html',tables = [df.to_html()],titles = ['timestamp',	'latitude',	'longitude',	'depth',	'mag',	'magType',	'nst',	'gap',	'dmin',	'rms',	'net',	'id',	'updated',	'type',	'horizontalError',	'depthError',	'magError',	'magNst',	'status',	'locationSource',	'magSource',	'Date',	'Time',	'place'])

@app.route('/latlong',methods = ["GET","POST"])
def latlong():
    return render_template('latlong.html')

@app.route('/allplaces',methods = ["GET","POST"])
def allplaces():
    lat = int(request.form["lat"])
    long = int(request.form["long"])
    latminus = lat-2
    latplus = lat + 2
    longminus = long -2
    longplus = long + 2
    sql = """ select * from earthquake.upload where latitude between %s and %s and longitude between %s and %s;"""
    data = (latminus,latplus,longminus,longplus)
    mycursor = conn.cursor()
    mycursor.execute(sql,data)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('allplaces.html')

    return render_template('allplaces.html',tables = [df.to_html()],titles = ['timestamp',	'latitude',	'longitude',	'depth',	'mag',	'magType',	'nst',	'gap',	'dmin',	'rms',	'net',	'id',	'updated',	'type',	'horizontalError',	'depthError',	'magError',	'magNst',	'status',	'locationSource',	'magSource',	'Date',	'Time',	'place'])

@app.route('/place_search',methods = ["GET","POST"])
def place_search():
    return render_template('place_search.html')

@app.route('/place_out',methods = ["GET","POST"])
def place_out():
    place = "'%%" + request.form["place"] + "%%'"       
    sql = """ select * from earthquake.upload where place like %s;"""
    data = [(place)]
    mycursor = conn.cursor()
    mycursor.execute(sql,data)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('place_out.html')

    return render_template('place_out.html',tables = [df.to_html()],titles = ['timestamp',	'latitude',	'longitude',	'depth',	'mag',	'magType',	'nst',	'gap',	'dmin',	'rms',	'net',	'id',	'updated',	'type',	'horizontalError',	'depthError',	'magError',	'magNst',	'status',	'locationSource',	'magSource',	'Date',	'Time',	'place'])

@app.route('/mag',methods = ["GET","POST"])
def mag():
    return render_template('mag.html')


@app.route('/mag_out',methods = ["GET","POST"])
def mag_out():
    
    mag1 = int(request.form["mag1"])
    mag2 = int(request.form["mag2"])
 
    sql = """ select * from earthquake.upload where mag between %s and %s;"""
    data = (mag1,mag2)
    mycursor = conn.cursor()
    mycursor.execute(sql,data)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('mag_out.html')

    return render_template('mag_out.html',tables = [df.to_html()],titles = ['timestamp',	'latitude',	'longitude',	'depth',	'mag',	'magType',	'nst',	'gap',	'dmin',	'rms',	'net',	'id',	'updated',	'type',	'horizontalError',	'depthError',	'magError',	'magNst',	'status',	'locationSource',	'magSource',	'Date',	'Time',	'place'])


@app.route('/distance',methods = ["GET","POST"])
def distance():
    return render_template('distance.html')


@app.route('/dist_out',methods = ["GET","POST"])
def dist_out():
    lat1 = int(request.form["lat1"])
    lat2 = int(request.form["lat2"])
    long1 = int(request.form["long1"])
    long2 = int(request.form["long2"])
    dist = int(request.form["dist"])
    lat1 = (lat1 + (dist/111))
    lat2 = (lat2 + (dist/111))
    long1 = (long1 + (dist/111))
    long2 = (long2 + (dist/111))
 
    sql = """ select * from earthquake.upload where latitude  between %s and %s and longitude between %s and %s;"""
    data = (lat1,lat2,long1,long2)
    mycursor = conn.cursor()
    mycursor.execute(sql,data)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('dist_out.html')

    return render_template('dist_out.html',tables = [df.to_html()],titles = ['timestamp',	'latitude',	'longitude',	'depth',	'mag',	'magType',	'nst',	'gap',	'dmin',	'rms',	'net',	'id',	'updated',	'type',	'horizontalError',	'depthError',	'magError',	'magNst',	'status',	'locationSource',	'magSource',	'Date',	'Time',	'place'])

@app.route('/del_mag',methods = ["GET","POST"])
def del_mag():
    return render_template('del_mag.html')

@app.route('/delmag',methods = ["GET","POST"])
def mdelmag():
    
    mag1 = int(request.form["mag1"])
    mag2 = int(request.form["mag2"])
 
    sql = """UPDATE earthquake.upload SET mag = '%s' WHERE mag = '%s'; """
    data = (mag1,mag2)
    mycursor = conn.cursor()
    mycursor.execute(sql,data)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('delmag.html')
    return render_template('dist_out.html',tables = [df.to_html()],titles = ['timestamp',	'latitude',	'longitude',	'depth',	'mag',	'magType',	'nst',	'gap',	'dmin',	'rms',	'net',	'id',	'updated',	'type',	'horizontalError',	'depthError',	'magError',	'magNst',	'status',	'locationSource',	'magSource',	'Date',	'Time',	'place'])

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8000, debug = True)
