from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "a super secret, secret key"

def encode_token(costumer_id): #using unique pieces of info to make our tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), #Setting the expiration time to an hour past now. Expiration
        'iat': datetime.now(timezone.utc), #Issued at 
        'sub':  str(costumer_id) #This needs to be a string or the token will be malformed and won't be able to be decoded. subject of the token, the unique identifier for the user. In this case, we are using the costumer_id as the subject of the token.
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

#This is a decorator function that can be used to protect routes that require authentication. It checks for the presence of a token in the Authorization header, decodes it, and retrieves the user ID from the token's payload. If the token is missing, expired, or invalid, it returns an appropriate error message.

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
            if len(parts) == 2:
                token = parts[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            kwargs["current_costumer_id"] = data["sub"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jose.exceptions.JWTError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated
