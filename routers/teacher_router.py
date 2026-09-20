from schemas.schemas import Teacher
from database import load_data, save_data
from fastapi import APIRouter, HTTPException, status

teacher_router = APIRouter(prefix="/teacher")


@teacher_router.get("/")
async def get_all_teachers():
    school_info = load_data()
    return school_info["teachers"]

@teacher_router.get("/{teacher_id}")
async def get_teacher_by_id(teacher_id: int):
    school_info = load_data()
    for teacher in school_info["teachers"]:
        if teacher["id"] == teacher_id:
            return teacher
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Учитель не найден")

@teacher_router.post("/")
async def add_new_teacher(teacher_object: Teacher):
    school_info = load_data()
    for teacher in school_info["teachers"]:
        if teacher["id"] == teacher_object.id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Такой учитель уже есть."
            )
        elif teacher["class_id"] == teacher_object.class_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Класс уже привязан к другому учителю"
            )
    school_info["teachers"].append(
        teacher_object.model_dump(mode="json")
    )
    save_data(school_info)

@teacher_router.patch("/{teacher_id}")
async def update_teacher_by_id(teacher_id: int, teacher_object: Teacher):
    school_info = load_data()
    teacher_to_update = None
    for teacher in school_info["teachers"]:
        if teacher["id"] != teacher_id and teacher["class_id"] == teacher_object.class_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Учитель с таким классом уже существует!"
            )
        elif teacher["id"] == teacher_id:
            teacher_to_update = teacher
    if teacher_to_update:
        teacher_to_update["fio"] = teacher_object.fio
        teacher_to_update["class_id"] = teacher_object.class_id
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Учитель не найден")
    save_data(school_info)

@teacher_router.delete("/{teacher_id}", status_code=202)
async def delete_teacher_by_id(teacher_id: int):
    school_info = load_data()
    for teacher in school_info["teachers"]:
        if teacher["id"] == teacher_id:
            school_info["teachers"].remove(teacher)
            save_data(school_info)
            return {"message": "Учитель удален"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Учитель не найден")        