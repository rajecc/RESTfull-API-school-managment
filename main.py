# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from routers.school_class_router import school_class_router

app = FastAPI()

app.include_router(school_class_router)