from db_lib import connect
from db_lib import command


#(user_id, password) --> bool
def create_user(user_id, password):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPassword'], (user_id, ))
    ret = list(cursor.fetchall())
    
    empty = (len(ret) == 0)
    if empty:
        cursor.execute(command['SignUp'],(user_id, password))
        cnx.commit();
    
    cursor.close()
    cnx.close()
    return empty


#(user_id) --> password:str or None
def find_user(user_id):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPassword'], (user_id, ))
    ret = list(cursor.fetchall())
    
    cursor.close()
    cnx.close()
    
    password = None
    if len(ret) == 0:
        return None
    
    return bytes(ret[0][0])


#(user_id, title, content) --> None
def create_post(user_id, title, content):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['CreatePost'],(user_id, title, content))
    cnx.commit();
    
    cursor.close()
    cnx.close()


#(None) --> int
def get_pagecnt():
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPostCnt'])
    ret = list(cursor.fetchall())
    
    cursor.close()
    cnx.close()
    
    return ret[0][0]


#(page_id, unit) --> arr: list<dict<post_id, user_id, title>>
def get_page(page_id, unit):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPostCnt'])
    sz = list(cursor.fetchall())[0][0]
    
    offset = page_id * unit
    
    cursor.execute(command['GetPage'], (unit, offset))
    
    ret = []
    for (post_id, user_id, title) in cursor:
        ret.append({\
            'post_id':post_id\
            , 'user_id':user_id\
            , 'title':title\
        })
    
    cursor.close()
    cnx.close()

    return ret


#(post_id) --> dict<post_id, user_id, title, content> or None
def get_post(post_id):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPost'], (post_id, ))
    ret = list(cursor.fetchall())
    
    cursor.close()
    cnx.close()
    
    if len(ret) != 1 or post_id != ret[0][0]:
        return None
    
    return {\
        'post_id' : ret[0][0]\
        , 'user_id' : ret[0][1]\
        , 'title' : ret[0][2]\
        , 'content' : ret[0][3]\
    }


#(post_id, user_id, title, content) --> bool
def patch_post(post_id, user_id, title = None, content = None):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPost'], (post_id, ))
    ret = list(cursor.fetchall())
    
    success = (len(ret) != 0 and ret[0][1] == user_id)
    if success:
        if title != None:
            cursor.execute(command['ChangeTitle'], (title, post_id))
        if content != None:
            cursor.execute(command['ChangeContent'], (content, post_id))
        cnx.commit()
    
    cursor.close()
    cnx.close()
    
    return success


#(post_id, user_id) --> bool
def delete_post(post_id, user_id):
    cnx = connect()
    cursor = cnx.cursor()
    
    cursor.execute(command['GetPost'], (post_id, ))
    ret = list(cursor.fetchall())
    
    success = (len(ret) != 0 and ret[0][1] == user_id)
    if success:
        cursor.execute(command['DeletePost'], (post_id, ))
        cnx.commit()
    
    cursor.close()
    cnx.close()
    
    return success
