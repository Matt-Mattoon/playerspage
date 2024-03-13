from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template,redirect,session,request,flash #type:ignore
from flask_app.models.models_user import User
from flask_app.models.models_attribute import Attribute

@app.route('/create')
def createchar():
    return render_template('createchar.html')
    
@app.route('/create/new' , methods=['post'])
def solidify_characters():
    data = {'top_strength':request.form['top_strength'],
            'bottom_strength':request.form['bottom_strength'],
            'speed':request.form['speed'],
            'user_id':request.form['user_id']
            }
    #defining data above so it knows what to look for when we say data below
    Attribute.create(data)
    #calling the function of create that we made in the attribute class
    return redirect (f'/cplrs/{request.form["user_id"]}')


@app.route('/cplrs/<int:id>')
def showcplrs(id):
    data = {'id':id}
    attribute_set = Attribute.get_one(data)
    return render_template('showcplr.html' ,  attribute_set = attribute_set)