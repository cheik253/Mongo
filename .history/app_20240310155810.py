from flask import Flask,render_template,redirect,url_for
from flask_pymongo import PyMongo

app=Flask(__name__)

@app.route('/')
def a():
    return render_template('a.html')

app.run(debug=True)