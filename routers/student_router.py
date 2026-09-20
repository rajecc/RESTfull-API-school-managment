from schemas.schemas import Student
from database import load_data, save_data
from fastapi import APIRouter,  HTTPException, status

student_router = APIRouter(prefix="/student")

@student_router.get("/")
async def get_all_students():
    school_info = load_data()
    return school_info["students"]

@student_router.get("/{student_id}")
async def get_student_by_id(student_id: int):
    school_info = load_data()
    for student in school_info["students"]:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

@student_router.post("/")
async def add_new_student(student_object: Student):
    school_info = load_data()
    for student in school_info["students"]:
        if student["id"] == student_object.id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Студент с таким id уже существует!")

    school_info["students"].append(student_object.model_dump(mode="json"))
    save_data(school_info)

@student_router.patch("/{student_id}")
async def update_student_by_id(student_id: int, student_object: Student):
    school_info = load_data()
    student_to_update = None
    for student in school_info["students"]:
        if student["id"] == student_id:
            student_to_update = student
    if student_to_update:
        student_to_update["fio"] = student_object.fio
        student_to_update["birth_date"] = student_object.birth_date.isoformat()
        student_to_update["class_ranking"] = student_object.class_ranking
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    save_data(school_info)

@student_router.delete("/{student_id}", status_code=202)
async def delete_student_by_id(student_id: int):
    school_info = load_data()
    for student in school_info["students"]:
        if student["id"] == student_id:
            school_info["students"].remove(student)
            save_data(school_info)
            return {"message": "Ученик удален"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")