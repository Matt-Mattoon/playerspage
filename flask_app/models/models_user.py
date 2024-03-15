from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #type:ignore
import re	# the regex module
# create a regular expression object that we'll use later   
r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
db = 'atheletes'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls , data):
        query = 'insert into users (first_name , last_name , email , password) values ( %(first_name)s , %(last_name)s , %(email)s , %(password)s )'
        return connectToMySQL(db).query_db(query , data)
    
    @classmethod
    def get_by_email(cls , data):
        query = 'select * from users where email = %(email)s;'
        result = connectToMySQL(db).query_db(query,data)
        if len(result)< 1:
            return False
        return cls(result[0])
    
    
    
    @staticmethod
    def validate_user(users):
        is_valid = True
        if len(users['first_name']) < 2 or len(users['first_name']) > 21 :
            flash("first_name must be between 1 and 21  characters.")
            is_valid = False
        if not EMAIL_REGEX.match(users['email']):
            flash('Invalid Email.')
            is_valid = False
        if len(users['password']) < 1:
            flash("Please enter a password")
            is_valid = False
            
        return is_valid