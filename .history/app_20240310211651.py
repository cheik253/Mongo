from flask import Flask, render_template, jsonify,url_for,redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)
Voter=mongo.db.voter
Candidate=mongo.db.candidate
@app.route('/')
def get_data():
    
        collection = mongo.db.voter
        data = collection.find()

        # Convert ObjectId to string for JSON serialization
       

        return render_template('a.html',result=data)
@app.route('/a/<name>')   
def add_election(name):
   Candidate.update_one({ "name": "Donald Trump" },{ '$push': { "voter": "madara" } })

#     #db.people.updateOne(
#   { "name": "Donald Trump" }, // the query to find the document
#   { $push: { "voter": "Johnwick" } } // the update operation using $push
# )

    
   return redirect(url_for('get'))  
     
@app.route('/update_voted')
def update_voted() :
                 
app.run(debug=True,port=8000)
