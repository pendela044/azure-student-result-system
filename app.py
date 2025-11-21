# app.py
from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os

app = Flask(__name__)

# Azure SQL Database connection (free tier works)
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:azure-internship-server.database.windows.net,1433;"
    "DATABASE=studentdb;"
    "UID=siddhu;"
    "PWD=Azure@2024;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

@app.route('/')
def index():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Results")
    data = cursor.fetchall()
    return render_template('index.html', students=data)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']
    marks = request.form['marks']
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Results (Name, RollNo, Marks) VALUES (?, ?, ?)", 
                   (name, roll, marks))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)