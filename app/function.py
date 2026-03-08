from passlib.context import CryptContext
from sqlalchemy import text

context=CryptContext(schemes=["pbkdf2_sha256","des_crypt"],deprecated="auto")

def password_hash(password):

    return context.hash(password) 

def password_verify(password,hash_password):

    return context.verify(password,hash_password)

def all_appartement(session):

    sql=text("select* from Appartement") 
    cursor=session.execute(sql)
    result=cursor.fetchall()

    return result