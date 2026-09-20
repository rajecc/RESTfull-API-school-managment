from routers.school_class_router import add_new_school_class
from unicodedata import name
import pytest
from database import save_data
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    save_data(
        {
            "school_classes": [],
            "teachers": [],
            "students": []
        }
    )

def test_school_class_crud():
    get_all_school_classes = client.get("/school_class")
    assert get_all_school_classes.status_code == 200

    add_new_school_class = client.post("/school_class", json={"id": 1, "name": "10-А", "number_of_students": 25, "teacher_id": 2})
    assert add_new_school_class.status_code == 200

    get_one_school_class = client.get("/school_class/1")
    assert get_one_school_class.status_code == 200
    
    update_one_school_class = client.patch("/school_class/1", json={"id": 1, "name": "10-Б", "number_of_students": 25, "teacher_id": 2})
    assert update_one_school_class.status_code == 200

    get_one_school_class = client.get("/school_class/1")
    assert get_one_school_class.status_code == 200
    assert get_one_school_class.json() == {"id": 1, "name": "10-Б", "number_of_students": 25, "teacher_id": 2}

    delete_one_school_class = client.delete("/school_class/1")
    assert delete_one_school_class.status_code == 202

    get_one_school_class = client.get("/school_class/1")
    assert get_one_school_class.status_code == 404

    get_all_school_classes = client.get("/school_class")
    assert get_all_school_classes.status_code == 200
    assert get_all_school_classes.json() == []

def test_teacher_crud():
    get_all_teachers = client.get("/teacher")
    assert get_all_teachers.status_code == 200

    add_new_teacher = client.post("/teacher", json={"id": 1, "fio": "Иванов Иван Иванович", "school_class_id": 1})
    assert add_new_teacher.status_code == 200

    get_one_teacher = client.get("/teacher/1")
    assert get_one_teacher.status_code == 200
    
    update_one_teacher = client.patch("/teacher/1", json={"id": 1, "fio": "Иванов Иван Петрович", "school_class_id": 1})
    assert update_one_teacher.status_code == 200

    get_one_teacher = client.get("/teacher/1")
    assert get_one_teacher.status_code == 200
    assert get_one_teacher.json() == {"id": 1, "fio": "Иванов Иван Петрович", "school_class_id": 1}

    delete_one_teacher = client.delete("/teacher/1")
    assert delete_one_teacher.status_code == 202

    get_one_teacher = client.get("/teacher/1")
    assert get_one_teacher.status_code == 404

    get_all_teachers = client.get("/teacher")
    assert get_all_teachers.status_code == 200
    assert get_all_teachers.json() == []

def test_student_crud():
    get_all_students = client.get("/student")
    assert get_all_students.status_code == 200

    add_new_student = client.post("/student", json={"id": 1, "fio": "Петров Петр Петрович", "birth_date": "2000-01-01", "class_ranking": 10})
    assert add_new_student.status_code == 200

    get_one_student = client.get("/student/1")
    assert get_one_student.status_code == 200
    
    update_one_student = client.patch("/student/1", json={"id": 1, "fio": "Петров Петр Петрович", "birth_date": "2000-01-01", "class_ranking": 10})
    assert update_one_student.status_code == 200

    get_one_student = client.get("/student/1")
    assert get_one_student.status_code == 200
    assert get_one_student.json() == {"id": 1, "fio": "Петров Петр Петрович", "birth_date": "2000-01-01", "class_ranking": 10}

    delete_one_student = client.delete("/student/1")
    assert delete_one_student.status_code == 202

    get_one_student = client.get("/student/1")
    assert get_one_student.status_code == 404

    get_all_students = client.get("/student")
    assert get_all_students.status_code == 200
    assert get_all_students.json() == []


def test_unique_teacher():
    client.post("/school_class", json={"id": 1, "name": "10-А", "number_of_students": 25, "teacher_id": 2})
    add_class_same_teacher = client.post("/school_class", json={"id": 2, "name": "10-А", "number_of_students": 25, "teacher_id": 2})
    assert add_class_same_teacher.status_code == 500

def test_unique_school_class():
    client.post("/teacher", json={"id": 1, "fio": "Иванов Иван Петрович", "school_class_id": 2})
    add_teacher_same_school_class = client.post("/teacher", json={"id": 2, "fio": "Петров Петр Иванович", "school_class_id": 2})
    assert add_teacher_same_school_class.status_code == 500