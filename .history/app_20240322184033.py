from flask import Flask, render_template, jsonify, url_for, redirect, request, flash,session
from flask_pymongo import PyMongo
from datetime import timedelta

  
app = Flask(__name__)
app.secret_key = 'Cheik2263' # Needed for sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)# Adjust the time as needed



app.config['MONGO_URI'] = 'mongodb://localhost:27017/Mongo'  # Change this URI based on your MongoDB configuration
mongo = PyMongo(app)
Voter=mongo.db.voter
Candidate=mongo.db.candidate



@app.route('/', methods=['GET', 'POST'])
def register():
    if 'user'  in session:
         return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        age = int(request.form['age'])  # Convert age to integer
        pawd = request.form['passwd']

        if age < 16:
             flash('Age should be greater or equal to 16.', 'error')  # Flash an error message
             return redirect(url_for('register'))
        check_name=Voter.find_one({'name':nom})
        check_pass=Voter.find_one({'paswd':pawd})

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
        # return redirect(url_for('register'))  # Redirect or render a template as required

    # Render your registration form template if method is GET
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if 'user'  in session:
         return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Here, you should query your database to check if the username and password match
        # This is just a placeholder logic.
        # if name=='admin' and password=='1':
        #      session['user'] = name
        #      return redirect(url_for('admin'))

        user = Voter.find_one({'name':name, 'paswd': password})

        if user:
            session['user'] = name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

    # If the request method is GET, simply render the login page
    return render_template('login.html')
@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user', None)
    if 'user' not in session:
         return redirect(url_for('login'))

    # Redirect to the login page
    return redirect(url_for('login'))

        


 
 


@app.route('/voting/<candidate>/<voter>')
def voting(candidate, voter):
    # Check if the voter already exists in the candidate's voter list
    candidate_doc = Candidate.find_one({'name': candidate, 'voter': {'$elemMatch': {'$eq': voter}}})

    if candidate_doc:
        return redirect(url_for('dashboard'))
        flash(f'You have already voted for {candidate}', 'error')
    else:
        # If the voter does not exist, update the candidate's voter list
        Candidate.update_one({'name': candidate}, {'$push': {'voter': voter}})
        update_voted()
        flash(f'You have already voted for {candidate}', 'error')
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

# @app.route('/admin')
# def admin():
    



@app.route('/dashboard')
def dashboard():
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
        return render_template('voter_dashboard.html', V=Voter, C=Candidate, M=M, i=i)
    else:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    
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

app.run(debug=True,port=8000)
