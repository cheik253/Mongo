from flask import Flask,render_template,redirect,url_for
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'

from flask import jsonify
mongo = PyMongo(app)
@app.route('/get_data')
def get_data():
    collection = mongo.db.your_collection_name  # Replace with your actual collection name
    data = collection.find()
    
    result = []
    for document in data:
        result.append({
            'name': document['name'],
            'age': document['age'],
            # Add other fields as needed
        })
    
    return jsonify(result)

app.run(debug=True)