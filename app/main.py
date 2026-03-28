from fastapi import FastAPI

from .database import engine, Base


Base.metadata.create_all(engine)

app = FastAPI(title="Library API")
