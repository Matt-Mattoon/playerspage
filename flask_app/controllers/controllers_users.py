from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt #type:ignore
bcrypt = Bcrypt(app)
from flask import render_template,redirect,session,request,flash #type:ignore
from flask_app.controllers  import controllers_cpers
from flask_app.models.models_user import User

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template ('loginreg.html')
    return redirect('/playerspage/home')

@app.route('/register' , methods = ['post'])
def register():
    # validate form data and check whether email is taken
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # the following code in this comment is now handled by User.validate_register
    # data = {"email":request.form["email"]}
    # user_in_db = User.get_by_email(data)
    # if user_in_db:
    #     flash
    # if not User.validate_user(request.form) or user_in_db :
    #     flash ('') or flash('this account already exist')
    #     return redirect('/')
    data = {
    'first_name'  : request.form['first_name'],
    'last_name' : request.form['last_name'],
    'email': request.form['email'],
    'password':pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect ('/playerspage/home') # since 'user_id' is now in session: redirect to home
    
@app.route('/login', methods=['POST'])
def login():
    # validate form data
    if not User.validate_login(request.form):
        return redirect('/')
    # see if the email provided exists in the database
    data = { "email" : request.form["email"]}
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/playerspage/home")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect('/playerspage/home')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('loginreg.html')