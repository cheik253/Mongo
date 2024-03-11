from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'
app.json_encoder = CustomJSONEncoder  # Set the custom JSON encoder
mongo = PyMongo(app)

@app.route('/api/voters', methods=['GET'])
def get_data():
    try:
        collection = mongo.db.voter
        data = collection.find()

        # jsonify uses the custom JSON encoder
        result = jsonify(list(data))

        return result, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
