from fastapi import FastAPI
from .routers import users, auth, entries, tags
from .database import engine
from . import models

models.Base.metadata.create_all(bind = engine)


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(entries.router)
app.include_router(tags.router)

