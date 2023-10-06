from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv, dotenv_values
import pymysql
from Auth import Auth

load_dotenv()#loading env variables
app = Flask(__name__)
app.register_blueprint(Auth,url_prefix='/Auth')#blueprint for auth routes

#pymysql config
conn = pymysql.connect( 
        host=os.getenv('HOSTDB'), 
        user=os.getenv('USERDB'),  
        password = os.getenv('PASSDB'), 
        db=os.getenv('DBDB'), 
        ) 

#home route used for testing
@app.route("/")
def home():
    return "Home"


if __name__ == '__main__':
    app.run(debug=True)