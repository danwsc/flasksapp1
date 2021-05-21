# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:35:00 2021

@author: Lenovo
"""
from model.DatabasePool import DatabasePool
from config.Settings import Settings

import datetime
import jwt
import bcrypt

class User:
    
    @classmethod
    def getAllUsers(cls):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM user;"
            cursor.execute(sql)
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def getUser(cls, userid):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')
            
            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM user WHERE userid=%s;"
            cursor.execute(sql,(userid,))
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
            print('release connection')
            
    @classmethod
    def insertUser(cls, userJson):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            # Hash a password for the first time, with a randomly generated salt
            password = userJson['password'].encode() # convert string to bytes
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())

            sql = "INSERT INTO user (username,email,role,password) VALUES (%s,%s,%s,%s)"
            users = cursor.execute(sql, (userJson['username'],
                                         userJson['email'],
                                         userJson['role'],
                                         hashed))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def deleteUser(cls, userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "DELETE FROM user WHERE userid=%s"
            users = cursor.execute(sql, (userid,))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def updateUser(cls, userid, email, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "UPDATE user SET email=%s, password=%s WHERE userid=%s"
            users = cursor.execute(sql, (email,
                                         password,
                                         userid))
            dbConn.commit()

            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print('release connection')

    @classmethod
    def loginUser1(cls, userJson):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')

            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM user WHERE email=%s"
            cursor.execute(sql, (userJson['email'],))
            user = cursor.fetchone() # at most 1 record since email is supposed to be unique

            if user==None:
                return {'jwt' : ''} # No match
            else:
                # put password test over here
                storedpasswordb = user['password'].encode()
                plaintextb = userJson['password'].encode()
                hashed = bcrypt.hashpw(plaintextb, storedpasswordb)

                if (hashed == storedpasswordb):
                    print('logged in')
                    payload = {'userid' : user['userid'],
                                'role' : user['role'],
                                'exp' : datetime.datetime.utcnow() +
                                        datetime.timedelta(seconds=7200)}
                    jwtToken = jwt.encode(payload, Settings.secretKey, algorithm="HS256")
                    # for Python 3, jwt.encode results in a byte string
                    # which is not accepted by flask.jsonify.
                    # Here the whole jwtToken is decoded to a string and posted in
                    # the bearer field of postman 
                    jwtToken = jwtToken.decode('utf-8')
                    return {'jwt' : jwtToken}
                else:
                    return {'jwt' : ''} # No match

        finally:
            dbConn.close()

    @classmethod
    def loginUser(cls, userJson):
        try:
            dbConn = DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f'Connected to {db_Info}')

            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * FROM user WHERE email=%s"
            cursor.execute(sql, (userJson['email'],))
            user = cursor.fetchone() # at most 1 record since email is supposed to be unique

            if user==None:
                return {'jwt' : ''} # No match
            else:
                # put password test over here
                storedpasswordb = user['password'].encode()
                plaintextb = userJson['password'].encode()
 
                if (bcrypt.checkpw(plaintextb, storedpasswordb)):
                    print('logged in')
                    payload = {'userid' : user['userid'],
                                'role' : user['role'],
                                'exp' : datetime.datetime.utcnow() +
                                        datetime.timedelta(seconds=7200)}
                    jwtToken = jwt.encode(payload, Settings.secretKey, algorithm="HS256")
                    # for Python 3, jwt.encode results in a byte string
                    # which is not accepted by flask.jsonify.
                    # Here the whole jwtToken is decoded to a string and posted in
                    # the bearer field of postman 
                    jwtToken = jwtToken.decode('utf-8')
                    return {'jwt' : jwtToken}
                else:
                    return {'jwt' : ''} # No match

        finally:
            dbConn.close()
