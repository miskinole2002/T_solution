from passlib.context import CryptContext
from sqlalchemy import text

context=CryptContext(schemes=["pbkdf2_sha256","des_crypt"],deprecated="auto")

def password_hash(password):

    return context.hash(password) 

def password_verify(password,hash_password):

    return context.verify(password,hash_password)
#ajouter un appartement
def Add_appartement(session,N_App,etage,Superficie,type,status):
        sql = text(
                "INSERT INTO Appartement (N_App, etage, Superficie, type, status,is_Delete) VALUES (:N_App, :etage, :Superficie, :type, :status,:is_Delete)"
            )

        params = {
                "N_App": N_App,
                "etage": etage,
                "Superficie": Superficie,
                "type": type,
                "status": status,
                "is_Delete":0
            }
        
        session.exec(sql, params=params)
        session.commit()

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
    cursor=session.exec(sql,params=params)
    result=cursor.fetchone()
    return result

#delete un appartement 
def del_Appartement(session,id):
    sql=text("delete from Appartement Where id_App=:id_App")
    params={"id_App":id}
    session.execute(sql,params)
    session.commit()

#delete mais modifie plutot la colone is delete de notre table
def upd_Appartement_one(session, id):
    sql = text(
        "UPDATE Appartement SET is_Delete= :is_Delete WHERE id_App = :id_App"
    )

    params = {
        "id_App":id,
      "is_Delete":1
    }

    session.exec(sql, params=params)
    session.commit()

 # fonction qui modifie un appartement    
def update_Appartement(session, id,N_App,etage,Superficie,type,status):
        sql = text(
        "UPDATE Appartement SET N_App=:N_App, etage = :etage, Superficie = :Superficie, type = :type, status = :status WHERE id_App = :id_App"
    )

        params = {
        "id_App": id,
        "N_App": N_App,
        "etage": etage,
        "Superficie": Superficie,
        "type": type,
        "status": status,
        }
        session.exec(sql, params=params)
        session.commit()
# selectionner tous les locataires 
def all_Locataires(session):

    sql=text("select* from Locataires where is_Delete=:is_Delete") 
    params={"is_Delete":0}
    cursor=session.exec(sql,params=params)
    result=cursor.fetchall()
 


    return result

def Add_Locataires(session,Nom,Prenom, Tel,Email,NumeroRue,Rue,NumeroApp,ville,province,code):
         sql = text(
                "INSERT INTO Locataires (Nom, Prenom,Tel,Email,NumeroRue,Rue,NumeroApp,ville,province,code,is_Delete) VALUES (:Nom, :Prenom,:Tel,:Email,:NumeroRue,:Rue,:NumeroApp,:ville,:province,:code,:is_Delete)"
            )

         params = {
                "Nom": Nom,
                "Prenom": Prenom,
                "Tel": Tel,
                "Email": Email,
                "NumeroRue": NumeroRue,
                "Rue":Rue,
                "NumeroApp":NumeroApp,
                "ville":ville,
                "province":province,
                "code":code,
                "is_Delete":0 
            }
        
         session.exec(sql, params=params)
         session.commit()

def Locataire_one(session,email):
    sql=text("select* from Locataires where Email=:Email")
    params={"Email":email}
    cursor=session.execute(sql,params)
    result=cursor.fetchone()
    return result

#modifier un locataire 

def locataire_Update(session,id,Nom,Prenom,Tel,Email,NumeroRue,Rue,NumeroApp,ville,province,code):
     
        sql = text(
        "UPDATE Locataires SET Nom=:Nom, Prenom = :Prenom, Tel =:Tel, Email = :Email, NumeroRue = :NumeroRue,Rue =:Rue," 
        " NumeroApp=:NumeroApp,ville=:ville, province=:province, code=:code  WHERE id= :id"
    )

        params = {
        "id": id,
         'Nom':Nom, 
         'Prenom'  :Prenom, 
        'Tel':Tel, 
         "Email"  :Email, 
         "NumeroRue" :NumeroRue,
         "Rue" :Rue,
        "NumeroApp":NumeroApp,
        "ville":ville, 
        "province":province, 
        "code":code
        }
        session.exec(sql, params=params)
        session.commit()

#agir comme un delete mais modifie plutot la colone is delete de notre table
def upd_locataire_one(session, id):
    sql = text(
        "UPDATE Locataires SET is_Delete= :is_Delete WHERE id = :id"
    )

    params = {
        "id":id,
      "is_Delete":"1"
    }
    session.exec(sql, params=params)
    session.commit()

def get_id_App_by_name():
      return 
#creer un Bail

def Bail_Create(session, Nom_Locataire, N_App, date_debut, date_fin, prix,Statut):
         sql = text(
                "INSERT INTO Locataires (id,id_App,Nom_Locataire, N_App, date_debut, date_fin, prix,Statut,is_Delete) " \
                "VALUES (:Nom_Locataire, :N_App, :date_debut, :date_fin, :prix,:Statut,:is_Delete)"
            )

         params = {
                "Nom": Nom,
                "Prenom": Prenom,
                "Tel": Tel,
                "Email": Email,
                "NumeroRue": NumeroRue,
                "Rue":Rue,
                "NumeroApp":NumeroApp,
                "ville":ville,
                "province":province,
                "code":code,
                "is_Delete":0 
            }
        
         session.exec(sql, params=params)
         session.commit()
