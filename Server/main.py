from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv, dotenv_values
import pymysql

load_dotenv()#loading env variables
app = Flask(__name__)

#pymysql
conn = pymysql.connect( 
        host=os.getenv('HOST'), 
        user=os.getenv('USER'),  
        password = os.getenv('PASS'), 
        db=os.getenv('DB'), 
        ) 


#mysql configuration


@app.route("/")
def home():
    return "Home"

@app.route("/getRequest")
def getdata():
    data = {
        "name":"david"
    }
    return jsonify(data)

@app.route("/Login", methods=('POST',))
def login():
    req = request.get_json()
    UserName = req['UserName']
    Password = req['Password']
    print(UserName)
    cur = conn.cursor() 
    query_string = "SELECT * FROM Users WHERE UserName = %s AND Password = %s"

    cur.execute(query_string,[UserName, Password])
    dat = cur.fetchall()

    if(dat):
        data = {
            "Login": "True",
            "Token":"token"
        }
    else:
        data = {
            "Login": "False",
        }

    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)