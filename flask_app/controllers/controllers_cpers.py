from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template,redirect,session,request,flash
from flask_app.models import models_user
from flask_app.controllers import controllers_cpers
from flask_app.models.models_attribute import Attribute

# create player - get form
@app.route('/create')
def createchar():
    return render_template('createchar.html')
    
# create player - post
@app.route('/create/new' , methods=['post'])
def solidify_characters():

    data = {'name':request.form['name'],
            'school':request.form['school'],
            'position':request.form['position'],
            'top_strength':request.form['top_strength'],
            'bottom_strength':request.form['bottom_strength'],
            'speed':request.form['speed'],
            'user_id':request.form['user_id']
            }
    #defining data above so it knows what to look for when we say data below
    Attribute.create(data)
    #calling the function of create that we made in the attribute class
    return redirect (f'/playerspage/{request.form["user_id"]}')

# home page - get
@app.route('/playerspage/home')
def playerspage():
    if 'user_id' not in session:
        return redirect('/')
    players = Attribute.get_all()
    return render_template('home.html', players = players)

# Show player - get
@app.route('/playerspage/<int:id>')
def show_player(id):
    if 'user_id' not in session:
        return render_template('loginreg.html')
    data = {'id':id}
    attributes = Attribute.get_one(data)
    return render_template('showcplr.html', attributes = attributes)

# Edit player - get form
@app.route('/playerspage/update')
def edit_player():
    if 'user_id' not in session:
        return render_template('loginreg.html')
    return render_template('editplayer.html' , attribute_set = attribute_set)

# Edit player - post
@app.route('/playerspage/update/<int:user_id>', methods=['POST'])
def update_player(user_id):
    if 'user_id' not in session:
        return render_template('loginreg.html')
    data = {
        'name' : request.form['name'],
        'position' : request.form['position'],
        'school' : request.form['school'],
        'top_strength' : request.form['top_strength'],
        'bottom_strength' : request.form['bottom_strength'],
        'speed' : request.form['speed'],
        'id' : request.form['user_id']
    }
    Attribute.update(data)
    return redirect(f'/playerspage/{session['user_id']}')

# Delete player - post
@app.route('/playerspage/<int:user_id>/delete')
def delete_player(user_id):
    if 'user_id' not in session:
        return redirect('/')
    elif user_id != session['user_id']: # protect against db calls from URL
        return redirect('/')
    Attribute.delete(user_id)
    return redirect(f'/playerspage/home')
