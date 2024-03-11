from flask import Flask,render_template,redirect,url_for
app=Flask(__name__)

@app.route('/')
def a():
    return 'Hello world'


with app.app_context:
    app.run(debug=True)