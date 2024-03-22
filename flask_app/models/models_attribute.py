db = 'athletes'
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #type:ignore

class Attribute:
    def __init__(self , data):
        self.id = data['id']
        self.name=data['name']
        self.position = data['position']
        self.school=data['school']
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
        return connectToMySQL(db).query_db(query ,  data)
    
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM attributes 
                Where user_id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        attributes = []
        for attribute in results:
            attributes.append(attribute)
        return results
    
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
        query = 'UPDATE attributes SET name = %(name)s, school = %(school)s, top_strength = %(top_strength)s, bottom_strength = %(bottom_strength)s, speed = %(speed)s, position = %(position)s WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query ,data)
    
    @classmethod
    def delete(cls, user_id):
        data = {'user_id' : user_id}
        query = 'DELETE FROM attributes WHERE user_id = %(user_id)s'
        return connectToMySQL(db).query_db(query, data)