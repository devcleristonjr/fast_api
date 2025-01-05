from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/create", json={
        "name": "Test Task",
        "description": "This is a test task",
        "progress": "open"
    }, auth=("admin", "password"))
    assert response.status_code == 200
    assert response.json()["message"] == "Task created successfully"

def test_list_tasks():
    response = client.get("/tasks", auth=("admin", "password"))
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)

def test_update_task():
    # Primeiro, cria uma tarefa para atualizar
    response = client.post("/tasks/create", json={
        "name": "Test Task",
        "description": "This is a test task",
        "progress": "open"
    }, auth=("admin", "password"))
    task_id = response.json()["task"]["id"]

    # Atualiza a tarefa criada
    response = client.put(f"/tasks/update/{task_id}", json={
        "name": "Updated Task",
        "description": "This is an updated test task",
        "progress": "in progress"
    }, auth=("admin", "password"))
    assert response.status_code == 200
    assert response.json()["message"] == "Task updated successfully"

def test_delete_task():
    # Primeiro, cria uma tarefa para deletar
    response = client.post("/tasks/create", json={
        "name": "Test Task",
        "description": "This is a test task",
        "progress": "open"
    }, auth=("admin", "password"))
    task_id = response.json()["task"]["id"]

    # Deleta a tarefa criada
    response = client.delete(f"/tasks/delete/{task_id}", auth=("admin", "password"))
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

def test_get_task():
    # Primeiro, cria uma tarefa para recuperar
    response = client.post("/tasks/create", json={
        "name": "Test Task",
        "description": "This is a test task",
        "progress": "open"
    }, auth=("admin", "password"))
    task_id = response.json()["task"]["id"]

    # Recupera a tarefa criada
    response = client.get(f"/tasks/{task_id}", auth=("admin", "password"))
    assert response.status_code == 200
    assert "task" in response.json()
