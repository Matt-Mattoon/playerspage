from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,redirect,session,request,flash
from flask_app.controllers  import controllers_cpers
from flask_app.models.models_user import User
from flask_app.models import models_user

@app.route('/')
def loginreg():
    return render_template ('loginreg.html')


@app.route('/register' , methods = ['post'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {"email":request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not User.validate_user(request.form) or user_in_db :
        flash ('') or flash('this account already exist')
        return redirect('/')
    data = {
    'first_name'  : request.form['first_name'],
    'last_name' : request.form['last_name'],
    'email': request.form['email'],
    'user_id':request.form['user_id'],
    'password':pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect (f'/cplrs/{session["user_id"]}')
    
    
@app.route('/login', methods=['POST'])
def login():
    # see if the first_name provided exists in the database
    data = { "email" : request.form["email"]}
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect (f'/cplrs/{session["user_id"]}')





if __name__=='__main__':
    app.run(debug=True)