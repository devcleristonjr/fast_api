# Importando as bibliotecas necessárias do FastAPI, SQLAlchemy e outras
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session, declarative_base
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum

# Importando o modelo ProgressStatus de models
from models import ProgressStatus

# Criando as tabelas no banco de dados com base nos modelos
models.Base.metadata.create_all(bind=engine)

# Configurando a renderização dos templates com Jinja2
templates = Jinja2Templates(directory="templates")

# Inicializando a aplicação FastAPI
app = FastAPI()

# Configurando o acesso aos arquivos estáticos (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Função que retorna uma sessão de banco de dados
def get_db():
    db = sessionlocal()  # Cria uma sessão de banco de dados
    try:
        yield db  # Retorna a sessão para ser usada nas rotas
    finally:
        db.close()  # Fecha a sessão após o uso

# Rota principal que exibe a lista de usuários
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # Consultando todos os usuários ordenados por ID
    users = db.query(models.User).order_by(models.User.id.desc()).all()
    # Retorna o template index.html com a lista de usuários
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

# Rota para adicionar um novo usuário
@app.post("/add")
async def add(request: Request, name: str = Form(...), description: str = Form(...), progress: ProgressStatus = Form(...), db: Session = Depends(get_db)):
    # Criando um novo usuário com os dados fornecidos
    user = models.User(name=name, description=description, progress=progress)
    db.add(user)  # Adiciona o usuário ao banco de dados
    db.commit()  # Commit da transação para salvar no banco
    db.refresh(user)  # Atualiza o objeto para garantir que ele tenha todos os dados (como timestamps)
    # Redireciona para a página principal
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# Rota para exibir os detalhes de um usuário
@app.get("/user/{user_id}")
async def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    # Buscando o usuário no banco de dados
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        # Se o usuário não for encontrado, retorna a página de erro
        return templates.TemplateResponse("user_not_found.html", {"request": request, "user_id": user_id})
    # Log para verificar os dados do usuário (utilizado para debugging)
    print(f"User data: {user}")
    # Retorna o template com os detalhes do usuário
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})

# Rota para exibir o formulário de adição de novo usuário
@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

# Rota para exibir o formulário de edição de um usuário
@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    # Buscando o usuário para editar
    user = db.query(models.User).filter(models.User.id == user_id).first()
    # Retorna o template de edição com os dados do usuário
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})

# Rota para atualizar os dados de um usuário
@app.post("/update/{user_id}")
async def update(request: Request, user_id: int, name: str = Form(...), description: str = Form(...), progress: ProgressStatus = Form(...), db: Session = Depends(get_db)):
    # Buscando o usuário no banco de dados
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        # Atualiza os dados do usuário
        user.name = name
        user.description = description
        user.progress = progress
        db.commit()  # Commit da transação para salvar as alterações no banco
        db.refresh(user)  # Atualiza o objeto para refletir as mudanças
    # Redireciona para a página principal após a atualização
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# Rota para excluir um usuário
@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    # Buscando o usuário a ser excluído
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)  # Deleta o usuário do banco de dados
    db.commit()  # Commit da transação para aplicar a exclusão
    # Redireciona para a página principal após a exclusão
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
