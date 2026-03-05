from fastapi import FastAPI,Request
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
app=FastAPI()
templates_dir= os.path.abspath(os.path.join(os.path.dirname(__file__),"template"))
templates=Jinja2Templates(directory=templates_dir)

@app.get("/")
async def home_page(request:Request):
   

   
    return templates.TemplateResponse("base.html",{"request":request })

if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000, workers=1)