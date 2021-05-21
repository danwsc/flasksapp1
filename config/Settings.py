import os

class Settings:

    secretKey="a12nc)238OmPq#cxOlm*a" # your own secret key

    # Dev
    host='localhost'
    database='furniture'
    user='root'
    password=''

    #Staging on heroku
    # host=os.environ['HOST']
    # database=os.environ['DATABASE']
    # user=os.environ['USERNAME']
    # password=os.environ['PASSWORD']