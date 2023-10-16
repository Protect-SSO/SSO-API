from functools import wraps
import jwt
import datetime
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

#where it gets passed into:
app.config['KEY']='testkey'

#token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token= request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}),403

        try:
            data = jwt.decode(token, app.config['KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}),403
        
        return f(*args,**kwargs)
    return decorated

#routes
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is available for people with valid tokens'})

@app.route('/login')
def login():
    auth = request.authorization
    #if successful:
    if auth and auth.password=='password':
        token=jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=5)}, app.config['KEY'])
        return jsonify({'token' :token.decode('UTF-8')})
    return make_response('Could not verify',401,{'www-authenticate':'Basic realm="Login required"'})

if __name__=='__main__':
    app.run(debug=True)
    