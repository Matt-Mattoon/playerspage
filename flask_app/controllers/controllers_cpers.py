from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template,redirect,session,request,flash #type:ignore
from flask_app.models import models_user
from flask_app.controllers import controllers_cpers
from flask_app.models.models_attribute import Attribute
from flask_app.models.models_log import Log

# create player - get form
@app.route('/create')
def createchar():
    if 'user_id' not in session:
        return redirect('/')
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
    if not Attribute.player_validation(data):
        return redirect('/create')
    Attribute.create(data)
    #calling the function of create that we made in the attribute class
    return redirect (f'/playerspage/{request.form["user_id"]}')

# home page - get
@app.route('/playerspage/home')
def playerspage():
    if 'user_id' not in session:
        return render_template('loginreg.html')
    players = Attribute.get_all()
    return render_template('home.html', players = players)

# Show player - get
@app.route('/playerspage/<int:id>')
def show_player(id):
    if 'user_id' not in session:
        return render_template('loginreg.html')
    data = {'id':id}
    player = Attribute.get_one(data)
    return render_template('showcplr.html', player = player)

#Show player log - get
@app.route('/playerspage/<int:id>/log')
def show_log(player_id):
    if 'user_id' not in session:
        return render_template('loginreg.html')
    data = {'attribute_id' : player_id}
    log = Log.get_log(data)
    return render_template('log.html', log = log)

# Edit player - get form
@app.route('/playerspage/edit/<int:id>')
def edit_player(id):
    if 'user_id' not in session:
        return render_template('loginreg.html')
    data = {'id':id}

    player = Attribute.get_one(data)
    return render_template('editplayer.html' , player = player)

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
        'id' : user_id
    }
    attribute_id = int(request.form['attribute_id'])
    if not Attribute.player_validation(data):
        return redirect(f'/playerspage/edit/{user_id}')
    Attribute.update(data)
    Log.create_log(data, attribute_id)
    return redirect (f'/playerspage/{request.form["user_id"]}')

# Delete player - post
@app.route('/playerspage/<int:user_id>/delete')
def delete_player(user_id):
    if 'user_id' not in session:
        return redirect('/')
    elif user_id != session['user_id']: # protect against db calls from URL
        return redirect('/')
    player = Attribute.get_one({'id' : user_id})
    player_id = player[0]['id']
    print(player)
    Attribute.delete(player_id)
    return redirect(f'/playerspage/{session["user_id"]}')

