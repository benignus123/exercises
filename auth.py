from fastapi import Depends, HTTPException, status, APIRouter, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
import bcrypt
import jwt
from datetime import datetime, timedelta
from database import get_session
from typing import Optional
from classes import Users
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from depend import get_current_user


router = APIRouter(tags=["auth"], prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функции для работы с паролями
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Создание JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Модели данных
class RegisterForm(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int 
    
class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

# Регистрация пользователя
@router.post("/register", response_model=UserResponse)
def register(user: RegisterForm, db = Depends(get_session)):

    db_user = db.query(Users).filter(Users.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    

    hashed_password = hash_password(user.password)
    
    db_user = Users(
        username=user.username,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_session)
):

    db_user = db.query(Users).filter(Users.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    token_data = {"sub": str(db_user.id), "username": db_user.username}
    access_token = create_access_token(data=token_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60*60*24*7,  
        secure=False,  
        samesite="lax"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id
    }

# Получение текущего пользователя
@router.get("/me", response_model=UserResponse)
def read_me(current_user: Users = Depends(get_current_user)):
    return current_user

# Получение списка всех пользователей
@router.get("/users")
def get_users(db = Depends(get_session)):
    users = db.query(Users).all()
    return {"users": [{"id": user.id, "username": user.username, "is_active": user.is_active} for user in users]}

# Проверка наличия куки
@router.get("/check_cookie")
def read_cookie(access_token: str = Cookie(None)):
    if access_token:
        return {"message": "Cookie is present", "token": access_token[:20] + "..." if len(access_token) > 20 else access_token}
    return {"message": "Cookie not found"}

# Логаут (очистка куки)
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}
