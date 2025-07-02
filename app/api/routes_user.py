from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, authenticate_user
from app.core.jwt import create_access_token
from app.deps import get_current_user
from fastapi import Query
from app.db.mongo import db


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

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

@router.get("/profile", response_model=UserOut)
async def get_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.get("/search", response_model=list[UserOut])
async def search_user(
    keyword: str = Query(..., min_length=1),
    current_user: UserOut = Depends(get_current_user)
):
    cursor = db.users.find({"username": {"$regex": keyword, "$options": "i"}})
    users = []
    async for u in cursor:
        if u["username"] != current_user.username:
            users.append({"id": str(u["_id"]), "username": u["username"]})
    return users