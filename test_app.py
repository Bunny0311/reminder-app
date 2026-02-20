# Test for Task Manager REST API

import requests

BASE_URL = "http://localhost:5000/api"

# Test creating a task
def test_create_task():
    response = requests.post(f"{BASE_URL}/tasks", json={"title": "Test Task", "description": "Task for testing"})
    assert response.status_code == 201
    assert "id" in response.json()

# Test retrieving a task
def test_get_task():
    response = requests.get(f"{BASE_URL}/tasks/1")
    assert response.status_code == 200
    assert "title" in response.json()

# Test updating a task
def test_update_task():
    response = requests.put(f"{BASE_URL}/tasks/1", json={"title": "Updated Task"})
    assert response.status_code == 200

# Test deleting a task
def test_delete_task():
    response = requests.delete(f"{BASE_URL}/tasks/1")
    assert response.status_code == 204
