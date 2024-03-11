from flask import Flask,render_template,redirect,url_for
from flask_pymongo import PyMongo
from flask import jsonify

app=Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'
mongo = PyMongo(app)

@app.route('/)
def get_data():
    collection = mongo.voter # Replace with your actual collection name
    data = collection.find()
    
    result = []
    for document in data:
        result.append(document)
    
    return jsonify(result)

app.run(debug=True)