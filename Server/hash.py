import bcrypt

def hash_password(password):
    #generate salt
    password_salt=bcrypt.gensalt()

    #salt the password
    hashed_password=bcrypt.hashpw(password.encode('utf-8'),password_salt)

    return hashed_password,password_salt

def verify_password(password,hashed_password,salt):
    #compare the two passwords
    new_hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)

    return new_hashed_password == hashed_password