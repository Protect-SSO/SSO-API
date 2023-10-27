from flask import Blueprint, render_template, request, jsonify
import pymysql
import os, json
from dotenv import load_dotenv, dotenv_values
from dataclasses import dataclass
import bcrypt
import jwt
import datetime



#conn = conn = pymysql.connect( host=os.getenv('HOSTDB'), user=os.getenv('USERDB'),  password = os.getenv('PASSDB'), db=os.getenv('DBDB'), ) 
#cursor = conn.cursor()
#query = "INSERT INTO tablename (text_for_field1, text_for_field2, text_for_field3, text_for_field4) VALUES (%s, %s, %s, %s)"
#cursor.execute(query, (field1, field2, field3, field4))
#conn.commit()
#cursor.close()
#conn.close()



#Encryption methods
def encrypt(text):
    #hash text
    # converting password to array of bytes 
    bytes = text.encode('utf-8') 
  
    # generating the salt 
    salt = bcrypt.gensalt() 
  
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    return hash


def comparePasswords(password, DBvalue):
    #compare user input to value in database
    DBvalue = DBvalue.encode('utf-8')
    password = password.encode('utf-8')
    result = bcrypt.checkpw(password, DBvalue) 
    
    return result



  

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
Auth = Blueprint("Auth",__name__)

def OpenConnection():
    #mysql connection config
    conn = pymysql.connect( 
            host=os.getenv('HOSTDB'), 
            user=os.getenv('USERDB'),  
            password = os.getenv('PASSDB'), 
            db=os.getenv('DBDB'), 
            ) 
    return conn

#route that handles login and notifies website
@Auth.route("/Login", methods=('POST',))
def login():

    conn =  OpenConnection()

    #get request info
    req = request.get_json()
    UserName = req['UserName']
    Password = req['Password']
    print(UserName)
    
    cur = conn.cursor()
    #query for logging user in 
    query_string = "SELECT * FROM Users WHERE UserName = %s"

    #query execute
    cur.execute(query_string,[UserName])
    dat = cur.fetchone()
    data = {}
    if(dat):#if user info is correct
        
        
        if(comparePasswords(Password,dat[1])):
            data = {
                "Login": "True",
                "Token":jwt.encode({'user':UserName, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=10)}, os.getenv('SECRETKEY')),
                "User": {
                    "UserName": dat[0],
                    "FirstName": dat[2],
                    "LastName": dat[3],
                    "Email": dat[4],
                    "AccountType": dat[5],
                    "OrgName": dat[6],
                }
            }
        
        
    
        
    else:#if user info is not correct
        data = {
            "Login": "False",
        }

    cur.close()
    conn.close()
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

    #request info
    conn =  OpenConnection()
    req = request.get_json()
    OrgName = req['OrgName']
    UserName = req['UserName']
    Password = req['Password']
    FirstName = req['FirstName']
    LastName = req['LastName']
    Email = req['Email']
    #hash password
    Password = encrypt(Password)

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

        sql = "INSERT INTO Users (UserName, Password, FirstName, LastName, Email, AccountType, Organization) VALUES (%s, %s,%s, %s,%s, %s,%s)"
        val = [UserName, Password, FirstName, LastName, Email, "Owner", OrgName]
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
        insertUser.close()
        insertOrg.close()

    #json object response
    cur.close()
    cur1.close()
    conn.close()
    return jsonify(data)

@Auth.route("/RegisterUser", methods=('POST',))
def RegUser():
    data = {
        "Registered": "False"
    }
    #request input
    #{
    #   +--------------+--------------+------+-----+---------+-------+
    #   +DB Layout
    #   +--------------+--------------+------+-----+---------+-------+
    #   | Field        | Type         | Null | Key | Default | Extra |
    #   +--------------+--------------+------+-----+---------+-------+
    #   | UserName     | varchar(100) | NO   | PRI | NULL    |       |
    #   | Password     | varchar(100) | NO   |     | NULL    |       |
    #   | FirstName    | varchar(100) | NO   |     | NULL    |       |
    #   | LastName     | varchar(100) | NO   |     | NULL    |       |
    #   | Email        | varchar(100) | NO   |     | NULL    |       |
    #   | AccountType  | varchar(100) | NO   |     | NULL    |       |
    #   | Organization | varchar(100) | NO   |     | NULL    |       |
    #   +--------------+--------------+------+-----+---------+-------+
    #}

    #request info
    conn =  OpenConnection()
    req = request.get_json()
    if not req:
        return jsonify(data)

    Organization = req['OrgName']
    UserName = req['UserName']
    Password = req['Password']
    FirstName = req['FirstName']
    LastName = req['LastName']
    Email = req['Email']
    AccountType = "User"
    Password = encrypt(Password)

    cur = conn.cursor()
    # Ensure that org Exists
    query_string = "SELECT * FROM Users WHERE Organization = %s;"

    #query execute
    cur.execute(query_string,[Organization])

    valid_org_rows = cur.fetchall()
    
    if not valid_org_rows:
        # Valid org does not exist
        data['Reason'] = "Passed Organization isn't valid"
        return jsonify(data)

    row_objs = [UserObj(item) for item in valid_org_rows]

    for row_obj in row_objs:
        if UserName == row_obj.UserName:
            # User exists
            data['Reason'] = "User already exists"
            return jsonify(data)


    sql = "INSERT INTO Users (UserName, Password, FirstName, LastName, Email, AccountType, Organization) VALUES (%s, %s,%s, %s,%s, %s,%s)"
    val = [UserName, Password, FirstName, LastName, Email, AccountType, Organization]
    cur.execute(sql, val)

    conn.commit()

    cur.close()
    conn.close()
    data = {
        "Registered": "True"
    }
    return jsonify(data)
