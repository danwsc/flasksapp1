# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:28:22 2021

@author: Lenovo
"""
from mysql.connector import pooling
# import mariadb
import os,sys

from config.Settings import Settings

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

class DatabasePool:
    
    # class variable
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name = 'ws_pool',
            pool_size = 5,
            host = Settings.host,
            port = 3306,
            user = Settings.user,
            password = Settings.password,
            database= Settings.database
        )
    except pooling.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        sys.exit(1)
    
    @classmethod
    def getConnection(cls):
        dbConn = cls.connection_pool.get_connection()
    
        return dbConn
