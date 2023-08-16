import mysql.connector

def connect():
    cnx = mysql.connector.connect(\
        host='database'\
        , user='root'\
        , password='root'\
        , port='3306'\
        , database='community'\
    )
    return cnx

command = {
    #user_id
    'GetPassword' : ('SELECT password FROM user_table '
                     'WHERE user_id = %s '
                     ';'),
    
    #user_id, password
    'SignUp' : ('INSERT INTO user_table '
                '(user_id, password) '
                'VALUES (%s, %s) '
                ';'),
    
    #user_id, title, content
    'CreatePost' : ('INSERT INTO post_table '
                    '(user_id, title, content) '
                    'VALUES (%s, %s, %s) '
                    ';'),
    
    #None
    'GetPostCnt' : ('SELECT COUNT(post_id) FROM post_table ;'),
    
    #count, offset
    'GetPage' : ('SELECT post_id, user_id, title FROM post_table '
                 'ORDER BY post_id ASC '
                 'LIMIT %s OFFSET %s '
                 ';'),
    
    #post_id
    'GetPost' : ('SELECT post_id, user_id, title, content FROM post_table '
                 'WHERE post_id = %s '
                 ';'),
    
    #title, post_id
    'ChangeTitle' : ('UPDATE post_table '
                     'SET title = %s '
                     'WHERE post_id = %s '
                     ';'),
    #content, post_id
    'ChangeContent' : ('UPDATE post_table '
                     'SET content = %s '
                     'WHERE post_id = %s '
                     ';'),
    
    #post_id
    'DeletePost' : ('DELETE FROM post_table '
                    'WHERE post_id = %s '
                    ';')
}
