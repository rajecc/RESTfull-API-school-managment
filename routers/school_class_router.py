from schemas.schemas import SchoolClass
from database import load_data, save_data
from fastapi import APIRouter,  HTTPException, status

school_class_router = APIRouter(prefix="/school_class")

@school_class_router.get("/")
async def get_all_school_classes():
    school_info = load_data()
    return school_info["school_classes"]

@school_class_router.get("/{school_class_id}")
async def get_school_class_by_id(school_class_id: int):
    school_info = load_data()
    for school_class in school_info["school_classes"]:
        if school_class["id"] == school_class_id:
            return school_class
    raise HTTPException(status_code=404, detail="Класс не найден")

@school_class_router.post("/")
async def add_new_school_class(school_class_object: SchoolClass):
    school_info = load_data()
    for school_class in school_info["school_classes"]:
        if school_class["id"] == school_class_object.id:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Такой класс уже есть."
            )
        elif school_class["teacher_id"] == school_class_object.teacher_id:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="У учителя может быть только один класс!"
            )
    school_info["school_classes"].append(
        school_class_object.model_dump(mode="json")
    )
    save_data(school_info)

@school_class_router.patch("/{school_class_id}")
async def update_class_by_id(school_class_id: int, school_class_object: SchoolClass):
    school_info = load_data()
    school_class_to_update = None
    for school_class in school_info["school_classes"]:
        if school_class["id"] != school_class_id and school_class["teacher_id"] == school_class_object.teacher_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Класс с таким учителем уже есть!")
        elif school_class["id"] == school_class_id:
            school_class_to_update = school_class
    if school_class_to_update:
        school_class_to_update["name"] = school_class_object.name
        school_class_to_update["teacher_id"] = school_class_object.teacher_id
        school_class_to_update["number_of_students"] = school_class_object.number_of_students
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Класс не найден")
    save_data(school_info)

@school_class_router.delete("/{school_class_id}", status_code=202)
async def delete_school_class_by_id(school_class_id: int):
    school_info = load_data()
    for school_class in school_info["school_classes"]:
        if school_class["id"] == school_class_id:
            school_info["school_classes"].remove(school_class)
            save_data(school_info)

            return {"message": "Класс удален"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Класс не найден")