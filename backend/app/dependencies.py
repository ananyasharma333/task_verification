from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from bson import ObjectId
from app.security import decode_access_token
from app.database import get_database
from app.models.user import UserInDB, RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
        
    db = get_database()
    user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if user_doc is None:
        raise credentials_exception
    
    # Motor returns _id as ObjectId, map it to string id
    user_doc["_id"] = str(user_doc["_id"])
    return UserInDB(**user_doc)

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    # Currently all registered users are active, but this is a placeholder for future logic
    return current_user

def require_role(roles: List[RoleEnum]):
    async def role_checker(current_user: UserInDB = Depends(get_current_active_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough privileges"
            )
        return current_user
    return role_checker
