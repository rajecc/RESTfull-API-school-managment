from datetime import date
from pydantic import BaseModel, Field

class SchoolClass(BaseModel):
    id: int
    name: str = Field(max_length = 20)
    teacher_id: int
    number_of_students: int = Field(ge = 0, le = 40)

class Teacher(BaseModel):
    id: int
    fio: str = Field(max_length = 100)
    school_class_id: int

class Student(BaseModel):
    id: int
    fio: str = Field(max_length = 100)
    birth_date: date
    class_ranking: int


