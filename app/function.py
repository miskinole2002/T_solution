from passlib.context import CryptContext
from sqlalchemy import text

context=CryptContext(schemes=["pbkdf2_sha256","des_crypt"],deprecated="auto")

def password_hash(password):

    return context.hash(password) 

def password_verify(password,hash_password):

    return context.verify(password,hash_password)

#slectionne tous les appartements 
def all_appartement(session):

    sql=text("select* from Appartement") 
    cursor=session.execute(sql)
    result=cursor.fetchall()

    return result

#selectionne un appartement 
def appartement_one(session,Numero):
     
    sql=text("select* from Appartement where N_App=:N_App")
    params={"N_App":Numero}
    cursor=session.execute(sql,params)
    result=cursor.fetchone()
    return result

#delete un appartement 
def del_Appartement(session,id):
    sql=text("delete from Appartement Where id_App=:id_App")
    params={"id_App":id}
    session.execute(sql,params)
    session.commit()

    