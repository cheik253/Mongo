from flask import Flask,render_template,redirect,url_for
app=Flask(__name__)

@app.route('/')
def a():
    return 'He'


with app.app_context:
    app.run(debug=True)