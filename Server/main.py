from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv, dotenv_values
import pymysql
from Auth import Auth
from Token import Token
from AppServices import AppServices

load_dotenv()#loading env variables
app = Flask(__name__)
app.register_blueprint(Auth,url_prefix='/Auth')#blueprint for auth routes
app.register_blueprint(Token,url_prefix='/Token')#blueprint for auth routes
app.register_blueprint(AppServices,url_prefix='/AppServices')#blueprint for auth routes


#home route used for testing
@app.route("/")
def home():
    return "Home"


if __name__ == '__main__':
    app.run(debug=True)