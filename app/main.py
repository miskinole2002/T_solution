from fastapi import FastAPI, Request, Depends, Form
from typing import Annotated
from sqlalchemy import text
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models import Appartements, User, Locataire
import sys, os
from sqlmodel import SQLModel, create_engine, Session
from .function import (
    password_hash,
    password_verify,
    Add_appartement,
    all_appartement,
    appartement_one,
    del_Appartement,
    upd_Appartement_one,
    update_Appartement,
    all_Locataires,
    Locataire_one,
    Add_Locataires,
    locataire_Update,
    upd_locataire_one,
    get_admin_by_Mail,
    Add_Admin,
    get_all_admin,get_User_By_Email
    
)
from starlette.middleware.sessions import SessionMiddleware


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
app = FastAPI()
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
templates = Jinja2Templates(directory=templates_dir)
#static
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"static"))
app.mount("/static",StaticFiles(directory=static_dir), name="static")


app.add_middleware(SessionMiddleware, secret_key="1234")

# connection a la base de donne sql server

url = "mssql+pyodbc://(LocalDB)\\MSSQLLocalDB/Tsolution?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(url)


# ouvre et ferme automatique une session de la BD
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
async def home_page(session: SessionDep, request: Request):
    User = request.session.get("user")
    if User:
        return templates.TemplateResponse("home.html", {"request": request, "U": User})

    return templates.TemplateResponse("home.html", {"request": request})


# connexion
@app.get("/login")
async def home_page(request: Request):
    error = request.session.get("error", None)
    if error:
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": error}
        )

    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def home_page(
    session: SessionDep,
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):

    # if not email or not password:
    #     request.session["error"] = "veuillez remplir tout les champs svp"
    #     return RedirectResponse(url='/login', status_code=302)

    result=get_User_By_Email(session,email)
    
    if result:
        R= password_verify(password,result[5])
        if R:
            S = {
                "user_id": result[0],
                "nom": result[1],
                "prenom": result[2],
                "Email": result[3],
                "role": result[4],
            }
            request.session["user"] = S

            return RedirectResponse(url="/dashboard", status_code=302)
        else:
            
            return templates.TemplateResponse("login.html", {"request": request, "error": "mot de passe incorect"}
    )

         

    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "email introuvable"})
      


@app.get("/dashboard")
async def dashboard(session: SessionDep, request: Request):
    User = request.session.get("user")
    error = request.session.pop("error", None)
    result = all_appartement(session) # retourne un tableau de tous les appartements 
    result_locataire=all_Locataires(session) # retourne un tableau de tous les locataires
    result_admin=get_all_admin(session)# retourne un tableau d administrateur
    
    if error:
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "U": User, "A": result, "error": error,"C":result_admin}
        )

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "U": User,"B": result_locataire, "A": result,"C":result_admin}
    )

# ajouter un appartement

@app.post("/add_App")
async def add_App(
    session: SessionDep,
    request: Request,
    N_App: str = Form(...),
    etage: str = Form(...),
    Superficie: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),):

    User = request.session.get("user")
    if not N_App or not etage or not Superficie or not type or not status:
        request.session["error"] = (
            "assurez vous que tous les champs soient remplis svp "
        )
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        r = appartement_one(session, N_App)
        if r:
            request.session["error"] = "cet Appartement a deja ete enregistre  "
            return RedirectResponse(url="/dashboard", status_code=302)

        else:
            Add_appartement(session,N_App,etage,Superficie,type,status)
            return RedirectResponse(url="/dashboard", status_code=302)

   


# modifier un appartement
@app.post("/update_App")
async def update_App(
    session: SessionDep,
    request: Request,
    id_App: str = Form(...),
    N_App: str = Form(...),
    etage: str = Form(...),
    Superficie: str = Form(...),
    type: str = Form(),
    status: str = Form(...),
):
    
    User = request.session.get("user")
    update_Appartement(session,id_App,N_App,etage,Superficie,type,status,)  
    return RedirectResponse(url="/dashboard", status_code=302)

#delete un Appartement
@app.get("/delete_App/{id_App}")
async def delete_App(session: SessionDep, request: Request, id_App: str):

    user = request.session.get("user")
   
    upd_Appartement_one(session,id_App)

    return RedirectResponse(url="/dashboard", status_code=302)

#ajouter un locataire 
@app.post("/add_locataire")
async def add_locataire(session:SessionDep, request:Request,Nom:str=Form(...),
            
      Prenom:str=Form(...),
      Tel:str=Form(...),
      Email:str=Form(...),
      NumeroRue:str=Form(None),
      Rue:str=Form(None),
      NumeroApp:str=Form(None),
      ville:str=Form(None),
      province:str=Form(None),
      code:str=Form(None)
 ):
        
        result=Locataire_one(session,Email)
        if result:
            request.session["error"] = "ce Locataire a deja ete enregistre  "
            return RedirectResponse(url="/dashboard", status_code=302)
        else:
            Add_Locataires(session,Nom,Prenom, Tel,Email,NumeroRue,Rue,NumeroApp,ville,province,code)
        return RedirectResponse(url="/dashboard", status_code=302)
#modifier un locataire
@app.post("/update_locataire")
async def update_locataire(session:SessionDep, request:Request,id:str=Form(...),Nom:str=Form(...),
            
      Prenom:str=Form(...),
      Tel:str=Form(...),
      Email:str=Form(...),
      NumeroRue:str=Form(None),
      Rue:str=Form(None),
      NumeroApp:str=Form(None),
      ville:str=Form(None),
      province:str=Form(None),
      code:str=Form(None)
 ):
    
    locataire_Update(session,id,Nom,Prenom,Tel,Email,NumeroRue,Rue,NumeroApp,ville,province,code)

    return RedirectResponse(url="/dashboard", status_code=302)


#delete un Locataire
@app.get("/delete_Loc/{id}")
async def delete_App(session: SessionDep, request: Request, id: str):

    user = request.session.get("user")
    # print(id_App)
    upd_locataire_one(session,id)

    return RedirectResponse(url="/dashboard", status_code=302)

#creer un bail
@app.post("/Create_Bail")
async def create_Bail(session:SessionDep, request:Request,
                      Nom_Locataire:str=Form(...),
                      N_App:str=Form(...),
                      date_debut:str=Form(...),
                      date_fin:str=Form(...),
                      prix:str=Form(...),
                      Statut:str=Form(...)
                      ):
    
    print(date_debut)

    
    return RedirectResponse(url="/dashboard", status_code=302)

#ajouter un administrateur
@app.post("/add_Admin")
async def add_Admin(
    session: SessionDep,
    request: Request,
    Nom: str = Form(...),
    Prenom: str = Form(...),
    Password: str = Form(...),
    Email:str=Form(...),
    Role: str = Form(...),
    ):
    print(Role)
    print(Password)

    User = request.session.get("user")
    if not Nom or not Prenom or not Password or not Role or not Email:
        request.session["error"] = (
            "assurez vous que tous les champs soient remplis svp "
        )
        return RedirectResponse(url="/dashboard", _code=302)
    else:
        r =get_admin_by_Mail(session, Email)
        if r:
            request.session["error"] = "cet utilisateur a deja ete enregistre  "
            return RedirectResponse(url="/dashboard", status_code=302)

        else:
            password=password_hash(Password)
            print(password)
            Add_Admin(session,Nom,Prenom,Email,Role,password)
            return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/")
    request.session.clear()
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, workers=1)
