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
    get_year = request.form["year"]
    get_year2 = request.form["year1"]
    #sql = "select * from test where time in %s, (get_year)"
    sql = """select * from test where time between %s and %s"""
    #query = """Update employee set Salary = %s where id = %s"""
    tuple1 = (get_year,get_year2)
    #tuple1 = (1980,1990)
    mycursor = conn.cursor()
    mycursor.execute(sql, tuple1)
    #mycursor.execute(sql)
    myresult = mycursor.fetchall()
    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df,df2])
    df.to_html('state.html')
    return render_template('state.html',tables = [df.to_html()])

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8000, debug = True)

 