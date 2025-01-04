from fastapi import FastAPI,Request,Depends,Form,status
from fastapi.templating import Jinja2Templates
import models
from database import engine,sessionlocal
from sqlalchemy.orm import Session,declarative_base
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name = "static")

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
    
@app.post("/add")
async def add(request: Request, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    user = models.User(name=name, description=description,)
    db.add(user)
    db.commit()
    db.refresh(user)  # Ensure the created user has all data, including timestamps
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER) 

@app.get("/addnew") 
async def addnew(request:Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})

@app.post("/update/{user_id}")
async def update(request: Request, user_id: int, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.name = name
        user.description = description
        db.commit()  # The `updated_at` will be updated automatically
        db.refresh(user)
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)