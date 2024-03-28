from flask import Flask, render_template, redirect, url_for, request, flash, session,jsonify
from flask_pymongo import PyMongo
from datetime import timedelta
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'Cheik2263'  # Needed for sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=100)  # Adjust the time as needed

# Initialize Flask-Session
Session(app)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)
Voter = mongo.db.voter
Candidate = mongo.db.candidate

@app.route('/', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        age = int(request.form['age'])  # Convert age to integer
        pawd = request.form['passwd']

        if age < 18:
            flash('Age should be greater or equal to 18.', 'error')  # Flash an error message
            return redirect(url_for('register'))
        check_name = Voter.find_one({'name': nom})
        check_pass = Voter.find_one({'paswd': pawd})

        if check_name:
            flash('name already exists', 'error')  # Flash an error message
            return redirect(url_for('register'))
        if check_pass:
            flash('password already exists', 'error')  # Flash an error message
            return redirect(url_for('register'))

        query = {'name': nom, 'age': age, 'has_voted': 0, 'email': email, 'paswd': pawd}
        Voter.insert_one(query)  # Assuming 'Voter' is your collection
        flash('Voter added successfully!')
        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = Voter.find_one({'name': name, 'paswd': password})

        if user:
            session['user'] = name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    check_vote()

    if 'user' in session:  # Check if user is logged in
        C = Candidate.count_documents({})
        V = Voter.count_documents({})
        M = Candidate.aggregate([
            {
                '$unwind': '$voter'
            },
            {
                '$group': {
                    '_id': '$name',
                    'count': { '$sum': 1 },
                    'age': { '$first': '$age' }
                }
            },
            {
                '$sort': { 'count': -1 }
            },
            {
                '$project': { '_id': 1, 'count': 1, 'age': 1 }
            }
        ])
        i = session['user']
        session_timeout_seconds = app.config['PERMANENT_SESSION_LIFETIME'].total_seconds()  # Directly using the session timeout value
        return render_template('voter_dashboard.html', V=Voter, C=Candidate, M=M, i=i, session_timeout_seconds=session_timeout_seconds)
    else:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect(url_for('login'))

   

 
 


@app.route('/voting/<candidate>/<voter>')
def voting(candidate, voter):
    # Check if the voter already exists in the candidate's voter list
    candidate_doc = Candidate.find_one({'name': candidate, 'voter': {'$elemMatch': {'$eq': voter}}})
    A=Voter.find({'name':'v,'has_voted':1})

    if A:
        return redirect(url_for('dashboard'))
        flash(f'You have already voted for ', 'error')
    else:
        # If the voter does not exist, update the candidate's voter list
        Candidate.update_one({'name': candidate}, {'$push': {'voter': voter}})
        update_voted()
        flash(f'You have already voted ', 'error')
        return redirect(url_for('dashboard'))  # Assuming this function is defined elsewhere
    return redirect(url_for('dashboard'))


    

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
    
    return    redirect(url_for('dashboard'))

@app.route('/check_vote')
def check_vote():
 

    # Get all distinct voter names from the voter collection
    distinct_voter_names = [voter['name'] for voter in Voter.find({}, {'name': 1})]

    # Find candidates with voters not in the voter collection
    candidates_with_invalid_voters = Candidate.find({'voter.name': {'$nin': distinct_voter_names}})

    print("Candidates with invalid voters:")
    for candidate in candidates_with_invalid_voters:
        print(candidate)  # Print out candidate to see its type

    # Remove invalid voters from the voter array in each candidate document
    for candidate in candidates_with_invalid_voters:
        invalid_voter_names = [voter['name'] for voter in candidate['voter'] if voter['name'] not in distinct_voter_names]
        Candidate.update_one({'_id': candidate['_id']}, {'$pull': {'voter': {'name': {'$in': invalid_voter_names}}}})

    return redirect(url_for('dashboard'))
@app.route('/count')
def count():
    try:
       # Replace 'your_collection_name' with your actual collection name
        result = list(Candidate.aggregate([
            { '$addFields': { 'numberOfElements': { '$size': "$voter" } } },
            { '$project': { 'numberOfElements': 1, '_id': 0, 'name': 1 }} ,{'$match':{'numberOfElements':{'$gt':1}}}
        ]))

        numbers_of_elements = [int(entry['numberOfElements']) for entry in result]
        voter_name = [entry['name'] for entry in result]

        return jsonify(chartData=[{"data": numbers_of_elements}], categories=voter_name)
    except Exception as e:
        return jsonify(error=str(e)), 500

# @app.route('/admin')
# def admin():
    


    
@app.route('/age_can')
def age_can():
    try:
        candidates = Candidate.find({}, {'name': 1, '_id': 0})
        ages = Candidate.find({}, {'age': 1, '_id': 0})
        candidates_list = [candidate['name'] for candidate in candidates]  # Extracting names from candidates
        ages_list = [age['age'] for age in ages]  # Extracting ages
        return jsonify(chartData=[{"data": ages_list}], categories=candidates_list)
    except Exception as e:
        return jsonify(error=str(e)), 500
@app.route('/age_vote')  
def age_vote():
     try:
        candidates = Voter.find({}, {'name': 1, '_id': 0})
        ages = Voter.find({}, {'age': 1, '_id': 0})
        candidates_list = [candidate['name'] for candidate in candidates]  # Extracting names from candidates
        ages_list = [age['age'] for age in ages]  # Extracting ages
        return jsonify(chartData=[{"data": ages_list}], categories=candidates_list)
     except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/election')
def election():
    vote=Voter.count_documents({'has_voted':1})
    not_vote=Voter.count_documents({'has_voted':0})
    return jsonify(vote,not_vote)
    







app.run(debug=True,port=8000)
