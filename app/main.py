from fastapi import FastAPI,Request,Depends,Form
from typing import Annotated
from sqlalchemy import text
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models import Appartements,User,Locataire
import sys,os
from sqlmodel import SQLModel,create_engine,Session
from .function import password_hash,password_verify,all_appartement
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
#   sql =text("SELECT * FROM Appartement")
#     x=session.execute(sql)

#     users = x.fetchall()

#     print(users)

@app.get("/")
async def home_page(session: SessionDep, request:Request):
    User=request.session.get("user")
    if User:
        return templates.TemplateResponse("home.html",{"request":request,"U":User})
  
    return templates.TemplateResponse("home.html",{"request":request})

#connexion
@app.get("/login")
async def home_page(request:Request):
    error= request.session.get('error',None)
    if error :
        return templates.TemplateResponse("login.html",{"request":request, "error":error})

    return templates.TemplateResponse("login.html",{"request":request})

@app.post("/login")
async def home_page(session: SessionDep, request:Request,email:str=Form(...), password:str=Form(...) ):
     
    # if not email or not password: 
    #     request.session["error"] = "veuillez remplir tout les champs svp"
    #     return RedirectResponse(url='/login', status_code=302)
    
    sql=text("select* from Users where email=:email")
    params={"email":email}
    cursor=session.execute(sql,params)
    result=cursor.fetchone()
    
    if result:
       
        # R= password_verify(password,result[1])
        S={
            "user_id":result[0],
            "nom":result[1],
            "prenom":result[2],
            "Email":result[3],
            "role":result[4]
          }
        
        request.session["user"]=S

        return RedirectResponse(url='/dashboard',status_code=302)


    else:
        request.session["error"]="email introuvable"
        return RedirectResponse(url='/login', status_code=302)

    

@app.get("/dashboard")
async def dashboard(session: SessionDep, request:Request):
    User=request.session.get("user")
    result=all_appartement(session) 
    


    return templates.TemplateResponse("dashboard.html",{"request":request, "U":User, "A":result})
 
#ajouter un appartement 


@app.post("/add_App")
async def add_App(session:SessionDep ,request:Request,N_App:str=Form(...),etage:str=Form(...),Superficie: str=Form(...),type:str=Form(),status:str=Form(...)):

    User=request.session.get("user")

    sql = text("INSERT INTO Appartement (N_App, etage, Superficie, type, status) VALUES (:N_App, :etage, :Superficie, :type, :status)")

    params = {
        "N_App": N_App,
        "etage": etage,
        "Superficie": Superficie,
        "type": type,
        "status": status
            }

    session.execute(sql, params)
    session.commit()  


    return templates.TemplateResponse("dashboard.html",{"request":request, "U":User})

# modifier un appartement 
@app.post("/update_App")
async def update_App(session:SessionDep ,request:Request,N_App:str=Form(...),etage:str=Form(...),Superficie: str=Form(...),type:str=Form(),status:str=Form(...)):

    User=request.session.get("user")
    sql = text("UPDATE Appartement SET etage = :etage, Superficie = :Superficie, type = :type, status = :status WHERE N_App = :N_App")

    params = {
    "N_App": N_App,
    "etage": etage,
    "Superficie": Superficie,
    "type": type,
    "status": status
    }

    session.execute(sql, params)
    session.commit()

    return templates.TemplateResponse("dashboard.html",{"request":request, "U":User})












@app.get("/logout")
async def logout(request:Request):
    response=RedirectResponse(url='/')
    request.session.clear()
    return response

   

   

   
    

if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8001, workers=1)