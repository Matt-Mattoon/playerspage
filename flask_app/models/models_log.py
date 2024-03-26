db = 'athletes'
from flask_app.config.mysqlconnection import connectToMySQL

class Log: # Meant to mirror the Attribute class
    def __init__(self, data):
        self.id = data['attribute_id']
        self.name = data['name']
        self.position = data['position']
        self.school = data['school']
        self.speed = data['speed']
        self.top_strength = data['top_strength']
        self.bottom_strength = data['bottom_strength']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.log_id = data['id']

    @classmethod
    def get_log(cls, player_id):
        query = 'SELECT * FROM attributes_log WHERE attribute_id = %(player_id)s'
        results = connectToMySQL(db).query_db(query, player_id)
        if results: 
            log = []
            for entry in results:
                cls(entry)
                log.append(entry)
            return log
        return
    
    @classmethod
    def create_log(cls, data, attribute_id):
        log_data = {'name' : data['name'],
                    'school' : data['school'],
                    'position' : data['position'],
                    'top_strength' : data['top_strength'],
                    'bottom_strength' : data['bottom_strength'],
                    'speed' : data['speed'],
                    'attribute_id' : attribute_id
                    }
        query = '''
        insert into attributes_log (name, school, position, top_strength, bottom_strength, speed, attribute_id) 
        values (%(name)s, %(school)s, %(position)s, %(top_strength)s, %(bottom_strength)s, %(speed)s, %(attribute_id)s)
        '''
        return connectToMySQL(db).query_db(query, log_data)
    