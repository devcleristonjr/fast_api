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

# Endpoints para backend (Insomnia)

# Endpoint para criar uma nova tarefa via POST
@app.post("/tasks/create")
async def create_task(taskItem: TaskItem, db: Session = Depends(get_db)):
    task = models.Task(
        name=taskItem.name,
        description=taskItem.description,
        progress=taskItem.progress
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"message": "Task created successfully", "task": task}

# Endpoint para listar todas as tarefas
@app.get("/tasks")
async def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.desc()).all()
    return {"tasks": tasks}

# Endpoint para atualizar uma tarefa existente
@app.put("/tasks/update/{task_id}")
async def update_task(task_id: int, taskItem: TaskItem, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    task.name = taskItem.name
    task.description = taskItem.description
    task.progress = taskItem.progress
    db.commit()
    db.refresh(task)

    return {"message": "Task updated successfully", "task": task}

# Endpoint para deletar uma tarefa
@app.delete("/tasks/delete/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Endpoint para visualizar uma tarefa específica pelo ID
@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    return {"task": task}

# Endpoints para front-end

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
    task = models.Task(
        name=name, 
        description=description, 
        progress=progress
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
    
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": task})

# Rota para exibir o formulário de edição de um tasks
@app.get("/edit/{task_id}")
async def edit(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "task": task})

# Rota para atualizar os dados de um tasks
@app.post("/update/{task_id}")
async def update(request: Request, task_id: int, name: str = Form(...), description: str = Form(...), progress: str = Form(...), method: str = Form(None), db: Session = Depends(get_db)):
    if method == 'put':  # Verifica se estamos simulando o PUT
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if task:
            task.name = name
            task.description = description
            task.progress = progress
            db.commit()
            db.refresh(task)

        return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

    return {"error": "Invalid method"}
# Rota para excluir um tasks
@app.delete("/remove/{task_id}")
async def remove(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(task)
    db.commit() 
    
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)