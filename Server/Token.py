from flask import Blueprint, render_template, request, jsonify
import pymysql
import os, json
from dotenv import load_dotenv, dotenv_values
from dataclasses import dataclass
import jwt
import datetime


load_dotenv()#loading env variables
Token = Blueprint("Token",__name__)

@Token.route("/decode_token", methods=('POST',))
def decode_token_route():
    #request info
    req = request.get_json()
    Token = req['Token']
    try:
        decoded_data=jwt.decode(jwt=Token,key=os.getenv('SECRETKEY'),algorithms=['HS256'])
        return jsonify(decoded_data)
    except jwt.DecodeError:
        return jsonify({
            "error":'Invalid token'
        })
    except jwt.ExpiredSignatureError:
        return jsonify({
            "error":"expired" 
        })
    