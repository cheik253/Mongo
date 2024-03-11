from flask import Flask,render_template,redirect,url_for
app=Flask(__name__)

@app.route('/')
def a():
    return render_template('a.ht')

app.run(debug=True)