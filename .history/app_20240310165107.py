from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)

@app.route('/')
def get_data():
    try:
        collection = mongo.db.voter
        data = collection.find()

        # Convert ObjectId to string for JSON serialization
        result = [{'_id': str(doc['_id']), 'name': doc['name']} for doc in data]

        return render_template('a.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
app.run(debug=True)
