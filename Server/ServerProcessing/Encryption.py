import bcrypt

def encrypt(text):
    # converting password to array of bytes 
    bytes = text.encode('utf-8') 
  
    # generating the salt 
    salt = bcrypt.gensalt() 
  
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    return hash


def comparePasswords(password, DBvalue):
    password = password.encode('utf-8')
    result = bcrypt.checkpw(password, DBvalue) 
    return result


  
