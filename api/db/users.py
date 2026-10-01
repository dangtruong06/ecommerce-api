from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import DBUser, NotFoundError, EmailAlreadyExistsError
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordBearer
import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str  

class UserUpdate(BaseModel):
    email: Optional[str] = None

def read_db_user_by_email(email, session: Session) -> Optional[DBUser]:
    return session.query(DBUser).filter(DBUser.email == email).first()

# Get User
def read_db_user(id: int, session: Session) -> DBUser:
    return session.query(DBUser).filter(DBUser.id == id).first()

# Create User
def create_db_user(user_create: UserCreate, session: Session) -> DBUser:
    email_exists = read_db_user_by_email(user_create.email, session)
    
    if email_exists is not None:
        raise EmailAlreadyExistsError("This email is already taken")
    
    password_hash = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt())
    db_user = DBUser(email=user_create.email, password=password_hash.decode())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Update User
def update_db_user(user_id: int, user_update: UserUpdate, session: Session) -> DBUser:
    return



def delete_db_user(user_id: int, session: Session) -> DBUser:
    return