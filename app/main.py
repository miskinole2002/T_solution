from fastapi import FastAPI,Request,Depends
from typing import Annotated
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models import Appartements
import sys,os
from sqlmodel import SQLModel,create_engine,Session


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
app=FastAPI()
templates_dir= os.path.abspath(os.path.join(os.path.dirname(__file__),"template"))
templates=Jinja2Templates(directory=templates_dir)

#connection a la base de donne sql server

url="mssql+pyodbc://(LocalDB)\\MSSQLLocalDB/Tsolution?driver=ODBC+Driver+17+for+SQL+Server" 
engine= create_engine(url)

#ouvre et ferme automatique une session de la BD
def get_session():
     with Session(engine) as session:
          yield session

SessionDep=Annotated[Session,Depends(get_session)]

# users=SessionDep.query(Appartements).filter(Appartements.N_App=="303").first()
# print(users)




@app.get("/")
def home_page(session: SessionDep):
 
    x=session.exec(select(Appartements)).all()
    print(x)

    return x

   

   
    return 

if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8001, workers=1)