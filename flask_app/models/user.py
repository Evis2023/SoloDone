from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name='mybeltexam'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']
    
    @classmethod
    def getAllUsers(cls):
        query= 'SELECT * FROM users;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        users= []
        for row in results:
            users.append(row)
        return users
    
    @classmethod
    def get_user_by_id(cls, data):
        query= 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]


    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def create_user(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s,  %(email)s , %(password)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_logged_user_liked_posts(cls, data):
        query = 'SELECT tvshow_id as id FROM likes LEFT JOIN users on likes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        postsLiked = []
        for row in results:
            postsLiked.append(row['id'])
        return postsLiked

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name be at least 2 characters.", 'first_name')
            is_valid = False
        if len(user['first_name']) < 1:
            flash("Field required.", 'first_name')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name be at least 2 characters!", 'last_name')
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Field required!", 'last_name')
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'passwordRegister')
            is_valid = False
        if user['confirmpassword'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid