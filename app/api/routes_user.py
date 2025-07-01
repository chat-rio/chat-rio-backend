from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, authenticate_user
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    new_user = await create_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return new_user

@router.post("/login")
async def login(user: UserCreate):
    auth_user = await authenticate_user(user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": auth_user["username"], "id": auth_user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
