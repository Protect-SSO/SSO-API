import jwt

key = "secrete"

encoded = jwt.encode({"user": "dvana1"}, key, algorithm="HS256")

print(encoded)