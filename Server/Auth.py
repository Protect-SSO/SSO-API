from flask import Blueprint, render_template, request, jsonify
import pymysql
import os
from dotenv import load_dotenv, dotenv_values
#jwt imports
import jwt
import datetime
#bcrypt imports
import hash

load_dotenv()#loading env variables
Auth = Blueprint("Auth",__name__)

#mysql connection config
conn = pymysql.connect( 
        host=os.getenv('HOSTDB'), 
        user=os.getenv('USERDB'),  
        password = os.getenv('PASSDB'), 
        db=os.getenv('DBDB'), 
        ) 

#jwt where it gets passed into:
#Auth.config['KEY']=os.getenv('SECRETKEY')

#jwt create token function
def createToken(username):
    token=jwt.encode({'user':username, 
                      'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=5)},
                        os.getenv('SECRETKEY'))
    return token.decode('UTF-8')

#route that handles login and notifies website
@Auth.route("/Login", methods=('POST',))
def login():
    #get request info
    req = request.get_json()
    UserName = req['UserName']
    provided_password = req['Password']
    print(UserName)
    
    cur = conn.cursor()
    #query for logging user in 
    query_string = "SELECT * FROM Users WHERE UserName = %s AND Password = %s"

    #query execute
    cur.execute(query_string,[UserName, provided_password])
    dat = cur.fetchone()
    if(dat):#if user info is correct

        #retrieve hashed password and salt from db
        stored_hashed_password=dat['Password']
        salt=dat['Salt']

        #BCRYPT Verify the provided password against the stored hashed password using bcrypt
        if hash.verify_password(provided_password, stored_hashed_password, salt):

            #JWT invoke create token to you guessed it create a token
            token=jwt.encoded = jwt.encode({"user": dat[0]}, "secrete", algorithm="HS256")


            data = {
                "Login": "True",
                "Token":token,
                "User": {
                    "UserName": dat[0],
                    "FirstName": dat[2],
                    "LastName": dat[3],
                    "Email": dat[4],
                    "AccountType": dat[5],
                    "Org": dat[6],
                }
            }
        else:#if user info is not correct
            data = {
                "Login": "False",
            }

        #json object response
        return jsonify(data)


@Auth.route("/RegisterOrg", methods=('POST',))
def RegOrg():

    #request info
    req = request.get_json()
    OrgName = req['OrgName']
    UserName = req['UserName']
    hashed_password, salt = hash.hash_password(req['Password'])
    FirstName = req['FirstName']
    LastName = req['LastName']
    Email = req['Email']

    cur = conn.cursor()
    #query for finding user
    query_string = "SELECT * FROM Users WHERE UserName = %s"

    #query execute
    cur.execute(query_string,[UserName])
    User = cur.fetchall()


    cur1 = conn.cursor()
    #query for finding org
    query_string = "SELECT * FROM Organizations WHERE OrgName = %s"

    #query execute
    cur1.execute(query_string,[OrgName])
    Org = cur1.fetchall()


    if(User or Org):#if user or org found
        data = {
            "Registered": "False"
        }
    else:#if no org or user exist, register
        
        insertUser = conn.cursor()

        sql = "INSERT INTO Users (UserName, Password, Salt, FirstName, LastName, Email, AccountType, Organization) VALUES (%s, %s,%s, %s,%s, %s,%s)"
        val = [UserName, hashed_password,salt, FirstName, LastName, Email, "Owner", OrgName]
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

@Auth.route("/decode_token", methods=('POST',))
def decode_token_route():
        #request info
        req = request.get_json()
        OrgName = req['OrgName']
        UserName = req['UserName']
        Password = req['Password']
        FirstName = req['FirstName']
        LastName = req['LastName']
        Email = req['Email']
        try:
            token = req['Token']

            decoded_data=jwt.decode(jwt=token,key=os.getenv('SECRETKEY'),algorithms=['HS256'])
            return jsonify(decoded_data)
        except jwt.DecodeError:
            return jsonify('Invalid token')

@Auth.route('/verify_token',methods=('POST',))
def is_token_expired():
             #request info
        req = request.get_json()
        OrgName = req['OrgName']
        UserName = req['UserName']
        Password = req['Password']
        FirstName = req['FirstName']
        LastName = req['LastName']
        Email = req['Email']
        token=req['Token']
        try:
            payload = jwt.decode(token, verify=False)  # Decoding without verification
            expiration_timestamp = payload.get('exp', 0)
            current_timestamp = int(datetime.datetime.utcnow().timestamp())
            return current_timestamp > expiration_timestamp
        except jwt.DecodeError:
        # Token is invalid or malformed
            return True
