from flask import Blueprint, render_template, request, jsonify
import pymysql
import os
from dotenv import load_dotenv, dotenv_values


load_dotenv()#loading env variables
Auth = Blueprint("Auth",__name__)

#mysql connection config
conn = pymysql.connect( 
        host=os.getenv('HOSTDB'), 
        user=os.getenv('USERDB'),  
        password = os.getenv('PASSDB'), 
        db=os.getenv('DBDB'), 
        ) 

#route that handles login and notifies website
@Auth.route("/Login", methods=('POST',))
def login():
    #get request info
    req = request.get_json()
    UserName = req['UserName']
    Password = req['Password']
    print(UserName)
    
    cur = conn.cursor()
    #query for logging user in 
    query_string = "SELECT * FROM Users WHERE UserName = %s AND Password = %s"

    #query execute
    cur.execute(query_string,[UserName, Password])
    dat = cur.fetchall()

    if(dat):#if user info is correct
        data = {
            "Login": "True",
            "Token":"token"
        }
    else:#if user info is not correct
        data = {
            "Login": "False",
        }

    #json object response
    return jsonify(data)