from flask import Flask, render_template, jsonify,url_for,redirect
from flask_pymongo import PyMongo
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)
Voter=mongo.db.voter
Candidate=mongo.db.candidate

@app.route('/')
def get_data():
    
        collection = mongo.db.candidate
        data = collection.find()

        # Convert ObjectId to string for JSON serialization
       

        return render_template('list_candidate.html',result=data)
  


@app.route('/voting/<candidate>,<voter>')   
def voting(candidate,voter):
   #Joe Biden
      Candidate.update_one({ "name": candidate },{ '$push': { "voter": voter } })
      update_voted()
      return redirect(url_for('get_data'))

    

@app.route('/update_voted') 
def update_voted():
    pipeline = [
       
        {"$unwind": "$voter"},  # Unwind the "voter" array
        {"$group": {"_id": "$voter"}},
        {"$project": {"_id": 0, "name": "$_id"}}
    ]

    # Execute aggregation
    voter_names = list(Candidate.aggregate(pipeline))

    # Update voters in the Voter collection based on the names obtained
    for voter_name in voter_names:
        Voter.update_many({"name": voter_name['name']}, {"$set": {"has_voted": 1}})
    
    return    redirect(url_for('get_data'))
@app.route('/count')
def count():
    try:
        result = list(Candidate.aggregate([
            { '$addFields': { 'numberOfElements': { '$size': "$voter" } } },
            { '$project': { 'numberOfElements': 1, '_id': 0, 'name': 1 } }
        ]))

        # Extract the values of "numberOfElements" into a list
        numbers_of_elements = [int(entry['numberOfElements']) for entry in result]
        voter_name = [entry['name'] for entry in result]

        # Plotting the pie chart
        fig, ax = plt.subplots()
        ax.pie(numbers_of_elements, labels=voter_name, autopct='%1.1f%%', startangle=90)
        ax.set_title('Number of Voters for Each Candidate')
        plt.legend

        # Save the plot to a BytesIO buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Encode the image as base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # Return the HTML with the embedded image
        return render_template('pie_chart.html', image_base64=image_base64)
    except Exception as v:
        print(str(v))  # Print the exception to the server console for debugging
        return jsonify({'error': str(v)})

@app.route('/login')
def login():
     return render_template('login.html')
app.run(debug=True,port=8000)
