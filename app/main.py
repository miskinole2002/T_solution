from fastapi import FastAPI,Request,Depends
from typing import Annotated
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models import Appartements,User,Locataire
import sys,os
from sqlmodel import SQLModel,create_engine,Session,select
from .securite import password_hash,password_verify 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
app=FastAPI()
templates_dir= os.path.abspath(os.path.join(os.path.dirname(__file__),"templates"))
templates=Jinja2Templates(directory=templates_dir)

#connection a la base de donne sql server

url="mssql+pyodbc://(LocalDB)\\MSSQLLocalDB/Tsolution?driver=ODBC+Driver+17+for+SQL+Server" 
engine= create_engine(url)

#ouvre et ferme automatique une session de la BD
def get_session():
     with Session(engine) as session:
          yield session 

SessionDep=Annotated[Session,Depends(get_session)]



# x=session.exec(select(User)).all()
#     print(x)


@app.get("/")
async def home_page(session: SessionDep, request:Request):

    return templates.TemplateResponse("home.html",{"request":request})

@app.get("/login")
async def home_page(session: SessionDep, request:Request):

    return templates.TemplateResponse("login.html",{"request":request})

@app.get("/dashboard")
async def dashboard(session: SessionDep, request:Request):

    return templates.TemplateResponse("dashboard.html",{"request":request})
 
    

   

   

   
    

if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8001, workers=1)