db = 'athletes'
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #type:ignore
from flask_app.models import models_log

class Attribute:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.position = data['position']
        self.school = data['school']
        self.speed = data['speed']
        self.top_strength = data['top_strength']
        self.bottom_strength = data['bottom_strength']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    @classmethod
    def create(cls, data):
        query = '''
        insert into attributes (name, school, position, top_strength, bottom_strength, speed, user_id) 
        values (%(name)s, %(school)s, %(position)s, %(top_strength)s, %(bottom_strength)s, %(speed)s, %(user_id)s)
        '''
        results = connectToMySQL(db).query_db(query, data) # returns attribute id
        models_log.Log.create_log(data, results) # create log 
        return results
    
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM attributes
                WHERE user_id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        if results:
            return cls(results[0])
        return
    
    @classmethod
    def get_all(cls): # create a list of Attribute instances and return it
        query = 'SELECT * FROM attributes;'
        results = connectToMySQL(db).query_db(query)
        if results: 
            attributes = []
            for attribute in results:
                cls(attribute)
                attributes.append(attribute)
            return attributes
        return
    
    @classmethod
    def update(cls, data):
        query = 'UPDATE attributes SET name = %(name)s, school = %(school)s, top_strength = %(top_strength)s, bottom_strength = %(bottom_strength)s, speed = %(speed)s, position = %(position)s WHERE user_id = %(id)s'
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        data = {'id' : id}
        query = 'DELETE FROM attributes WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def player_validation(data):
        is_valid = True
        if len(data['name']) < 2:
            is_valid = False
            flash('Name must be at least 2 letters.')
        if len(data['position']) < 2:
            is_valid = False
            flash('Position must be at least 2 letters.')
        if len(data['school']) < 2:
            is_valid = False
            flash('School must be at least 2 letters.')
        if data['top_strength'] == '':
            is_valid = False
            flash('Bench Press must be more than 0.')
        elif int(data['top_strength']) < 1:
            is_valid = False
            flash('Bench Press must be more than 0.')
        if data['bottom_strength'] == '':
            is_valid = False
            flash('Squat must be more than 0.')
        elif int(data['bottom_strength']) < 1:
            is_valid = False
            flash('Squat must be more than 0.')
        if data['speed'] == '':
            is_valid = False
            flash('Speed must be more than 0.')
        elif float(data['speed']) < 1:
            is_valid = False
            flash('Speed must be more than 0.')
        return is_valid