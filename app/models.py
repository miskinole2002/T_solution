from pydantic import BaseModel
from sqlmodel import SQLModel,Field

# creation des classes

      #Table Appartements
class Appartements(SQLModel,table=True):
    __tablename__="Appartement"

    id_App : int = Field(primary_key=True)
    N_App : str
    Superficie: str
    type:str
    etage:str
    Status:str

# table Locataire 
class Locataire(SQLModel,table=True):
    __tablename__="Locataires"

    id:int=Field(primary_key=True)
    Nom: str
    Prenom:str
    Tel:str
    Email:str
  #table user pour les administrateurs 
class User(SQLModel,table=True):

    __tablename__="Users"
    id:int=Field(primary_key=True)
    Nom: str
    Prenom:str
    Email:str
    Role:str

