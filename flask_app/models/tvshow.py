from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# create a regular expression object that we'll use later   
class Tvshow:
    db_name='mybeltexam'
    def __init__(self,data):
        self.id = data['id'],
        self.title = data['title'],
        self.network = data['network'],
        self.release_date = data['release_date'],
        self.description = data['description'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']
    
    @classmethod
    def getAlltvshows(cls):
        query= 'SELECT * FROM tvshows;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        tvshows= []
        if results:
            for row in results:
                tvshows.append(row)
            return tvshows
        return tvshows
    @classmethod
    def get_tvshows_by_id(cls, data):
        query= 'SELECT * FROM tvshows LEFT JOIN users on tvshows.user_id = users.id WHERE tvshows.id = %(tvshow_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
        
        

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM tvshows WHERE tvshows.id=%(tvshow_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_tvshow(cls,data):
        query = 'UPDATE tvshows SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s, user_id = %(user_id)s WHERE tvshows.id = %(tvshow_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    #Class Method to create a user
    @classmethod
    def create_tvshow(cls,data):
        query = 'INSERT INTO tvshows (title, network, release_date,description, user_id) VALUES ( %(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_logged_user_liked_posts(cls, data):
        query = 'SELECT tvshows_id as id FROM likes LEFT JOIN users on likes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        postsLiked = []
        for row in results:
            postsLiked.append(row['id'])
        return postsLiked

    @staticmethod
    def validate_tvshows(tvshow):
        is_valid = True
        if len(tvshow['title']) < 3:
            flash("Title must be at least 3 characters.", 'title')
            is_valid = False
        if len(tvshow['description']) < 3:
            flash("Description must be at least 3 characters.", 'description')
            is_valid = False
        if tvshow['release_date'] == "":
            flash("Release date must not be blank!", 'release_date')
            is_valid = False
        return is_valid
    

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (tvshow_id, user_id) VALUES ( %(tvshow_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE tvshow_id = %(tvshow_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
   
    @classmethod
    def deleteAllLikes(cls, data):
        query= 'DELETE FROM likes WHERE likes.tvshow_id = %(tvshow_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

