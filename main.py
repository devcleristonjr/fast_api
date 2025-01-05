from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class TaskItem(BaseModel):
    id: int | None = None
    name: str
    description: str
    created_at: str | None = None
    updated_at: str | None = None
    progress: str

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Rota principal que exibe a lista de tasks
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.desc()).all()

    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Rota para adicionar um novo tasks
@app.post("/add")
async def add(
        request: Request, 
        name: str = Form(...),
        description: str = Form(...),
        progress: str = Form(...),
        db: Session = Depends(get_db)
    ):
    """ Teste de texto no docs"""
    
    task = models.Task(
        name=name, 
        description=description, 
        progress=progress
    )

    db.add(task) 
    db.commit() 
    db.refresh(task) 

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# Rota para adicionar um novo task (para mostrar uso do Pydantic)
@app.post("/add_via_post")
async def add(
        request: Request, 
        taskItem: TaskItem,
        db: Session = Depends(get_db)
    ):
    
    task = models.Task(
        name=taskItem.name, 
        description=taskItem.description, 
        progress=taskItem.progress
    )

    db.add(task) 
    db.commit() 
    db.refresh(task) 

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# Rota para exibir o formulário de adição de novo tasks
@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

# Rota para exibir os detalhes de um tasks
@app.get("/task/{task_id}")
async def get_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return templates.TemplateResponse("task_not_found.html", {"request": request, "task_id": task_id})
    
    print(f"Task data: {task}")
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": task})

# Rota para exibir o formulário de edição de um tasks
@app.put("/edit/{task_id}")
async def edit(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    return templates.TemplateResponse("edit.html", {"request": request, "task": task})

# Rota para atualizar os dados de um tasks
@app.put("/update/{task_id}")
async def update(request: Request, task_id: int, name: str = Form(...), description: str = Form(...), progress: str = Form(...), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.name = name
        task.description = description
        task.progress = progress
        
        db.commit()
        db.refresh(task)

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# Rota para excluir um tasks
@app.delete("/delete/{task_id}")
async def delete(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(task)
    db.commit() 
    
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
