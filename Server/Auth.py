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

@Auth.route("/RegisterOrg", methods=('POST',))
def RegOrg():
    #request input
    #{
    #   OrgName: 
    #   UserName:
    #   Password:
    #   FirstName:
    #   LastName:
    #   Email:
    #}
    req = request.get_json()
    OrgName = req['OrgName']
    UserName = req['UserName']
    Password = req['Password']
    FirstName = req['FirstName']
    LastName = req['LastName']
    Email = req['Email']

    cur = conn.cursor()
    #query for finding user user in 
    query_string = "SELECT * FROM Users WHERE UserName = %s"

    #query execute
    cur.execute(query_string,[UserName])
    User = cur.fetchall()


    cur1 = conn.cursor()
    #query for finding user user in 
    query_string = "SELECT * FROM Organizations WHERE OrgName = %s"

    #query execute
    cur1.execute(query_string,[OrgName])
    Org = cur1.fetchall()


    if(User or Org):#if user info is correct
        data = {
            "Registered": "False"
        }
    else:#if user info is not correct
        
        insertUser = conn.cursor()

        sql = "INSERT INTO Users (UserName, Password, FirstName, LastName, Email, AccountType, Organization) VALUES (%s, %s,%s, %s,%s, %s,%s)"
        val = [UserName, Password, FirstName, LastName, Email, "Employee", OrgName]
        insertUser.execute(sql, val)

        conn.commit()


        insertOrg = conn.cursor()

        sql = "INSERT INTO Organizations (OrgName, OwnerUser) VALUES (%s, %s)"
        val = [OrgName, UserName]
        insertOrg.execute(sql, val)

        conn.commit()
        
        data = {
            "Registered": "True"
        }

    #json object response
    return jsonify(data)
