from flask import Blueprint, render_template, request, jsonify
import pymysql
import os, json
from dotenv import load_dotenv, dotenv_values
from dataclasses import dataclass
import bcrypt
import jwt
import datetime
 

@dataclass(eq=True)
class UserObj:
    UserName     :str
    Password     :str
    FirstName    :str
    LastName     :str
    Email        :str
    AccountType  :str
    Organization :str

    def __init__(self, items):
        print(f"items is/are {items}")
        self.UserName     = items[0]
        self.Password     = items[1]
        self.FirstName    = items[2]
        self.LastName     = items[3]
        self.Email        = items[4]
        self.AccountType  = items[5]
        self.Organization = items[6]

    def get_json(self):
        return dataclass.asdict(self)



    

load_dotenv()#loading env variables
AppServices = Blueprint("AppServices",__name__)

#mysql connection config
conn = pymysql.connect( 
        host=os.getenv('HOSTDB'), 
        user=os.getenv('USERDB'),  
        password = os.getenv('PASSDB'), 
        db=os.getenv('DBDB'), 
        ) 


#home route used for testing
@AppServices.route("/")
def home():
    return "Home"


#
@AppServices.route("/GetUserApps", methods=('POST',))
def login():
    #get request info
    req = request.get_json()
    UserName = req['UserName']
    print(UserName)
    
    cur = conn.cursor()
    #
    query_string = "SELECT AppName FROM AppUsers WHERE Users = %s"

    #query execute
    cur.execute(query_string,[UserName])
    data = cur.fetchall()
    
    #json object response
    return jsonify(data)
