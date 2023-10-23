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
def GetUserApps():
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


#
@AppServices.route("/GetApps", methods=('POST',))
def GetApps():
    #get request info
    req = request.get_json()
    OrgName = req['OrgName']
    print(OrgName)
    
    cur = conn.cursor()
    #
    query_string = "SELECT AppName FROM Apps WHERE Org = %s"

    #query execute
    cur.execute(query_string,[OrgName])
    data = cur.fetchall()
    
    #json object response
    return jsonify(data)

#
@AppServices.route("/getRoute", methods=('POST',))
def getRoute():
    #get request info
    req = request.get_json()
    AppName = req['AppName']
    print(AppName)
    
    cur = conn.cursor()
    #
    query_string = "SELECT Redirect_URL FROM Apps WHERE AppName = %s"

    #query execute
    cur.execute(query_string,[AppName])
    data = cur.fetchone()
    
    #json object response
    return jsonify({
        "route":data[0]
    })



@AppServices.route("/RegisterApp", methods=('POST',))
def RegOrg():
    

    #request info
    req = request.get_json()
    OrgName = req['OrgName']
    AppName = req['AppName']
    RedirectURL = req['RedirectURL']

    cur = conn.cursor()
    #query for finding user
    query_string = "SELECT * FROM Apps WHERE AppName = %s"

    #query execute
    cur.execute(query_string,[AppName])
    App = cur.fetchall()



    if(App):#if user or org found
        data = {
            "Registered": "False"
        }
    else:#if no org or user exist, register
        
        insertUser = conn.cursor()

        sql = "INSERT INTO Apps (AppName, Redirect_URL, Org) VALUES (%s, %s,%s)"
        val = [AppName, RedirectURL,OrgName]
        insertUser.execute(sql, val)

        conn.commit()
        
        data = {
            "Registered": "True"
        }

    #json object response
    return jsonify(data)

@AppServices.route("/RequestApp", methods=('POST',))
def RequestApp():
    #get request info
    req = request.get_json()

    AppName = req['AppName']
    UserName = req['UserName']
    OrgName = req['OrgName']
    
    insertRequest = conn.cursor()

    sql = "INSERT INTO AppRequests (UserName, AppName, OrgName) VALUES (%s, %s,%s)"
    

    insertRequest.execute(sql,[UserName,AppName,OrgName])
    conn.commit()
    
    return jsonify({
        "AppRequested": "True"
    })