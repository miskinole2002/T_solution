from pydantic import BaseModel
from sqlmodel import SQLModel,Field

# creation des classes

class Appartements(SQLModel,table=True):
    __tablename__="Appartement"

    id_App : int = Field(primary_key=True)
    N_App : str
    Superficie: str
    type:str
    etage:str
    Status:str