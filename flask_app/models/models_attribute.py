db = 'atheletes'
from flask_app.config.mysqlconnection import connectToMySQL

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
        
        
        
    @classmethod
    def create(cls,data):
        query = 'insert into attributes (name  , school , top_strength , bottom_strength , speed  , position ,   user_id) values (   %(name)s , %(school)s ,  %(top_strength)s , %(bottom_strength)s , %(speed)s , %(position)s ,  %(user_id)s )'
        return connectToMySQL(db).query_db(query ,  data)
    
    @classmethod
    def get_one(cls , data):
        query = """select * from attributes 
        join users ON users.id = attributes.user_id
        Where attributes.id = %(id)s
        """
        results = connectToMySQL(db).query_db(query ,  data)
        attributes = []
        for attribute in results:
            attributes.append(attribute)
        return attributes
    

        
        
        
    
