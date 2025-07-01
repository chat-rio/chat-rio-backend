from fastapi import FastAPI
from app.api import routes_user
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# API
app.include_router(routes_user.router)

@app.get("/")
async def root():
    return {"message": "FastChat backend is running"}