from fastapi import FastAPI

from app.database import engine, Base
from app.models import *


Base.metadata.create_all(engine)

app = FastAPI(title="Library API")
