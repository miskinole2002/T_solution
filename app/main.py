from fastapi import FastAPI,Request,Depends,Form
from typing import Annotated
from sqlalchemy import text
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models import Appartements,User,Locataire
import sys,os
from sqlmodel import SQLModel,create_engine,Session,select
from .securite import password_hash,password_verify 
from starlette.middleware.sessions import SessionMiddleware 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
app=FastAPI()
templates_dir= os.path.abspath(os.path.join(os.path.dirname(__file__),"templates"))
templates=Jinja2Templates(directory=templates_dir)

app.add_middleware(SessionMiddleware,secret_key="1234")

#connection a la base de donne sql server

url="mssql+pyodbc://(LocalDB)\\MSSQLLocalDB/Tsolution?driver=ODBC+Driver+17+for+SQL+Server" 
engine= create_engine(url)

#ouvre et ferme automatique une session de la BD
def get_session():
     with Session(engine) as session:
          yield session 

SessionDep=Annotated[Session,Depends(get_session)]



# x=SessionDep.execute(select(User)).all()
#     print(x)


@app.get("/")
async def home_page(session: SessionDep, request:Request):
    sql =text("SELECT * FROM Appartement")
    x=session.execute(sql)

    users = x.fetchall()

    print(users)
    return templates.TemplateResponse("home.html",{"request":request})

#connexion
@app.get("/login")
async def home_page(request:Request):
    error= request.session.get('error',None)
    if error :
        return templates.TemplateResponse("login.html",{"request":request, "error":error})

    return templates.TemplateResponse("login.html",{"request":request})

@app.post("/login")
async def home_page(session: SessionDep, request:Request,Email:str=Form(...), password:str=Form(...) ):

    if not Email or not password: 
        request.session["error"] = "veuillez remplir tout les champs svp"
        return RedirectResponse(url='/login', status_code=302)
    return templates.TemplateResponse("login.html",{"request":request})


@app.get("/dashboard")
async def dashboard(session: SessionDep, request:Request):

    return templates.TemplateResponse("dashboard.html",{"request":request})
 
    


   

   

   
    

if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8001, workers=1)