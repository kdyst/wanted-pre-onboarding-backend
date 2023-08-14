#This is naive non-mysql code.
#It must be re-written.

from bisect import bisect_left

post_cnt = 0
user_table = dict()
post_table = list()


#(user_id, password) --> bool
def create_user(user_id, password):
    global user_table, post_table, post_cnt
    
    if user_id in user_table:
        return False
    user_table[user_id] = password
    return True


#(user_id) --> password:str or None
def find_user(user_id):
    global user_table, post_table, post_cnt
    
    return user_table.get(user_id)


#(user_id, title, content) --> post_id:int
def create_post(user_id, title, content):
    global user_table, post_table, post_cnt
    
    post_id = post_cnt
    post_table.append((post_id, user_id, title, content))
    post_cnt += 1
    return post_id


#(None) --> int
def get_pagecnt():
    global user_table, post_table, post_cnt
    
    return len(post_table)


#(page_id, unit) --> arr: list<dict<post_id, user_id, title>>
def get_page(page_id, unit):
    global user_table, post_table, post_cnt

    left = min(max(page_id * unit, 0), len(post_table))
    right = min(left + unit, len(post_table))
    arr = []
    for i in range(left, right):
        j = len(post_table) - 1 - i
        post_id = post_table[i][0]
        user_id = post_table[i][1]
        title = post_table[i][2]
        arr.append({\
            'post_id':post_id\
            , 'user_id':user_id\
            , 'title':title\
        })
    return arr


#(post_id) --> dict<post_id, user_id, title, content> or None
def get_post(post_id):
    global user_table, post_table, post_cnt

    i = bisect_left(post_table, post_id, \
        key=lambda x: x[0] if type(x) == tuple else x\
    )
    if i == len(post_table) or post_id != post_table[i][0]:
        return None
    
    return {\
        'post_id' : post_table[i][0]\
        , 'user_id' : post_table[i][1]\
        , 'title' : post_table[i][2]\
        , 'content' : post_table[i][3]\
    }


#(post_id, user_id, title, content) --> bool
def patch_post(post_id, user_id, title = None, content = None):
    global user_table, post_table, post_cnt

    i = bisect_left(post_table, post_id, \
        key=lambda x: x[0] if type(x) == tuple else x\
    )
    if i == len(post_table) or\
        post_id != post_table[i][0] or\
        user_id != post_table[i][1]:
        return False
    if title == None:
        title = post_table[i][2]
    if content == None:
        content = post_table[i][3]
    
    post_table[i] = (post_id, user_id, title, content)
    return True


#(post_id, user_id) --> bool
def delete_post(post_id, user_id):
    global user_table, post_table, post_cnt

    i = bisect_left(post_table, post_id, \
        key=lambda x: x[0] if type(x) == tuple else x\
    )
    if i == len(post_table) or\
        post_id != post_table[i][0] or\
        user_id != post_table[i][1]:
        return True
    if post_table[i][1] != user_id:
        return False
    post_table.pop(i)
    return True
