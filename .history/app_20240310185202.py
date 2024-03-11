from flask import Flask, render_template, jsonify,url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)
Voter=mongo.db.voter
Can
@app.route('/')
def get_data():
    
        collection = mongo.db.voter
        data = collection.find()

        # Convert ObjectId to string for JSON serialization
       

        return render_template('a.html',result=data)
 @app.route('/a')   
def a():
    # query={
    #  'name':'Donald Trump',
    #  'age':76,
    #  'voter':Voter.find_one({},{'name':1,'_id':0})
    # }
    # a=Candidate.insert_one(query)
     pipeline = [
        {"$unwind": "$voter"},
        {"$group": {"_id": "$voter.name"}},
        {"$project": {"_id": 0, "name": "$_id"}}
    ]

    # Execute aggregation
     voter_names = list(Candidate.aggregate(pipeline))

    # Update voters in the Voter collection based on the names obtained
     for voter_name in voter_names:
        Voter.update_one({"name": voter_name['name']}, {"$set": {"has_voted": 1}})
         
app.run(debug=True)
