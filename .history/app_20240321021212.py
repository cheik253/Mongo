from flask import Flask, render_template, jsonify,url_for,redirect,request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_pymongo import PyMongo
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

app.secret_key = 'your_secret_key' # Needed for sessions

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)
Voter=mongo.db.voter
Candidate=mongo.db.candidate

class User(UserMixin):
    def __init__(self, id):
        self.id = id


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
       # Replace 'your_collection_name' with your actual collection name
        result = list(Candidate.aggregate([
            { '$addFields': { 'numberOfElements': { '$size': "$voter" } } },
            { '$project': { 'numberOfElements': 1, '_id': 0, 'name': 1 } }
        ]))

        numbers_of_elements = [int(entry['numberOfElements']) for entry in result]
        voter_name = [entry['name'] for entry in result]

        return jsonify(chartData=[{"data": numbers_of_elements}], categories=voter_name)
    except Exception as e:
        return jsonify(error=str(e)), 500
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here, implement your method for checking the username and password.
        # This is just a placeholder logic.
        if username == "admin" and password == "secret":
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'fiald' # Unauthorized
    else:
        return render_template('login.html')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/a')
def dashboar():
    return render_template('index.html')
app.run(debug=True,port=8000)
