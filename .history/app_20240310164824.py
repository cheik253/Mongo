from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'
mongo = PyMongo(app)

@app.route('/')
def get_data():
   
        collection = mongo.db.voter  # Use mongo.db instead of mongo
        data = collection.find()

        result = [document for document in data]
        return result

app.run(debug=True)