import uvicorn
from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=6789, reload=True)