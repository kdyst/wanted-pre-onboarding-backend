from flask import Flask #Flask app
from flask import request #Request from Client

from flask_jwt_extended import create_access_token #create jwt
from flask_jwt_extended import get_jwt_identity #get username
from flask_jwt_extended import jwt_required #jwt authentification
from flask_jwt_extended import JWTManager #JWT manager

import bcrypt

import db_entry


app = Flask(__name__)

jwt = JWTManager(app)

app.config.update(\
    JWT_SECRET_KEY = 'd4638f3f733d495c9af729c5b8a83e3d',\
)

@app.route('/greet', methods=['GET'])
def greeting():
    return 'Hello, World!'

#check email & password syntax
def check_email_and_password(email, password):
    return ('@' in email) and (len(password) >= 8)


#sign up(or register)
@app.route('/api/auth/sign-up', methods=['POST'])
def sign_up():
    #unpack
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']
    except KeyError:
        return ('Fail', 400)
    
    #check email and password
    if not check_email_and_password(email, password):
        return ('Fail', 400)
    
    #hash the password
    hash_code = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    #register
    if not db_entry.create_user(email, hash_code):
        return ('Fail', 400)
    
    return ('Success', 200)


#sign in(or login)
@app.route('/api/auth/sign-in', methods=['POST'])
def sign_in():
    #unpack
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']
    except KeyError:
        return ({'status': 'Fail'}, 400)
    
    #check email and password
    if not check_email_and_password(email, password):
        return ({'status': 'Fail'}, 400)
    
    #get encrypted password
    user = db_entry.find_user(email)
    if user == None:
        return ({'status': 'Fail'}, 400)
    
    #rename
    user_id = email
    hash_code = user
    
    #compare password
    if not bcrypt.checkpw(password.encode('utf-8'), hash_code):
        return ({'status': 'Fail'}, 400)
    
    #return JWT token
    return (\
        {\
            'status': 'Success'\
            , 'JWT': create_access_token\
            (\
                identity = user_id\
                , fresh = False\
                , expires_delta = False \
            ) \
        } \
    , 200)


#create new post
@app.route('/api/content/new', methods=['POST'])
@jwt_required()
def create_post():
    #user-id
    user_id = get_jwt_identity()
    if user_id == None:
        return ({'status':'Fail'}, 401)
    
    #unpack
    data = request.get_json()
    try:
        title = data['title']
        content = data['content']
    except KeyError:
        return ({'status':'Fail'}, 400)
    
    #post it
    db_entry.create_post(user_id, title, content)
    
    #return post_id
    return ({'status':'Success'}, 200)


#get the number of pages
@app.route('/api/content/pages/<int:unit>', methods=['GET'])
def page_count(unit):
    
    #verify
    if unit <= 0:
        return ({'status':'Fail'}, 400)
    
    #get the number of posts
    num_post = db_entry.get_pagecnt();
    
    #calculate the number of pages(divide and round up)
    num_page = (num_post + unit - 1) // unit;
    
    #return the number of pages
    return ({'status':'Success', 'num':num_page}, 200);


#get some posts using page_id(maybe page_id is 1-index)
@app.route('/api/content/pages/<int:unit>/<int:page_id>', methods=['GET'])
def get_page(unit, page_id):
    
    #verify
    if unit <= 0 or page_id <= 0:
        return ({'status':'Fail'}, 400)
    
    #get the page of posts(convert to 0-index page_id)
    page = db_entry.get_page(page_id - 1, unit)
    
    #return page
    return ({'status':'Success', 'posts':page}, 200);


#get the post
@app.route('/api/content/<int:post_id>', methods=['GET'])
def get_post(post_id):
    #get post from db
    post = db_entry.get_post(post_id)
    if post == None:
        return ({'status':'Fail'}, 400)
    
    #return the info + content
    return (\
        {\
            'status':'Success'\
            , 'author':post['user_id']\
            , 'title':post['title']\
            , 'content':post['content']\
        }\
    , 200)


#fix the post
@app.route('/api/content/<int:post_id>', methods=['PATCH'])
@jwt_required()
def patch_post(post_id):
    
    #user-id
    user_id = get_jwt_identity()
    if user_id == None:
        return ('Fail', 401)
    
    #read from json
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    #fix the post
    if not db_entry.patch_post(post_id, user_id, title, content):
        return ('Fail', 403)
    
    return ('Success', 200)


#erase the post
@app.route('/api/content/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    #user-id
    user_id = get_jwt_identity()
    if user_id == None:
        return ('Fail', 401)
    
    #erase the post
    if not db_entry.delete_post(post_id, user_id):
        return ('Fail', 403)
    
    return ('Success', 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)