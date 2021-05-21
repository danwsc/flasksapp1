from flask import Flask,jsonify
from mysql.connector import pooling
# from config.Settings import Settings

import os

# HOST='localhost'
# DATABASE='furniture'
# USER='root'
# PASSWORD=''
HOST=os.environ['HOST']
DATABASE=os.environ['DATABASE']
USER=os.environ['USERNAME']
PASSWORD=os.environ['PASSWORD']
# HOST=os.environ['HOST2']
# DATABASE=os.environ['DATABASE2']
# USER=os.environ['USERNAME2']
# PASSWORD=os.environ['PASSWORD2']

app = Flask(__name__)


# http://localhost:5000?data=test@test.com
@app.route('/')
def validate():
   
    return "hello world"


@app.route('/users')
def validate2():
    # print(Settings.host)
    host=HOST
    database=DATABASE
    user=USER
    password=PASSWORD
    # print("host2",host)
    connection_pool = pooling.MySQLConnectionPool(pool_name="ws_pool",
                                                  pool_size=5,
                                                  host=host,
                                                  database=database,
                                                  user=user,
                                                  password=password)
    dbConn = connection_pool.get_connection()
    cursor = dbConn.cursor(dictionary=True)
    sql="select * from user"
    cursor.execute(sql)
    users = cursor.fetchall()
    try:
        jsonUsers=users
        jsonUsers={"Users":jsonUsers}
        return jsonify(jsonUsers)
    except Exception as err:
        print(err)
        return {},500

    dbConn.close()
   
    return "users"    

@app.route('/settings')
def Settings():
    host=HOST
    database=DATABASE
    user=USER
    password=PASSWORD
    settings={"host":host,"username":user,"database":database}
    return jsonify(settings)
    

if __name__ == '__main__':
    app.run(debug=True)
